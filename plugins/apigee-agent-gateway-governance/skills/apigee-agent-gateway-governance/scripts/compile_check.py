#!/usr/bin/env python3
"""Compile an AFT template offline and assert the ext-proc invariants.

No Apigee org, no network, no deploy. Replicates exactly what
`gcloud apigee apis import --from-template` does locally: load the template,
load every feature it names from the same directory, compile with an EMPTY
caller-parameter map, and convert to a bundle.

  python3 compile_check.py ../assets/apigee-proxy-template.yaml

Exits non-zero if an invariant fails. Checks:
  1. the proxy is no-route      -- a RouteRule with no TargetEndpoint
  2. no targets are declared
  3. at most one <PreFlow> and one <PostFlow> per endpoint
     (AFT emits one element per Flow entry; two Flows both named PreFlow
     produce two sibling <PreFlow> elements, which is not valid ProxyEndpoint
     XML -- put response-phase steps in PostFlow/Response instead)
  4. no unsubstituted {MACRO} survives into the bundle
"""

import io
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

try:
  import yaml
except ModuleNotFoundError:
  # The usual cause is running this with an interpreter that happens not to
  # carry PyYAML, which is common and says nothing about the install being
  # wrong. Name the interpreter in the message so the fix is unambiguous --
  # a bare traceback sends people looking for a problem with the script.
  sys.exit(
      "error: PyYAML is not available to this interpreter.\n"
      f"       interpreter: {sys.executable}\n"
      "       Install it (pip install pyyaml) or re-run with a Python 3\n"
      "       that already has it. The gcloud SDK's bundled interpreter does\n"
      "       not, and the SDK's vendored 'yaml' is Python 2 -- do not use it."
  )

# The AFT compiler ships inside the gcloud SDK rather than on PyPI, so import it
# from the SDK install. Set CLOUDSDK_ROOT_DIR to override the search.
_CANDIDATES = [
    os.path.join(os.environ["CLOUDSDK_ROOT_DIR"], "lib")
    if os.environ.get("CLOUDSDK_ROOT_DIR")
    else "",
    "/usr/lib/google-cloud-sdk/lib",
    os.path.expanduser("~/google-cloud-sdk/lib"),
]
for _p in _CANDIDATES:
  if _p and os.path.isdir(_p):
    # third_party first: the SDK vendors its own deps (dateutil and friends)
    # and importing googlecloudsdk without them fails.
    sys.path.insert(0, os.path.join(_p, "third_party"))
    sys.path.insert(0, _p)
    break
else:
  sys.exit(
      "error: could not find the gcloud SDK's python libraries.\n       Install"
      " the Google Cloud SDK (>= 588.0.0), or set CLOUDSDK_ROOT_DIR\n       to"
      " its install directory."
  )

from googlecloudsdk.command_lib.apigee.aft import compiler  # noqa: E402
from googlecloudsdk.command_lib.apigee.aft import converter  # noqa: E402
from googlecloudsdk.command_lib.apigee.aft import models  # noqa: E402

# Apigee message templates also use {}, so only flag names that look like AFT
# parameters: SCREAMING_SNAKE_CASE with no dots.
_MACRO = re.compile(r"\{([A-Z][A-Z0-9_]*)\}")

# A value safe to drop into a sed pattern unescaped. Deliberately narrow:
# anything with a quote, space, paren or regex metacharacter gets prose.
_SIMPLE_SCALAR = re.compile(r"[A-Za-z0-9._-]+")


def compile_template(path):
  root = os.path.dirname(os.path.abspath(path))
  with open(path) as fh:
    template = models.from_dict(models.Template, yaml.safe_load(fh))
  features = []
  for name in template.features:
    with open(os.path.join(root, name)) as fh:
      features.append(models.from_dict(models.Feature, yaml.safe_load(fh)))
  return template, compiler.ApigeeCompiler().compile(template, features, {})


def parameter_drift(path, template):
  """Template-declared parameters are INERT for features. Report the drift.

  `gcloud apigee apis import --from-template` invokes the compiler with an
  EMPTY caller-parameter map, so every feature resolves its own declared
  default and the template's declaration of the same name is never consulted.
  Editing a default in the template therefore changes nothing, silently, and
  the compile still succeeds -- the macro resolves, just to the other value.

  This was hit for real: MA_CONTINUE_ON_ERROR was set to "true" (DRY_RUN) in
  the template, the feature kept "false", and the bundle came out ENFORCE on
  a fail-closed Model Armor policy. Nothing in the output said so.

  Two findings, different severities:
    MISMATCH -- a feature declares the same name with a DIFFERENT default.
                The feature wins. This is the dangerous one: someone edited
                the template expecting an effect and got none.
    INERT    -- no feature declares it at all, so the parameter does nothing
                anywhere. Usually a leftover, occasionally a typo in a name.
  """
  root = os.path.dirname(os.path.abspath(path))
  tmpl_defaults = {
      p.name: getattr(p, "default", None) for p in template.parameters
  }
  feature_defaults = {}  # name -> {feature_file: default}
  for fname in template.features:
    with open(os.path.join(root, fname)) as fh:
      feat = models.from_dict(models.Feature, yaml.safe_load(fh))
    for fp in feat.parameters or []:
      feature_defaults.setdefault(fp.name, {})[fname] = getattr(
          fp, "default", None
      )

  mismatches, inert = [], []
  for name, tdefault in tmpl_defaults.items():
    holders = feature_defaults.get(name)
    if not holders:
      inert.append(name)
      continue
    differing = {f: d for f, d in holders.items() if d != tdefault}
    if differing:
      mismatches.append((name, tdefault, differing))
  return mismatches, inert


def check(path):
  template, proxy = compile_template(path)
  failures = []

  mismatches, inert = parameter_drift(path, template)
  root = os.path.dirname(os.path.abspath(path))
  for name, tdefault, differing in mismatches:
    where = "; ".join(f"{f} has {d!r}" for f, d in sorted(differing.items()))

    # Print the exact remedy, not just the diagnosis. Reconciling one
    # number across a template and two features is the most common edit
    # this check blocks, and leaving the operator to work out which file
    # and which direction is where the drift gets re-introduced -- the
    # feature value is the one that compiles, so the template is almost
    # always the side that moves.
    #
    # The pattern tolerates optional quotes because YAML scalars are
    # written `default: "10000"` here while the parsed value is bare, and
    # a sed that matches neither silently succeeds -- worse than printing
    # nothing. Values carrying regex or quote characters (LLM_URI_MATCH)
    # get prose instead of a command that might corrupt the file.
    def _remedy(fname, cur):
      target = os.path.join(root, fname)
      if _SIMPLE_SCALAR.fullmatch(str(cur)) and _SIMPLE_SCALAR.fullmatch(
          str(tdefault)
      ):
        return (
            f'      sed -i -E "s|(^[[:space:]]*default: )[\\"\']?{cur}[\\"\']?'
            f'[[:space:]]*$|\\1\\"{tdefault}\\"|" {target}'
        )
      return (
          f"      edit {target}: set {name} default to {tdefault!r} (value"
          " needs quoting care)"
      )

    fixes = "\n".join(_remedy(f, d) for f, d in sorted(differing.items()))
    failures.append(
        f"parameter {name}: the template declares {tdefault!r} but {where}. "
        "The FEATURE value is what compiles -- the template's is inert, "
        "because gcloud passes an empty caller-parameter map.\n"
        f"    To make the features match the template:\n{fixes}\n"
        "    To keep the feature value instead, change the template's "
        f"declaration of {name} to {sorted(differing.values())[0]!r}."
    )

  if proxy.targets:
    failures.append(
        f"expected no targets, got {[t.name for t in proxy.targets]}"
    )

  for ep in proxy.endpoints:
    routed = [r.name for r in ep.routes if r.target is not None]
    if routed:
      failures.append(f"endpoint {ep.name}: routes with a target: {routed}")
    if not ep.routes:
      failures.append(f"endpoint {ep.name}: no RouteRule at all")
    for tag in ("PreFlow", "PostFlow"):
      n = sum(1 for f in ep.flows if f.name == tag)
      if n > 1:
        failures.append(
            f"endpoint {ep.name}: {n} flows named {tag}; the converter "
            f"emits one <{tag}> element each, which is invalid. Move "
            "response-phase steps to PostFlow/Response."
        )

  bundle = converter.proxy_to_bundle(proxy)
  zf = zipfile.ZipFile(io.BytesIO(bundle))
  declared = {p.name for p in template.parameters}
  for entry in zf.namelist():
    if not entry.endswith((".xml", ".js", ".properties")):
      continue
    for macro in set(_MACRO.findall(zf.read(entry).decode("utf-8", "replace"))):
      if macro in declared:
        failures.append(
            f"{entry}: {{{macro}}} was not substituted. Template "
            "parameters are replaced in FEATURE content only -- the "
            "template's own fields are copied verbatim."
        )

  # Structural parse of the emitted ProxyEndpoint.
  for entry in zf.namelist():
    if "/proxies/" in entry:
      el = ET.fromstring(zf.read(entry))
      for tag in ("PreFlow", "PostFlow"):
        if len(el.findall(tag)) > 1:
          failures.append(f"{entry}: multiple <{tag}> elements")
      for rule in el.findall("RouteRule"):
        if rule.find("TargetEndpoint") is not None:
          failures.append(f"{entry}: RouteRule has a TargetEndpoint")

  print(f"template : {template.name}")
  print(f"policies : {len(proxy.policies)}  resources: {len(proxy.resources)}")
  print(f"bundle   : {len(zf.namelist())} entries")
  if inert:
    print(
        "WARNING  : template parameters no feature reads, so they do nothing: "
        + ", ".join(sorted(inert))
    )
  for ep in proxy.endpoints:
    for f in ep.flows:
      print(f"  {f.name}/{f.mode}: {[s.name for s in f.steps]}")

  if failures:
    print("\nFAIL")
    for f in failures:
      print(f"  - {f}")
    return 1
  print(
      "\nOK: no-route, no targets, single PreFlow/PostFlow, all macros resolved"
  )
  return 0


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(2)
  sys.exit(check(sys.argv[1]))
