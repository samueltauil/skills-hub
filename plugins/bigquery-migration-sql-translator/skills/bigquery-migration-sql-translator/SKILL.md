---
name: bigquery-migration-sql-translator
metadata:
  version: "1.0.2"
  category: BigDataAndAnalytics
  publisher: google
description: >-
  Translates SQL queries, DDL schemas, and stored procedures from legacy database
  dialects (Teradata, Oracle, Redshift, Snowflake, SparkSQL, HiveQL) to BigQuery
  GoogleSQL using the BigQuery Migration Service (BQMS) MCP server. Use when
  translating legacy SQL queries, migrating schemas or metadata zip archives,
  or configuring BigQuery Migration Service (BQMS) YAML translation settings.
  Don't use for executing BigQuery queries or managing datasets and tables (use
  bigquery-basics), diagnosing runtime job errors (use bigquery-troubleshooting),
  or tuning slot reservations (use bigquery-optimization).
---

# BigQuery Migration Service (BQMS) SQL Translator

The BigQuery Migration Service (BQMS) translates legacy database SQL scripts,
queries, and schemas into GoogleSQL. This skill coordinates translation
workflows, Cloud Storage staging, compiler error triage, and YAML configuration.

## Usage Attribution

**MUST READ**: Before executing any `gcloud`, REST API, or MCP command, you
MUST read and follow the instructions in
[Usage Attribution](references/attribution.md).

## Before you begin

Before translating queries or schemas, verify the following prerequisites:

1.  **Google Cloud SDK & Project Setup**: Ensure the
    [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) is installed,
    verify that your Google Cloud project has an active Cloud Billing account
    attached, and select the target project:

    ```bash
    gcloud config set project {project_id}
    ```

2.  **Enable the API**: Enable the BigQuery Migration API
    (`bigquerymigration.googleapis.com`) in your Google Cloud project:

    ```bash
    gcloud services enable bigquerymigration.googleapis.com
    ```

3.  **Required IAM Roles**: Verify that your identity or service account has:
    -   `roles/mcp.toolUser` (MCP Tool User)
    -   `roles/bigquerymigration.editor` (Migration Workflow Editor)
    -   For batch translation, `roles/storage.objectViewer` and
        `roles/storage.objectCreator` (or `roles/storage.objectAdmin`) on the
        Cloud Storage buckets that hold the input and output files.
4.  **MCP Server Connection**: If BigQuery Migration Service (BQMS) tools (e.g.
    `translate_query`, `translate_batch_queries`) are not present in your active
    tool list, configure the remote BigQuery Migration Service (BQMS) MCP
    server. For setup instructions across clients (Claude, Cursor, Gemini CLI,
    VS Code), see [mcp_config.md](references/mcp_config.md).
5.  **Cost & Cloud Storage Cleanup**: Review
    [Google Cloud Pricing](https://cloud.google.com/pricing) for Cloud Storage
    and BigQuery usage details. After completing a batch migration, clean up
    temporary staged input and output folders in Cloud Storage:

    ```bash
    gcloud storage rm -r gs://{bucket}/{folder}
    ```

6.  **Translation Tracking**: For batch translations, and for queries that need
    more than one translation iteration, keep a translation tracker (e.g.
    `translation_tracker.md`) to document goals, planned steps, and progress.
    After each translation, record one row with this template:

    Iteration | Status | Total Errors | Correctness Errors | Completeness Errors | Compatibility Errors | Key Actions / Transformations
    --------- | ------ | ------------ | ------------------ | ------------------- | -------------------- | -----------------------------

    A single query that translates cleanly on the first attempt needs no
    tracker: report its translation ID and logs in your response.

## Workflow Selection

Choose the workflow based on your migration scope:

-   **Interactive Translation (Single Query)**: Best for ad-hoc queries,
    exploratory testing, dialect syntax comparison, or quick error debugging.
-   **Batch Translation (Multiple Files & Cloud Storage)**: Use for more than
    one file or a directory, including SQL embedded in application code (extract
    it into `.sql` files first). For multi-file Python codebases containing
    embedded SQL, use
    [python_embedded_sql_migrator_template.py](assets/python_embedded_sql_migrator_template.py)
    to extract queries into staged files and re-inject translated SQL. Batch
    translation is faster and cheaper than translating files one by one, and it
    resolves cross-file dependencies, so it usually gives better results. Run
    `translate_batch_queries` on the staged files first; use `translate_query`
    only afterwards if needed to debug a specific statement from
    `translation_report.csv`.

## 1. Interactive Translation Workflow

Use the interactive workflow to translate a single query string, inspect
compiler logs, and iteratively resolve issues.

### Steps

1.  **Submit Query (`translate_query`)**: Call `translate_query` with
    `projectNumber`, `location`, `inputQuery`, `sourceDialect`, and
    `targetDialect` (`BigQuery`). Include optional parameters:

    -   `metadataFilePath`: Cloud Storage URI to a metadata zip file
        (`gs://.../metadata.zip`) for schema resolution.
    -   `translationConfigs`: Inline YAML configurations (e.g. object renaming,
        schema redirection, optimizer rules). Show the YAML you used in your
        response so the user can reuse it (e.g. in batch translation).

2.  **Poll Status (`get_translation`)**: If the returned `translation_state` is
    `RUNNING` or `PENDING`, poll `get_translation` using the `translation` ID,
    `projectNumber`, and `location` until `translation.state` is `SUCCEEDED` or
    `FAILED`, at the interval given in the BigQuery Migration Service (BQMS) MCP
    tool descriptions. While the job runs, do work that doesn't need the result
    (e.g. read the dialect gotchas reference).

3.  **Inspect Output & Logs**:

    -   Examine `translated_query` for the converted GoogleSQL.
    -   Review each entry in `translation_logs`: inspect `severity` (`ERROR`,
        `WARNING`), `category` (e.g. `RelationNotFound`), and `effect`
        (`CORRECTNESS`, `COMPLETENESS`, `COMPATIBILITY`).
    -   Check the SQL itself, not only the logs: BigQuery Migration Service
        (BQMS) emits `ERROR_TYPE(...)` for types it cannot map, sometimes with
        no log entry. Treat any `ERROR_TYPE` or inline error comment as an
        error, and when a BigQuery project is available, dry-run the result (`bq
        query --dry_run --use_legacy_sql=false`). A `Not found` or `must be
        qualified with a dataset` error still means the SQL is syntactically
        valid; the referenced objects just don't exist in BigQuery yet. Say so
        and move on, even if the error suggests a fix: don't stub tables or
        change the SQL or `bq` flags to get past it.
    -   A `NoSuchFunction` error means BigQuery Migration Service (BQMS) copied
        that call unchanged, sometimes with the function name in backticks.
        Treat it as untranslated even if BigQuery has a function with that name:
        a dry run that stops at missing tables doesn't check it.
    -   If the source dialect has a gotchas reference (see
        [Dialect-Specific Gotchas](#dialect-specific-gotchas)), read it and
        check the output for the patterns it lists. Some semantic differences
        produce no log entry and still pass a dry run.

4.  **Iterate Until Clean**: If the logs contain errors or warnings, the
    translated SQL contains `ERROR_TYPE` or inline error comments, the dry run
    fails, or the output matches a dialect gotcha, resolve the issues as
    described in [Resolving Translation Issues](#resolving-translation-issues)
    and re-translate.

5.  **Explain & Compare Differences (`explain_translation`)**: When requested to
    explain a translation, compare syntax differences, or understand how
    specific query logic was converted, call `explain_translation` with
    `translation` (the translation ID), `projectNumber`, and `location`. This
    returns a structured explanation of the query's purpose and a detailed
    breakdown of syntax, function, and behavioral differences between the source
    query and the translated GoogleSQL. The explanation doesn't validate the
    output, so check the translation as in step 3 rather than relying on it.

## 2. Batch Translation Workflow

Batch translation handles multiple files staged in Cloud Storage. It resolves
cross-file dependencies and produces a consolidated translation summary report
(`translation_report.csv`).

### Steps

1.  **Stage Input Files to Cloud Storage**: Upload the raw SQL files,
    configuration files (`*.config.yaml`), and any metadata file from the local
    workspace to a Cloud Storage input folder:

    ```bash
    gcloud storage cp input/*.sql gs://my-bucket/migration/input/
    gcloud storage cp *.config.yaml gs://my-bucket/migration/input/
    ```

    *Note: Do not pass configuration file paths in tool parameters if those
    files are already located inside `sourceBaseUri`.*

    Use new, empty Cloud Storage input and output folders for each run (e.g.
    with a timestamp suffix). Stage only files from the local workspace or
    generated in this run. Never reuse or copy inputs, DDL, or outputs that are
    already in a bucket from earlier runs: they may come from different inputs
    or settings.

2.  **Initiate Batch Translation**:

    -   **Translating SQL Queries (`translate_batch_queries`)**: Call
        `translate_batch_queries` with `projectNumber`, `location`,
        `sourceDialect`, `targetDialect`, `sourceBaseUri`, and `targetBaseUri`.
    -   **Translating Metadata Zip Files (`translate_metadata`)**: To aid batch
        translation by generating target BigQuery DDL schema definitions from an
        extracted database metadata zip file (`metadata.zip` from Teradata,
        Oracle, etc.), call `translate_metadata` specifying `sourceBaseUri`
        (Cloud Storage URI to `metadata.zip`) and `targetBaseUri` (destination
        Cloud Storage folder).

3.  **Poll Completion (`fetch_batch_translation`)**: Poll using the returned
    workflow ID until `translation.state` is `SUCCEEDED` or `FAILED`, at the
    interval given in the BigQuery Migration Service (BQMS) MCP tool
    descriptions.

4.  **Retrieve & Inspect Outputs**: Download the generated files from
    `translation.target_base_uri`:

    ```bash
    gcloud storage cp -r gs://my-bucket/migration/output/ ./local_output/
    ```

    Locate and inspect `report/translation_report.csv` to review all warnings,
    errors, and line-level diagnostics. Then scan the generated `.sql` files for
    `ERROR_TYPE(...)` and inline error comments, which the report can miss, and
    dry-run the generated SQL when a BigQuery project is available (handle `Not
    found` errors as in the interactive workflow). Check the output for the
    patterns in the source dialect's gotchas reference, if one exists. Resolve
    or clearly report every remaining issue; do not describe the output as clean
    until this check passes.

5.  **Iterate Until Clean**: Resolve the issues found in step 4 as described in
    [Resolving Translation Issues](#resolving-translation-issues), and re-run
    from step 1 with the changed inputs.

6.  **Post-processing (Final Step Only)**: Only after resolving every compiler
    error that re-translation can fix, execute any application-level
    post-processing (e.g. AST re-injection) to restore host source files.
    [effect_correctness.md](references/effect_correctness.md) lists the errors
    that may remain when re-injecting embedded SQL.

## Resolving Translation Issues

Both workflows resolve issues the same way:

-   Identify the **Effect** (`CORRECTNESS`, `COMPLETENESS`, `COMPATIBILITY`) of
    each issue, and resolve them in order of compiler phase dependencies:
    `CORRECTNESS` (parse errors) first, then `COMPLETENESS` (missing objects),
    then `COMPATIBILITY` (unsupported features).
-   **MUST Read the Reference Guide** for each effect in
    [Troubleshooting by Error Effect](#troubleshooting-by-error-effect) BEFORE
    applying fixes, and follow its resolution workflow.
-   Fixes can preprocess the input (e.g. prepend DDL) or post-process the
    BigQuery Migration Service (BQMS) output (e.g. a rewrite that a dialect
    gotcha calls for). Run BigQuery Migration Service (BQMS) on the preprocessed
    input rather than translating it yourself.
-   Keep the source system's dialect for every re-translation. Another dialect
    may accept the same SQL but translate it with different semantics (e.g.
    return types, numeric types, or identifier case), so don't switch dialects
    to get cleaner output.
-   Rewrites of the BigQuery Migration Service (BQMS) output, including
    optimizations the user asks for, must return the same rows as the source
    query. For example, a filter that runs after a row limit (`TOP`, `LIMIT`)
    can't be merged into the query before the limit.
-   Wait for each re-translation to finish, record its translation ID, error
    counts, and any pre- or post-processing in the tracker, and compare the
    counts with the previous iteration. Repeat until no errors remain or all
    options are exhausted.
-   Report the final SQL from the tracked iteration, the pre- and
    post-processing you applied, and any errors that remain.

## Reference Lookup Index

Use these reference guides when troubleshooting errors or authoring
configuration files:

### Troubleshooting by Error Effect

Effect          | Common Causes                                                                              | Reference Guide
:-------------- | :----------------------------------------------------------------------------------------- | :--------------
`CORRECTNESS`   | Syntax errors, unescaped literals, application script wrappers, `NoSuchFunction`.          | [effect_correctness.md](references/effect_correctness.md)
`COMPLETENESS`  | Missing tables, views, columns (`RelationNotFound`, `AttributeNotFound`), DDL suggestions. | [effect_completeness.md](references/effect_completeness.md)
`COMPATIBILITY` | Functions or features without direct GoogleSQL mapping.                                    | [effect_compatibility.md](references/effect_compatibility.md)

### Configuration & Setup Guides

Task                    | Description                                                                                                                                                                                                                                                              | Reference Guide
:---------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------
**YAML Configurations** | Database/schema redirection, name mapping, table partitioning and clustering injection, optimizer transformations, statement rewriters, and environment settings. Schemas in `assets/translation_config_schemas/` and examples in `assets/translation_config_examples/`. | [translation_yaml_config.md](references/translation_yaml_config.md)
**MCP Server Setup**    | Configuring the remote BigQuery Migration Service (BQMS) MCP server, OAuth scopes, and IAM roles.                                                                                                                                                                        | [mcp_config.md](references/mcp_config.md)

### Dialect-Specific Gotchas

Dialect       | Key Considerations                                                    | Reference Guide
:------------ | :-------------------------------------------------------------------- | :--------------
**Teradata**  | SET/MULTISET tables, `SAMPLE` clause, primary index mapping.          | [teradata_gotchas.md](references/teradata_gotchas.md)
**Oracle**    | PL/SQL procedures, `ROWNUM` emulation, outer join `(+)`, sequences.   | [oracle_gotchas.md](references/oracle_gotchas.md)
**Snowflake** | Dynamic templates, `USE` statements, metadata merging, lateral joins. | [snowflake_gotchas.md](references/snowflake_gotchas.md)
