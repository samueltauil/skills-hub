# Effect: CORRECTNESS (Syntax & Parse Errors)

Guides the resolution of translation-time errors where the compiler failed to
parse the input SQL (e.g., syntax errors, invalid characters, dialect-specific
macros, or application code wrappers).

## Table of Contents

-   [Common Categories](#common-categories) (lines 15–26)
-   [1. Syntax, Lexical & Dialect-Specific Errors](#1-syntax-lexical-dialect-specific-errors)
    (lines 28–71)
-   [2. Application Code Wrappers & Embedded SQL (.py, .js, Stored Procedures)](#2-application-code-wrappers-embedded-sql-py-js-stored-procedures)
    (lines 73–143)

## Common Categories

-   `SyntaxError`
-   `LexicalError`
-   `ConstantError`
-   `SemanticError`
-   `FeatureNotYetImplementedError`
-   `NoSuchFunction`

**Official Documentation**: For information on how to review translation
results, see the official guide on
[reviewing translation results][review_results].

## 1. Syntax, Lexical & Dialect-Specific Errors

-   **The Problem**: The BigQuery Migration Service (BQMS) compiler failed to
    parse the input SQL. This occurs due to non-standard dialect syntax,
    unparsed custom functions, invalid character encodings, or dialect-specific
    macros/templates.
-   **The Symptom**: `SyntaxError`, `LexicalError`, `NoSuchFunction`, or
    `FeatureNotYetImplementedError` (e.g.,
    `CreateMacroStatementNotYetImplementedError` or
    `NotYetImplementedStatementError`).
-   **Resolution Workflow**:
    1.  Inspect `impacted_object` and `message` in `translation_logs` (or
        `translation_report.csv`) to locate the exact position of the syntax
        error.
    2.  Check for invalid or unescaped characters (e.g., non-printable control
        characters, unescaped quotes). If invalid characters are systemic across
        the codebase, use `global.outputName.replace` in your
        [BigQuery Migration Service (BQMS) YAML configuration][translation-yaml-config].
    3.  If the error is caused by a proprietary dialect construct or macro,
        consult the dialect-specific gotchas reference:
        -   **Snowflake**: See the [Snowflake gotchas][snowflake-gotchas] for
            `QUALIFY`, `LATERAL FLATTEN`, dynamic templates, and stored
            procedures.
        -   **Teradata**: See the [Teradata gotchas][teradata-gotchas] for
            macros, SET/MULTISET tables, `QUALIFY`, `SAMPLE`, and `INDEX`
            clauses.
        -   **Oracle**: See the [Oracle gotchas][oracle-gotchas] for PL/SQL
            packages, procedures, `(+)` join syntax, and `ROWNUM`.
    4.  If the error comes from template syntax (e.g. dbt Jinja or `${VAR}`
        variables), mask the templates with valid SQL identifiers, re-translate,
        and restore them in the final output (see the
        [Snowflake gotchas reference][snowflake-gotchas]).
    5.  Apply the recommended dialect transformation (e.g., converting macros to
        CTEs/procedures or rewriting syntax constructs) and re-translate.
    6.  If `translation_logs` reports `NoSuchFunction`, BigQuery Migration
        Service (BQMS) did not recognize the function and copied the call
        unchanged, sometimes with the name in backticks. For an
        application-defined UDF, provide its definition in metadata and
        re-translate; do not stub built-in dialect functions as UDFs. For a
        built-in function of the source dialect, rewrite only that call in the
        BigQuery Migration Service (BQMS) output to the equivalent BigQuery
        function and dry-run the rewritten call on its own with literal
        arguments, since a dry run of the full query stops at missing tables
        before checking function calls.

## 2. Application Code Wrappers & Embedded SQL (.py, .js, Stored Procedures)

-   **Symptom**: `LexicalError` (e.g., `Unknown token: #`) or `SyntaxError`
    (e.g., `Unexpected identifier 'import'/'def'`) reported in
    `translation_report.csv`.
-   **Root Cause**: BigQuery Migration Service (BQMS) expects raw SQL
    statements. Application language syntax (Python, JavaScript, etc.) wrapping
    SQL execution calls cannot be parsed directly as native SQL statements by
    BigQuery Migration Service (BQMS).
-   **Resolution Workflow**:
    1.  **Preprocessing**: For a single file with one query, extract the query
        string directly, translate it with the interactive workflow
        (`translate_query`), and update the file in place without a manifest
        script. For multi-file codebases, extract the embedded static SQL
        statements from the application script files into staged `.sql` files
        and record a mapping manifest (`manifest.json`).
        -   *Python Codebases*: Run
            `assets/python_embedded_sql_migrator_template.py` directly (`python3
            .../python_embedded_sql_migrator_template.py --preprocess --src
            <src_dir> --staging <staging_dir> --manifest <manifest.json>
            [--gcs-input <gs://...>]`). It already extracts static SQL strings,
            masks `%s`, `:name`, and `{var}` placeholders, and writes DataFrame
            view DDL stubs without needing edits for standard Python DB-API,
            Spark, or SQLAlchemy code.
        -   *Other Languages (Java/JS/Go)*: AI agents should dynamically author
            a lightweight parser script using regex or AST parsing tailored to
            the target language framework following the same manifest extraction
            pattern.
    2.  **Translate & Iterate**: Upload staged `.sql` files to Cloud Storage,
        run `translate_batch_queries`, and analyze
        `report/translation_report.csv`. Resolve any remaining schema metadata
        DDLs or dialect warnings through further iterations.
    3.  **Post-processing (FINAL STEP ONLY)**: **ONLY AFTER resolving every
        issue in `translation_report.csv` that re-translation can fix**,
        download the final BigQuery Migration Service (BQMS) BigQuery output and
        re-inject the translated queries back into the application source files,
        preserving non-SQL application code, functions, comments, and parameter
        kwargs (`query_tags=...`). The only rows that may remain in the report
        are `-- ERROR` files for Spark, Databricks, or Hive constructs that
        BigQuery Migration Service (BQMS) cannot parse and that the fallback
        rewrites below cover, and `NoSuchFunction` files whose calls you have
        already rewritten in `sql/`.
        -   *Why wait?*: Postprocessing early while translation errors are still
            present pollutes application target files with intermediate broken
            code states.
        -   *Python Codebases*: Run
            `assets/python_embedded_sql_migrator_template.py` (`--postprocess
            --src <src_dir> --staging-out <translated_dir> --out <out_dir>
            --manifest <manifest.json> [--enable-fallback-rules] [--force]`).
            Pass `--enable-fallback-rules` only when the remaining `-- ERROR`
            files are Spark, Databricks, or Hive constructs that the fallback
            rewrites cover; otherwise leave it off so those queries keep their
            source SQL and get reported.
        -   *Verify*: `postprocess` re-injects every `.sql` file in `sql/`
            except `_dataframe_view_*` DDL stubs and files that start with `--
            ERROR` or contain `ERROR:` in their first 100 characters. For the
            skipped error files, it keeps the source SQL and prints `Warning:
            Missing clean BigQuery Migration Service (BQMS) translation for
            query ...`, or—when `--enable-fallback-rules` is passed—re-injects
            regex rewrites of the source SQL for Spark, Databricks, or Hive
            constructs that BigQuery Migration Service (BQMS) could not parse
            (such as table-valued `RANGE` or `FROM_UNIXTIME` format strings;
            `current_database()` becomes `@@dataset_id`, which is `NULL` unless
            the job sets a default dataset, whereas Snowflake's or Redshift's
            `CURRENT_DATABASE()` is the BigQuery project). Because
            `NoSuchFunction` outputs in `sql/` do not start with `-- ERROR`,
            `postprocess` re-injects them from `sql/` without running
            `--enable-fallback-rules`; rewrite any `NoSuchFunction` calls in
            their `sql/*.sql` files before running `--postprocess`. Dry-run
            every re-injected statement when a BigQuery project is available,
            and fix and report any that fail.

[review_results]: https://cloud.google.com/bigquery/docs/batch-sql-translator#summary_report
[translation-yaml-config]: translation_yaml_config.md
[snowflake-gotchas]: snowflake_gotchas.md
[teradata-gotchas]: teradata_gotchas.md
[oracle-gotchas]: oracle_gotchas.md
