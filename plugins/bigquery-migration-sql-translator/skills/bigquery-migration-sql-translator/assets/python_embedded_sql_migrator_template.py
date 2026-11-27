#!/usr/bin/env python3
r"""Template Script for Automated Python Embedded SQL AST Migration.

This asset template script provides a reference implementation for preprocessing
and postprocessing application codebases for BigQuery Migration Service (BQMS):
  1. Preprocessing (AST Extraction): Scans Python codebase, extracts full SQL
     statements, parameterized queries, and partial SQL expression/predicate
     segments (e.g. df.filter(), df.selectExpr(), expr(), sqlalchemy.text()),
     discovers non-SQL DataFrame views (df.createOrReplaceTempView()), and
     writes manifest.json plus staged .sql files with unambiguous wrappers.
  2. Transpilation: Staged .sql files are transpiled via BigQuery Migration
     Service (BQMS) batch migration.
  3. Postprocessing (AST Re-injection): Reads BigQuery Migration Service (BQMS)
     translated SQL, structurally unwraps fragments, preserves quote
     styles/triple-quotes for multi-line injection, maps queries via manifest
     bottom-up by occurrence span, and safely re-injects GoogleSQL back into
     Python codebases.

Usage Pattern:
  AI agents and engineers should copy this template file to a local working
  directory or scratch space and adjust it per situational needs (e.g., custom
  database framework calls, project-specific AST visitors, or dialect rules).

Example Execution:
  python3 python_embedded_sql_migrator_template.py --preprocess \
      --src ./my_project --staging ./staging_input --manifest ./manifest.json

  python3 python_embedded_sql_migrator_template.py --postprocess \
      --src ./my_project --staging-out ./staging_output \
      --manifest ./manifest.json --out ./output/my_project
"""

import argparse
import ast
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Optional

# Strict SQL clause regex to prevent false-positives on plain strings.
STRICT_SQL_CLAUSE_REGEX = re.compile(
    r"^(?:\s|/\*[\s\S]*?\*/|--[^\r\n]*|#[^\r\n]*)*"
    r"(?:"
    r"SELECT\s+(?:.*?\s+FROM\b|[^;\n]+)|"
    r"INSERT\s+(?:INTO|OVERWRITE)\b|"
    r"REPLACE\s+INTO\b|"
    r"UPDATE\s+.*?\s+SET\b|"
    r"DELETE\s+FROM\b|"
    r"TRUNCATE\s+TABLE\b|"
    r"CREATE\s+(?:OR\s+REPLACE\s+)?"
    r"(?:TEMP|TEMPORARY|TABLE|VIEW|PROCEDURE|FUNCTION|SCHEMA|DATABASE)\b|"
    r"DROP\s+(?:TABLE|VIEW|FUNCTION|PROCEDURE|SCHEMA|DATABASE)\b|"
    r"ALTER\s+(?:TABLE|VIEW|SCHEMA|DATABASE)\b|"
    r"WITH\s+.*?\s+AS\s*\(|"
    r"MERGE\s+INTO\b|"
    r"COPY\s+INTO\b|"
    r"CALL\s+[A-Za-z0-9_.`\"'\[\]]+\s*\(|"
    r"DECLARE\s+[A-Za-z_]|"
    r"BEGIN\b[\s\S]+\bEND\b|"
    r"GRANT\s+.*?\s+ON\b|"
    r"REVOKE\s+.*?\s+ON\b"
    r")",
    re.IGNORECASE | re.DOTALL,
)

# Recognized DB/ORM execution method names across Python SQL frameworks.
EXECUTE_METHOD_NAMES = (
    "execute",
    "execute_async",
    "executemany",
    "read_gbq",
    "query",
    "sql",
    "text",
    "sql_expr",
    "raw_sql",
)

# DataFrame methods taking partial SQL expression or predicate fragments.
DATAFRAME_FRAGMENT_METHODS = {
    "expr": "expression",
    "selectExpr": "select_list",
    "filter": "predicate",
    "where": "predicate",
}

# DataFrame view registration methods.
VIEW_REGISTRATION_METHODS = (
    "createOrReplaceTempView",
    "createTempView",
    "createOrReplaceGlobalTempView",
    "createGlobalTempView",
    "registerTempTable",
)

# Common SQL placeholder patterns for parameterized queries, plus SQL string
# literals and `::` type-cast operators that must be skipped during masking.
SQL_LITERAL_OR_PLACEHOLDER_REGEX = re.compile(
    r"('(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|::)"
    r"|(%[sdf]|%\([^)]+\)s|\?|(?<!:):[a-zA-Z_]\w*|\$\d+|\{[^{}]*\})"
)
PARAMETER_PLACEHOLDER_REGEX = re.compile(
    r"(%[sdf]|%\([^)]+\)s|\?|(?<!:):[a-zA-Z_]\w*|\$\d+|\{[^{}]*\})"
)

# Markers placed around fragments during staging for BigQuery Migration Service
# (BQMS) compilation.
FRAGMENT_EXPR_HEADER = "/* BQMS_FRAGMENT:EXPR */ SELECT "
FRAGMENT_PRED_HEADER = (
    "/* BQMS_FRAGMENT:PREDICATE */ SELECT * FROM __placeholder_table__ WHERE "
)


class SQLExtractor(ast.NodeVisitor):
  """AST Visitor to discover and extract SQL strings and fragments."""

  def __init__(self, file_path: str, relative_path: str) -> None:
    self.file_path = file_path
    self.relative_path = relative_path
    self.rel_path = relative_path  # Alias for backward compatibility
    self.extracted_queries: list[dict[str, Any]] = []
    self.discovered_views: list[dict[str, Any]] = []
    self._extracted_nodes: set[int] = set()

  def _is_strict_sql(self, text: Any) -> bool:
    """Checks if string matches top-level SQL structure."""
    if not text or not isinstance(text, str):
      return False
    clean = text.strip()
    if len(clean) < 8:
      return False
    return STRICT_SQL_CLAUSE_REGEX.search(clean) is not None

  def _detect_parameterization(self, sql_text: str) -> dict[str, Any]:
    """Detects if SQL string contains placeholders or parameter bindings."""
    matches = [
        m.group(2)
        for m in SQL_LITERAL_OR_PLACEHOLDER_REGEX.finditer(sql_text)
        if m.group(2) is not None
    ]
    is_param = len(matches) > 0
    style = "none"
    if is_param:
      sample = matches[0]
      if sample.startswith("%"):
        style = "py_printf"
      elif sample == "?":
        style = "qmark"
      elif sample.startswith(":"):
        style = "named_colon"
      elif sample.startswith("$"):
        style = "numeric_dollar"
      elif sample.startswith("{") and sample.endswith("}"):
        style = "format_brace"
    return {
        "is_parameterized": is_param,
        "parameter_style": style,
        "placeholders": matches,
    }

  def _generate_query_id(self, line_number: int) -> str:
    """Generates unique query ID from file path, line number, and index."""
    normalized = self.relative_path.replace("\\", "/").replace("/", "__")
    clean_path = re.sub(r"[^a-zA-Z0-9_]", "_", normalized)
    sequence_index = len(self.extracted_queries) + 1
    return f"{clean_path}_{line_number}_{sequence_index}"

  def _record_span(self, target_node: ast.AST) -> dict[str, Optional[int]]:
    """Extracts source line and column span metadata from an AST node."""
    return {
        "col_offset": getattr(target_node, "col_offset", None),
        "end_lineno": getattr(target_node, "end_lineno", None),
        "end_col_offset": getattr(target_node, "end_col_offset", None),
    }

  def _record_assignment_node(
      self, lineno: int, value_node: ast.AST, node_type: str
  ) -> None:
    """Extracts SQL strings from assignment value nodes."""
    sql_val = self._extract_node_str(value_node)
    if sql_val and self._is_strict_sql(sql_val):
      self._extracted_nodes.add(id(value_node))
      query_id = self._generate_query_id(lineno)
      param_info = self._detect_parameterization(sql_val)
      entry = {
          "query_id": query_id,
          "file_path": self.file_path,
          "relative_path": self.relative_path,
          "rel_path": self.relative_path,
          "line_number": lineno,
          "line_no": lineno,
          "original_sql": sql_val,
          "node_type": node_type,
          "fragment_type": "statement",
          "is_parameterized": param_info["is_parameterized"],
          "parameter_style": param_info["parameter_style"],
      }
      entry.update(self._record_span(value_node))
      self.extracted_queries.append(entry)

  # pylint: disable=invalid-name
  def visit_Assign(self, node: ast.Assign) -> None:
    """Extracts SQL strings from assignments requiring strict SQL structure."""
    self._record_assignment_node(node.lineno, node.value, "Assign")
    self.generic_visit(node)

  def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
    """Extracts SQL strings from type-annotated assignments."""
    if node.value is not None:
      self._record_assignment_node(node.lineno, node.value, "AnnAssign")
    self.generic_visit(node)

  def visit_Call(self, node: ast.Call) -> None:  # pylint: disable=invalid-name
    """Extracts SQL or fragments from recognized DB, ORM & DataFrame calls."""
    if id(node) in self._extracted_nodes:
      self.generic_visit(node)
      return

    method_name: Optional[str] = None
    receiver_name: Optional[str] = None
    if isinstance(node.func, ast.Attribute):
      method_name = node.func.attr
      if isinstance(node.func.value, ast.Name):
        receiver_name = node.func.value.id
    elif isinstance(node.func, ast.Name):
      method_name = node.func.id

    # 1. Non-SQL DataFrame view registration
    if method_name in VIEW_REGISTRATION_METHODS and node.args:
      view_arg = self._extract_node_str(node.args[0])
      if view_arg:
        self.discovered_views.append({
            "view_name": view_arg,
            "line_number": node.lineno,
            "dataframe_var": receiver_name or "df",
            "file_path": self.file_path,
            "relative_path": self.relative_path,
        })

    # 2. Recognized DB & ORM execution wrappers
    elif method_name in EXECUTE_METHOD_NAMES and node.args:
      first_arg = node.args[0]
      if id(first_arg) not in self._extracted_nodes:
        sql_str = self._extract_node_str(first_arg)
        if sql_str and self._is_strict_sql(sql_str):
          self._extracted_nodes.add(id(first_arg))
          query_id = self._generate_query_id(node.lineno)
          param_info = self._detect_parameterization(sql_str)
          entry = {
              "query_id": query_id,
              "file_path": self.file_path,
              "relative_path": self.relative_path,
              "rel_path": self.relative_path,
              "line_number": node.lineno,
              "line_no": node.lineno,
              "original_sql": sql_str,
              "node_type": type(first_arg).__name__,
              "fragment_type": "statement",
              "is_parameterized": param_info["is_parameterized"],
              "parameter_style": param_info["parameter_style"],
          }
          entry.update(self._record_span(first_arg))
          self.extracted_queries.append(entry)

    # 3. Partial SQL segment methods (df.filter(), df.selectExpr(), expr())
    elif method_name is not None and method_name in DATAFRAME_FRAGMENT_METHODS:
      fragment_kind = DATAFRAME_FRAGMENT_METHODS[method_name]
      args_to_check = (
          node.args if method_name == "selectExpr" else node.args[:1]
      )

      for arg in args_to_check:
        if id(arg) in self._extracted_nodes:
          continue
        frag_str = self._extract_node_str(arg)
        if frag_str and frag_str.strip():
          self._extracted_nodes.add(id(arg))
          query_id = self._generate_query_id(node.lineno)
          param_info = self._detect_parameterization(frag_str)
          entry = {
              "query_id": query_id,
              "file_path": self.file_path,
              "relative_path": self.relative_path,
              "rel_path": self.relative_path,
              "line_number": node.lineno,
              "line_no": node.lineno,
              "original_sql": frag_str,
              "node_type": type(arg).__name__,
              "fragment_type": fragment_kind,
              "method_call": method_name,
              "is_parameterized": param_info["is_parameterized"],
              "parameter_style": param_info["parameter_style"],
          }
          entry.update(self._record_span(arg))
          self.extracted_queries.append(entry)

    self.generic_visit(node)

  def _extract_binop_str(self, binop_node: ast.BinOp) -> Optional[str]:
    """Extracts concatenated strings from binary add or modulo operations."""
    if isinstance(binop_node.op, ast.Add):
      left_str = self._extract_node_str(binop_node.left)
      right_str = self._extract_node_str(binop_node.right)
      if left_str is not None and right_str is not None:
        return left_str + right_str
    elif isinstance(binop_node.op, ast.Mod):
      return self._extract_node_str(binop_node.left)
    return None

  def _extract_joined_str(self, joined_node: ast.JoinedStr) -> Optional[str]:
    """Extracts string representation from Python f-string AST nodes."""
    parts: list[str] = []
    conv_map = {97: "!a", 114: "!r", 115: "!s"}
    for part in joined_node.values:
      if isinstance(part, ast.Constant) and isinstance(part.value, str):
        parts.append(part.value)
      elif isinstance(part, ast.FormattedValue):
        expr_src = (
            ast.unparse(part.value) if hasattr(ast, "unparse") else "param"
        )
        conv_str = conv_map.get(getattr(part, "conversion", -1), "")
        spec_str = ""
        if getattr(part, "format_spec", None) is not None and isinstance(
            part.format_spec, ast.JoinedStr
        ):
          extracted_spec = self._extract_joined_str(part.format_spec)
          if extracted_spec:
            spec_str = f":{extracted_spec}"
        parts.append(f"{{{expr_src}{conv_str}{spec_str}}}")
    return "".join(parts) if parts else None

  def _extract_node_str(self, node: ast.AST) -> Optional[str]:
    """Extracts string content from constant, binop, joined, or call nodes."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
      return node.value
    elif isinstance(node, ast.BinOp):
      return self._extract_binop_str(node)
    elif isinstance(node, ast.JoinedStr):
      return self._extract_joined_str(node)
    elif isinstance(node, ast.Call):
      if isinstance(node.func, ast.Attribute) and node.func.attr == "format":
        self._extracted_nodes.add(id(node))
        return self._extract_node_str(node.func.value)
      elif isinstance(node.func, ast.Name) and node.func.id in (
          "text",
          "sql_expr",
      ):
        if node.args:
          self._extracted_nodes.add(id(node))
          self._extracted_nodes.add(id(node.args[0]))
          return self._extract_node_str(node.args[0])
    return None


def mask_sql_placeholders(sql_text: str) -> tuple[str, dict[str, str]]:
  """Masks parameter placeholders with valid SQL identifiers for BigQuery Migration Service (BQMS) staging."""
  placeholder_map: dict[str, str] = {}
  counter = 0

  def _replacer(match: re.Match[str]) -> str:
    if match.group(1) is not None:
      return match.group(1)
    nonlocal counter
    counter += 1
    token = f"__BQMS_PARAM_{counter}__"
    placeholder_map[token] = match.group(2)
    return token

  masked_sql = SQL_LITERAL_OR_PLACEHOLDER_REGEX.sub(_replacer, sql_text)
  return masked_sql, placeholder_map


def restore_sql_placeholders(
    sql_text: str, placeholder_map: Optional[dict[str, str]]
) -> str:
  """Restores original parameter placeholders into translated SQL."""
  if not placeholder_map:
    return sql_text
  result = sql_text
  # Sort tokens longest-first to avoid partial prefix replacements.
  for token in sorted(placeholder_map.keys(), key=len, reverse=True):
    orig = placeholder_map[token]
    result = re.sub(
        r"`?" + re.escape(token) + r"`?",
        lambda _, r=orig: r,
        result,
        flags=re.IGNORECASE,
    )
  return result


def wrap_fragment_for_staging(sql_text: str, fragment_type: str) -> str:
  """Wraps partial SQL fragments into valid statements for BigQuery Migration Service (BQMS) translation."""
  clean = sql_text.strip()
  if fragment_type in ("expression", "select_list"):
    return f"{FRAGMENT_EXPR_HEADER}{clean};"
  elif fragment_type == "predicate":
    return f"{FRAGMENT_PRED_HEADER}{clean};"
  else:
    if not clean.endswith(";"):
      clean += ";"
    return clean


def unwrap_fragment_after_translation(
    translated_sql: str, fragment_type: str
) -> Optional[str]:
  """Anchor-based structural unwrapping of expression or predicate fragments."""
  clean = translated_sql.strip()
  if clean.endswith(";"):
    clean = clean[:-1].strip()

  if fragment_type in ("expression", "select_list"):
    # Strip anchor marker header at index 0 without matching subqueries
    prefix_match = re.search(
        r"^(?:/\*.*?\*/\s*)?select\s+", clean, re.IGNORECASE | re.DOTALL
    )
    if prefix_match:
      return clean[prefix_match.end() :].strip()
    return None
  elif fragment_type == "predicate":
    # Strip outer placeholder selection wrapper anchor at index 0
    prefix_match = re.search(
        r"^(?:/\*.*?\*/\s*)?select\s+\*\s+from"
        r"\s+(?:[`\w.-]+\.)*`?__placeholder_table__`?\s+where\s+",
        clean,
        re.IGNORECASE | re.DOTALL,
    )
    if prefix_match:
      return clean[prefix_match.end() :].strip()
    return None

  return clean


def format_sql_for_python(
    translated_sql: str, original_sql: Optional[str] = None
) -> str:
  del original_sql
  clean_sql = translated_sql.strip()
  if "\n" not in clean_sql:
    return clean_sql
  lines = clean_sql.split("\n")
  if len(lines) <= 2:
    return " ".join(line.strip() for line in lines if line.strip())
  return f"\n{clean_sql}\n"


def _compute_span_offsets(
    content: str,
    line_number: Optional[int],
    col_offset: Optional[int],
    end_lineno: Optional[int],
    end_col_offset: Optional[int],
) -> Optional[tuple[int, int]]:
  """Computes character start/end offsets in content from 1-based AST span."""
  if (
      line_number is None
      or col_offset is None
      or end_lineno is None
      or end_col_offset is None
      or line_number < 1
      or end_lineno < line_number
  ):
    return None
  lines = content.splitlines(keepends=True)
  if end_lineno > len(lines):
    return None
  start_line_offset = sum(len(l) for l in lines[: line_number - 1])
  end_line_offset = sum(len(l) for l in lines[: end_lineno - 1])
  start_idx = start_line_offset + len(
      lines[line_number - 1]
      .encode("utf-8")[:col_offset]
      .decode("utf-8", errors="ignore")
  )
  end_idx = end_line_offset + len(
      lines[end_lineno - 1]
      .encode("utf-8")[:end_col_offset]
      .decode("utf-8", errors="ignore")
  )
  if 0 <= start_idx < end_idx <= len(content):
    return start_idx, end_idx
  return None


def safe_reinject_into_python(
    content: str,
    original_sql: str,
    translated_sql: str,
    line_number: Optional[int] = None,
    col_offset: Optional[int] = None,
    end_lineno: Optional[int] = None,
    end_col_offset: Optional[int] = None,
) -> str:
  """Safely injects translated SQL string into Python code."""
  replacement = translated_sql.strip()
  target_str = original_sql if original_sql in content else original_sql.strip()

  def _escape_triple_body(text: str, quote: str) -> str:
    escaped = text.replace(quote, f"\\{quote[0]}" * 3)
    if escaped.endswith(quote[0]):
      escaped = escaped[:-1] + f"\\{quote[0]}"
    return escaped

  def _prepare_triple_replacement(text: str, quote: str) -> str:
    return f"{quote}{_escape_triple_body(text, quote)}{quote}"

  def _prepare_single_replacement(text: str, quote: str) -> str:
    escaped = text.replace(quote, f"\\{quote}")
    return f"{quote}{escaped}{quote}"

  span_bounds = _compute_span_offsets(
      content, line_number, col_offset, end_lineno, end_col_offset
  )
  search_start = 0
  if span_bounds is not None:
    search_start = span_bounds[0]
  elif line_number and line_number > 1:
    lines = content.splitlines(keepends=True)
    if line_number <= len(lines):
      search_start = sum(len(l) for l in lines[: line_number - 1])

  target_escaped_double = target_str.replace('"', '\\"')
  target_escaped_single = target_str.replace("'", "\\'")

  patterns_to_try = [
      (f'"""{target_str}"""', "triple_double"),
      (f"'''{target_str}'''", "triple_single"),
      (f'"{target_str}"', "double"),
      (f"'{target_str}'", "single"),
  ]
  if target_escaped_double != target_str:
    patterns_to_try.append((f'"{target_escaped_double}"', "double"))
  if target_escaped_single != target_str:
    patterns_to_try.append((f"'{target_escaped_single}'", "single"))
  patterns_to_try.append((target_str, "bare"))

  for pat, kind in patterns_to_try:
    idx = content.find(pat, search_start)
    if idx == -1 and search_start > 0:
      idx = content.find(pat)
    if idx != -1:
      # If bare match is inside single-line quotes and replacement is multiline,
      # promote enclosing single-line quotes to triple quotes.
      if kind == "bare" and "\n" in replacement:
        line_start = content.rfind("\n", 0, idx) + 1
        line_end = content.find("\n", idx + len(pat))
        if line_end == -1:
          line_end = len(content)
        before_on_line = content[line_start:idx]
        after_on_line = content[idx + len(pat) : line_end]
        for q_char, triple_q in (('"', '"""'), ("'", "'''")):
          if (
              q_char in before_on_line
              and q_char in after_on_line
              and triple_q not in before_on_line
          ):
            q_open = line_start + before_on_line.rfind(q_char)
            q_close = idx + len(pat) + after_on_line.find(q_char)
            inner_prefix = content[q_open + 1 : idx]
            inner_suffix = content[idx + len(pat) : q_close]
            rep_val = _prepare_triple_replacement(
                inner_prefix + replacement + inner_suffix, triple_q
            )
            return content[:q_open] + rep_val + content[q_close + 1 :]

      if "\n" in replacement:
        if kind == "triple_double":
          rep_val = _prepare_triple_replacement(replacement, '"""')
        elif kind == "triple_single":
          rep_val = _prepare_triple_replacement(replacement, "'''")
        elif kind == "double":
          if '"""' in replacement and "'''" not in replacement:
            rep_val = _prepare_triple_replacement(replacement, "'''")
          else:
            rep_val = _prepare_triple_replacement(replacement, '"""')
        elif kind == "single":
          if "'''" in replacement and '"""' not in replacement:
            rep_val = _prepare_triple_replacement(replacement, '"""')
          else:
            rep_val = _prepare_triple_replacement(replacement, "'''")
        else:
          if content.rfind('"""', 0, idx) > content.rfind("'''", 0, idx):
            rep_val = _escape_triple_body(replacement, '"""')
          elif content.rfind("'''", 0, idx) > content.rfind('"""', 0, idx):
            rep_val = _escape_triple_body(replacement, "'''")
          else:
            rep_val = replacement
      else:
        if kind == "triple_double":
          rep_val = _prepare_triple_replacement(replacement, '"""')
        elif kind == "triple_single":
          rep_val = _prepare_triple_replacement(replacement, "'''")
        elif kind == "double":
          rep_val = _prepare_single_replacement(replacement, '"')
        elif kind == "single":
          rep_val = _prepare_single_replacement(replacement, "'")
        else:
          if content.rfind('"""', 0, idx) > content.rfind("'''", 0, idx):
            rep_val = _escape_triple_body(replacement, '"""')
          elif content.rfind("'''", 0, idx) > content.rfind('"""', 0, idx):
            rep_val = _escape_triple_body(replacement, "'''")
          else:
            rep_val = replacement

      return content[:idx] + rep_val + content[idx + len(pat) :]

  # AST span-based literal replacement fallback (handles string literals with
  # raw escape sequences like \n or \t where literal substring search differs).
  if span_bounds is not None:
    s_start, s_end = span_bounds
    node_src = content[s_start:s_end]
    m_lit = re.fullmatch(
        r"([fFrRbBuU]*)(?P<q>\"\"\"|'''|\"|')(?P<body>.*)(?P=q)",
        node_src,
        flags=re.DOTALL,
    )
    if m_lit:
      prefix = m_lit.group(1)
      quote = m_lit.group("q")
      if "\n" in replacement and len(quote) == 1:
        triple_q = quote * 3
        rep_lit = prefix + _prepare_triple_replacement(replacement, triple_q)
      elif len(quote) == 3:
        rep_lit = prefix + _prepare_triple_replacement(replacement, quote)
      else:
        rep_lit = prefix + _prepare_single_replacement(replacement, quote)
      return content[:s_start] + rep_lit + content[s_end:]

  # Fallback for concatenated string literals
  tokens = [re.escape(t) for t in re.split(r"\s+", target_str) if t]
  if tokens:
    sep = r"""(?:\s*(?:['"]\s*(?:\+\s*)?['"]|\s)\s*)"""
    pat_str = r"""(['"]?)""" + sep.join(tokens) + r"""(['"]?)"""
    match = re.search(pat_str, content[search_start:], flags=re.IGNORECASE)
    offset = search_start
    if not match and search_start > 0:
      match = re.search(pat_str, content, flags=re.IGNORECASE)
      offset = 0
    if match:
      m_start = offset + match.start()
      m_end = offset + match.end()
      matched_text = match.group(0)
      if matched_text.startswith(('"', "'")) and matched_text.endswith(
          ('"', "'")
      ):
        is_single_quote = matched_text.startswith("'")
        if "\n" in replacement:
          quote = "'''" if is_single_quote else '"""'
          rep_val = _prepare_triple_replacement(replacement, quote)
        else:
          quote = "'" if is_single_quote else '"'
          rep_val = _prepare_single_replacement(replacement, quote)
        return content[:m_start] + rep_val + content[m_end:]
      return content[:m_start] + replacement + content[m_end:]

  return content


# Most elements one BigQuery GENERATE_ARRAY call may return.
GENERATE_ARRAY_MAX_ELEMENTS = 1048576
# Inner array size when a range needs a cross join of two arrays.
_RANGE_CHUNK = 1000000


def range_to_googlesql(start: int, end: int) -> Optional[str]:
  """Returns a GoogleSQL table expression for Spark `range(start, end)`.

  Like Spark's `range`, the result has one INT64 column named `id`, so
  references such as `t.id` keep working. BigQuery's `GENERATE_ARRAY` returns
  at most `GENERATE_ARRAY_MAX_ELEMENTS` values, so larger ranges cross join two
  arrays.

  Args:
    start: First value (inclusive).
    end: Last value (exclusive).

  Returns:
    A parenthesized subquery, or None if the range is too large to express.
  """
  count = end - start
  if count <= GENERATE_ARRAY_MAX_ELEMENTS:
    return f"(SELECT id FROM UNNEST(GENERATE_ARRAY({start}, {end - 1})) AS id)"
  chunks = -(-count // _RANGE_CHUNK)
  if chunks > GENERATE_ARRAY_MAX_ELEMENTS:
    return None
  offset = f"{start} + " if start else ""
  where = (
      f" WHERE hi * {_RANGE_CHUNK} + lo < {count}"
      if count % _RANGE_CHUNK
      else ""
  )
  return (
      f"(SELECT {offset}hi * {_RANGE_CHUNK} + lo AS id"
      f" FROM UNNEST(GENERATE_ARRAY(0, {chunks - 1})) AS hi"
      f" CROSS JOIN UNNEST(GENERATE_ARRAY(0, {_RANGE_CHUNK - 1})) AS lo{where})"
  )


def apply_fallback_rules(sql_statement: str) -> str:
  """Applies heuristic fallback transforms for non-standard dialect syntax."""
  result = sql_statement

  def _replace_from_unixtime(match: re.Match[str]) -> str:
    ts_expr = match.group(1).strip()
    fmt_literal = match.group(2).strip()
    if "%" not in fmt_literal:
      fmt_literal = (
          fmt_literal.replace("yyyy", "%Y")
          .replace("yy", "%y")
          .replace("MM", "%m")
          .replace("dd", "%d")
          .replace("HH", "%H")
          .replace("mm", "%M")
          .replace("ss", "%S")
      )
    return (
        f"FORMAT_TIMESTAMP({fmt_literal}, TIMESTAMP_SECONDS(CAST({ts_expr} AS"
        " INT64)))"
    )

  result = re.sub(
      r"FROM_UNIXTIME\s*\(\s*([^,]+)\s*,\s*('[^']+')\s*\)",
      _replace_from_unixtime,
      result,
      flags=re.IGNORECASE,
  )
  range_rules = [
      (r"(\d+)\s*\*\s*(\d+)", lambda m: (0, int(m[1]) * int(m[2]))),
      (r"(\d+)", lambda m: (0, int(m[1]))),
      (r"(\d+)\s*,\s*(\d+)", lambda m: (int(m[1]), int(m[2]))),
  ]
  # The lookbehind skips qualified names such as `db.range(10)`, which would
  # otherwise become the invalid `db.(SELECT ...)`.
  for args, bounds in range_rules:
    result = re.sub(
        rf"(?<![.\w])RANGE\s*\(\s*{args}\s*\)",
        lambda m, bounds=bounds: range_to_googlesql(*bounds(m)) or m[0],
        result,
        flags=re.IGNORECASE,
    )
  result = re.sub(
      r"\bCAST\s*\(\s*([^)]+?)\s+AS\s+INT\s*\)",
      r"CAST(\1 AS INT64)",
      result,
      flags=re.IGNORECASE,
  )
  result = re.sub(
      r"\bcurrent_user\s*\(\s*\)",
      "SESSION_USER()",
      result,
      flags=re.IGNORECASE,
  )
  # Assumes a Spark, Databricks, or Hive source, where current_database() and
  # current_schema() both name the schema (a BigQuery dataset). BigQuery has no
  # CURRENT_SCHEMA(); @@dataset_id is the job's default dataset, or NULL if the
  # job sets none. In Snowflake, Redshift, and PostgreSQL, CURRENT_DATABASE()
  # is the BigQuery project instead.
  result = re.sub(
      r"\bcurrent_(?:database|schema)\s*\(\s*\)",
      "@@dataset_id",
      result,
      flags=re.IGNORECASE,
  )
  return result


def _validate_directory_safety(
    source_dir: str, target_dir: str, label: str
) -> None:
  """Ensures staging/output directories do not overlap with source_dir."""
  real_src = os.path.realpath(source_dir)
  real_target = os.path.realpath(target_dir)
  if (
      real_src == real_target
      or real_target.startswith(real_src + os.sep)
      or real_src.startswith(real_target + os.sep)
  ):
    raise ValueError(
        f"Unsafe {label} directory '{target_dir}': must not be equal to or"
        f" overlap with source directory '{source_dir}'."
    )


def preprocess(
    source_dir: str,
    staging_dir: str,
    manifest_path: str,
    gcs_input_uri: Optional[str],
) -> None:
  """Step 1: Walk codebase, extract embedded SQL via AST, and stage files."""
  print("==================================================")
  print("STEP 1: AST PREPROCESSING & SQL EXTRACTION")
  print("==================================================")

  _validate_directory_safety(source_dir, staging_dir, "staging")

  if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)
  os.makedirs(staging_dir, exist_ok=True)

  manifest: list[dict[str, Any]] = []
  all_discovered_views: list[dict[str, Any]] = []
  total_files = 0

  for root, _, files in os.walk(source_dir):
    for file in files:
      if file.endswith(".py"):
        total_files += 1
        full_path = os.path.join(root, file)
        relative_path = os.path.relpath(full_path, source_dir)

        try:
          with open(full_path, "r", encoding="utf-8") as f:
            source = f.read()

          tree = ast.parse(source, filename=full_path)
          extractor = SQLExtractor(full_path, relative_path)
          extractor.visit(tree)

          all_discovered_views.extend(extractor.discovered_views)

          for item in extractor.extracted_queries:
            manifest.append(item)
            sql_filename = f"{item['query_id']}.sql"
            sql_file_path = os.path.join(staging_dir, sql_filename)
            item["staged_sql_file"] = sql_filename

            frag_type = item.get("fragment_type", "statement")
            masked_sql, placeholder_map = mask_sql_placeholders(
                item["original_sql"]
            )
            item["placeholder_map"] = placeholder_map
            staged_sql = wrap_fragment_for_staging(masked_sql, frag_type)

            with open(sql_file_path, "w", encoding="utf-8") as sf:
              sf.write(staged_sql + "\n")

        except Exception as e:  # pylint: disable=broad-exception-caught
          print(f"Warning: Could not parse {relative_path}: {e}")

  # Cross-reference extracted queries against non-SQL DataFrame views
  view_names = {v["view_name"] for v in all_discovered_views}
  for item in manifest:
    sql_text = item["original_sql"]
    refs = [
        vn for vn in view_names if re.search(rf"\b{re.escape(vn)}\b", sql_text)
    ]
    item["referenced_dataframe_views"] = refs

  # Generate relation stub DDLs for non-SQL DataFrame views so BigQuery
  # Migration Service (BQMS) can resolve the relation name across any source
  # dialect without triggering RelationNotFound on a nonexistent upstream table.
  for view_info in all_discovered_views:
    vn = view_info["view_name"]
    inferred_cols: list[str] = []
    for item in manifest:
      for col in re.findall(
          rf"\b{re.escape(vn)}\.([A-Za-z_]\w*)\b",
          item["original_sql"],
          re.IGNORECASE,
      ):
        if col.lower() not in {c.lower() for c in inferred_cols}:
          inferred_cols.append(col)
    col_defs = (
        ", ".join(f"{c} VARCHAR(255)" for c in inferred_cols)
        if inferred_cols
        else "id INT"
    )
    stub_file = f"_dataframe_view_{vn}.sql"
    stub_path = os.path.join(staging_dir, stub_file)
    with open(stub_path, "w", encoding="utf-8") as sf:
      sf.write(
          f"-- Auto-generated DDL stub for non-SQL DataFrame relation: {vn}\n"
          f"CREATE TABLE {vn} ({col_defs});\n"
      )

  manifest_output = {
      "queries": manifest,
      "discovered_dataframe_views": all_discovered_views,
  }

  with open(manifest_path, "w", encoding="utf-8") as mf:
    json.dump(manifest_output, mf, indent=2)

  print(f"Scanned {total_files} files.")
  print(f"Extracted {len(manifest)} embedded SQL queries/fragments.")
  print(f"Discovered {len(all_discovered_views)} non-SQL DataFrame views.")
  print(f"Manifest written to: {manifest_path}")
  print(f"Staged SQL files written to: {staging_dir}")

  if gcs_input_uri:
    print("\nUploading staged SQL files to Cloud Storage...")
    gcs_target = (
        gcs_input_uri if gcs_input_uri.endswith("/") else f"{gcs_input_uri}/"
    )
    staged_files = sorted(glob.glob(os.path.join(staging_dir, "*")))
    if staged_files:
      cmd = ["gcloud", "storage", "cp"] + staged_files + [gcs_target]
      result = subprocess.run(cmd, capture_output=True, text=True, check=False)
      if result.returncode != 0:
        print(f"GCS upload error: {result.stderr}")
        sys.exit(1)
      print(f"Successfully uploaded staged files to {gcs_target}\n")
    else:
      print("No staged SQL files found to upload.\n")


def postprocess(
    source_dir: str,
    output_dir: str,
    translated_dir: str,
    manifest_path: str,
    force: bool = False,
    enable_fallback_rules: bool = False,
) -> None:
  """Step 3: Read translated SQL, map queries via manifest, and re-inject."""
  print("==================================================")
  print("STEP 3: POSTPROCESSING & AST RE-INJECTION")
  print("==================================================")

  _validate_directory_safety(source_dir, output_dir, "output")

  if not os.path.exists(manifest_path):
    print(f"Error: Manifest file {manifest_path} not found!")
    sys.exit(1)

  with open(manifest_path, "r", encoding="utf-8") as mf:
    raw_manifest = json.load(mf)

  if isinstance(raw_manifest, dict):
    manifest = raw_manifest.get("queries", [])
  else:
    manifest = raw_manifest

  if os.path.exists(output_dir):
    if os.listdir(output_dir) and not force:
      raise FileExistsError(
          f"Output directory '{output_dir}' already exists and is non-empty."
          " Pass --force (or force=True) to overwrite."
      )
    shutil.rmtree(output_dir)

  sql_dir = os.path.join(translated_dir, "sql")
  search_dir = sql_dir if os.path.exists(sql_dir) else translated_dir

  translated_map: dict[str, str] = {}

  if os.path.exists(search_dir):
    for root, _, files in os.walk(search_dir):
      for file in files:
        if file.endswith(".sql") and not file.startswith("_dataframe_view_"):
          query_id = os.path.splitext(file)[0]
          file_path = os.path.join(root, file)
          with open(file_path, "r", encoding="utf-8") as sf:
            raw_content = sf.read().strip()

          if (
              raw_content.startswith("-- ERROR")
              or "ERROR:" in raw_content[:100]
          ):
            continue

          lines = raw_content.splitlines()
          start_idx = 0
          while start_idx < len(lines) and (
              not lines[start_idx].strip()
              or lines[start_idx].strip().startswith("--")
          ):
            start_idx += 1
          translated_sql = "\n".join(lines[start_idx:]).strip()
          translated_map[query_id] = translated_sql

  queries_by_file: dict[str, list[dict[str, Any]]] = {}
  for item in manifest:
    file_rel_path = item.get("relative_path") or item.get("rel_path", "")
    queries_by_file.setdefault(file_rel_path, []).append(item)

  total_migrated = 0
  total_substituted = 0

  for root, _, files in os.walk(source_dir):
    for file in files:
      full_src_path = os.path.join(root, file)
      relative_path = os.path.relpath(full_src_path, source_dir)
      dest_path = os.path.join(output_dir, relative_path)
      os.makedirs(os.path.dirname(dest_path), exist_ok=True)

      if file.endswith(".py"):
        with open(full_src_path, "r", encoding="utf-8") as f:
          content = f.read()

        modified_content = content

        if relative_path in queries_by_file:
          # Sort queries bottom-up and right-to-left to prevent overlapping
          # string replacements from invalidating earlier AST spans.
          sorted_queries = sorted(
              queries_by_file[relative_path],
              key=lambda q: (
                  q.get("line_number", 0),
                  q.get("col_offset", 0),
              ),
              reverse=True,
          )
          for query_info in sorted_queries:
            qid = query_info["query_id"]
            original_sql = query_info["original_sql"]
            frag_type = query_info.get("fragment_type", "statement")
            line_no = query_info.get("line_number")
            col_off = query_info.get("col_offset")
            end_line_no = query_info.get("end_lineno")
            end_col_off = query_info.get("end_col_offset")
            placeholder_map = query_info.get("placeholder_map")

            if qid in translated_map and translated_map[qid]:
              unwrapped = unwrap_fragment_after_translation(
                  translated_map[qid], frag_type
              )
              if unwrapped is None:
                print(
                    "Warning: Could not unwrap translated SQL fragment for"
                    f" query '{qid}' ({relative_path}:{line_no}); skipping"
                    " re-injection."
                )
                continue
              restored = restore_sql_placeholders(unwrapped, placeholder_map)
              new_content = safe_reinject_into_python(
                  modified_content,
                  original_sql,
                  restored,
                  line_number=line_no,
                  col_offset=col_off,
                  end_lineno=end_line_no,
                  end_col_offset=end_col_off,
              )
              if new_content != modified_content:
                modified_content = new_content
                total_substituted += 1
              elif restored != original_sql:
                print(
                    "Warning: Could not locate original SQL literal for"
                    f" query '{qid}' ({relative_path}:{line_no}); skipping"
                    " re-injection."
                )
            else:
              print(
                  "Warning: Missing clean BigQuery Migration Service (BQMS)"
                  f" translation for query '{qid}' ({relative_path}:{line_no})."
              )
              if enable_fallback_rules:
                fallback_sql = apply_fallback_rules(original_sql)
                if fallback_sql != original_sql:
                  new_content = safe_reinject_into_python(
                      modified_content,
                      original_sql,
                      fallback_sql,
                      line_number=line_no,
                      col_offset=col_off,
                      end_lineno=end_line_no,
                      end_col_offset=end_col_off,
                  )
                  if new_content != modified_content:
                    modified_content = new_content
                    total_substituted += 1

        with open(dest_path, "w", encoding="utf-8") as df:
          df.write(modified_content)

        total_migrated += 1
      else:
        shutil.copy2(full_src_path, dest_path)

  print(f"Successfully migrated {total_migrated} Python files.")
  print(f"Re-injected {total_substituted} translated SQL queries into files.")
  print(f"Migrated codebase saved to: {output_dir}\n")


def main() -> None:
  parser = argparse.ArgumentParser(
      description=(
          "Automated Python Codebase AST Migration Tool for Embedded SQL"
      )
  )
  parser.add_argument(
      "--preprocess",
      action="store_true",
      help="Run Step 1 (AST SQL extraction and staging)",
  )
  parser.add_argument(
      "--postprocess",
      action="store_true",
      help="Run Step 3 (Re-inject translated SQL into target codebase)",
  )
  parser.add_argument(
      "--src",
      dest="source_dir",
      required=True,
      help="Path to source Python codebase directory to scan or migrate.",
  )
  parser.add_argument(
      "--out",
      dest="output_dir",
      default="./output/python",
      help=(
          "Output directory for the migrated codebase (default:"
          " ./output/python)."
      ),
  )
  parser.add_argument(
      "--staging",
      dest="staging_dir",
      default="./staging_input",
      help=(
          "Staging directory to store extracted .sql files (default:"
          " ./staging_input)."
      ),
  )
  parser.add_argument(
      "--staging-out",
      dest="translated_dir",
      default="./staging_output",
      help=(
          "Directory containing translated .sql files from BigQuery Migration"
          " Service (BQMS) (default: ./staging_output)."
      ),
  )
  parser.add_argument(
      "--manifest",
      default="./manifest.json",
      help=(
          "Path to the query extraction manifest JSON file (default:"
          " ./manifest.json)."
      ),
  )
  parser.add_argument(
      "--gcs-input",
      help=(
          "Optional Cloud Storage URI for uploading staged SQL files (e.g."
          " gs://my-bucket/input/)."
      ),
  )
  parser.add_argument(
      "--force",
      action="store_true",
      help="Overwrite non-empty output directory during --postprocess.",
  )
  parser.add_argument(
      "--enable-fallback-rules",
      action="store_true",
      help=(
          "Apply heuristic regex fallback rules when a query has no clean"
          " BigQuery Migration Service (BQMS) translation."
      ),
  )

  args = parser.parse_args()

  if args.preprocess:
    preprocess(args.source_dir, args.staging_dir, args.manifest, args.gcs_input)
  elif args.postprocess:
    postprocess(
        args.source_dir,
        args.output_dir,
        args.translated_dir,
        args.manifest,
        force=args.force,
        enable_fallback_rules=args.enable_fallback_rules,
    )
  else:
    parser.print_help()


if __name__ == "__main__":
  main()
