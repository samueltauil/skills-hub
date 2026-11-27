# Snowflake translation gotchas reference

Optimizes Snowflake SQL translation to BigQuery (GoogleSQL) and addresses common
dialect differences.

**Official Documentation**: For the complete list of Snowflake SQL translation
rules, see [Snowflake to BigQuery translation reference][snowflake_ref].

## Table of Contents

-   [1. Template Variables (`&VAR` / `${VAR}`)](#1-template-variables-var-var)
    (lines 29–47)
-   [2. Multi-Statement Files / USE Statements](#2-multi-statement-files-use-statements)
    (lines 51–74)
-   [3. Metadata Files (.zip vs DDL SQL)](#3-metadata-files-zip-vs-ddl-sql)
    (lines 78–89)
-   [4. Lateral Joins and FLATTEN](#4-lateral-joins-and-flatten) (lines 93–103)
-   [5. Streams and Change Data Capture (CDC)](#5-streams-and-change-data-capture-cdc)
    (lines 107–114)
-   [6. Schema Search Path / Database Redirection](#6-schema-search-path-database-redirection)
    (lines 118–148)
-   [7. EXECUTE IMMEDIATE Dynamic SQL](#7-execute-immediate-dynamic-sql) (lines
    152–165)
-   [8. Stored Procedures (JavaScript / Snowflake Scripting)](#8-stored-procedures-javascript-snowflake-scripting)
    (lines 169–182)

--------------------------------------------------------------------------------

## 1. Template Variables (`&VAR` / `${VAR}`)

Snowflake SQL scripts often use session parameters or deployment template
variables like `&MY_VAR` or `${MY_VAR}`.

-   **The Problem**: BigQuery Migration Service (BQMS) parses `&` or `$` as
    invalid syntax, resulting in `SyntaxError` or `LexicalError`.
-   **Baseline Translation First**: Send raw files to BigQuery Migration Service
    (BQMS) first. If the variables are inside standard string literals or static
    SQL comments, BigQuery Migration Service (BQMS) may process them without
    issue.
-   **Error-Driven Fix**: If translation fails:
    1.  Inspect `translation_report.csv` to identify the failing lines.
    2.  Write a custom Python script (e.g., `preprocess_templates.py`) to mask
        `&VAR` or `${VAR}` with a valid SQL identifier format (e.g.,
        `TMPL_VAR_1`) and re-translate.
-   **Post-processing**: After achieving a clean translation, write a custom
    script or use tools to restore the original templates in the translated
    BigQuery output.

--------------------------------------------------------------------------------

## 2. Multi-Statement Files / USE Statements

Snowflake scripts often contain `USE DATABASE db;` or `USE SCHEMA schema;`
statements.

-   **The Problem**: BigQuery does not support `USE` statements. BigQuery
    Migration Service (BQMS) might ignore them or throw warnings, causing
    subsequent table references without qualifiers to fail with
    `RelationNotFound`.
-   **Baseline Translation First**: Test the batch translation with default
    settings first.
-   **Error-Driven YAML Configuration**: If `RelationNotFound` errors appear in
    the report:
    1.  Create an `environment.config.yaml` specifying default database and
        schema search paths.
    2.  Include `environment.config.yaml` in your BigQuery Migration Service
        (BQMS) batch input.

```yaml
type: environment
session:
  defaultDatabase: MY_DEFAULT_DB
  schemaSearchPath: [SCHEMA1, SCHEMA2]
```

--------------------------------------------------------------------------------

## 3. Metadata Files (.zip vs DDL SQL)

When extracting metadata from Snowflake:

-   **DO NOT** upload multiple unzipped metadata DDL `.sql` files directly into
    the input folder alongside queries if you are also supplying a metadata
    `.zip` package.
-   If using the official BigQuery Migration Service (BQMS) metadata extractor
    tool, compress the JSON/YAML outputs into a single `metadata.zip` file and
    pass its Cloud Storage path to `metadataFilePaths`.
-   If you manually authored mock `CREATE TABLE` DDLs, leave them as plain
    `.sql` files inside `sourceBaseUri`.

--------------------------------------------------------------------------------

## 4. Lateral Joins and FLATTEN

Snowflake `LATERAL FLATTEN(input => ...)` constructs translate to BigQuery's
`UNNEST` operator.

-   **Gotcha**: BigQuery Migration Service (BQMS) automatically converts most
    `FLATTEN` calls to `UNNEST(JSON_EXTRACT_ARRAY(...))`.
-   **Verification**: Ensure that target BigQuery JSON paths match the unnested
    array structure. If BigQuery Migration Service (BQMS) leaves `FLATTEN`
    un-translated, manually rewrite the clause using BigQuery's `UNNEST` and
    `JSON_QUERY_ARRAY` functions.

--------------------------------------------------------------------------------

## 5. Streams and Change Data Capture (CDC)

Snowflake `STREAM` objects and `CHANGES(INFORMATION => ...)` clauses do not have
direct equivalents in GoogleSQL.

-   **Action**: Mask or extract `CHANGES` clauses during iteration, or rewrite
    the pipeline to use BigQuery Change Data Capture (CDC) with `MERGE`
    statements or Datastream.

--------------------------------------------------------------------------------

## 6. Schema Search Path / Database Redirection

In Snowflake, unqualified object names resolve using the current session's `USE
DATABASE` and `USE SCHEMA`. BigQuery requires fully qualified table names
(`project.dataset.table`).

-   **Action**: Use `experimental_object_rewriter` in a BigQuery Migration
    Service (BQMS) configuration YAML file to map Snowflake database and schema
    pairs to BigQuery project and dataset pairs:

```yaml
type: experimental_object_rewriter
relation:
  - match:
      database: "SNOWFLAKE_PROD"
      schema: "ANALYTICS"
    outputName:
      database: "my-gcp-project-id"
      schema: "bq_analytics"
      relation: "${relation}"
```

-   **Search Path Fallback**: If full qualifications are unavailable, use
    `environment.config.yaml`:

```yaml
type: environment
session:
  defaultDatabase: "MIGRATION_DB"
  schemaSearchPath: ["PUBLIC", "RAW_POS"]
```

--------------------------------------------------------------------------------

## 7. EXECUTE IMMEDIATE Dynamic SQL

BigQuery Migration Service (BQMS) cannot evaluate `EXECUTE IMMEDIATE` statements
dynamically at compile time if they use string concatenation or external
variables. This causes `ExecuteImmediateStatementNotYetImplementedError` or
`LexicalError`.

### Pattern: Error-Driven Static Evaluation

-   **Action**: If translation fails due to dynamic SQL compile errors, write a
    custom Python script (e.g., `fix_dynamic_sql.py`) to parse the source files
    and replace the offending dynamic `EXECUTE IMMEDIATE` blocks with their
    statically evaluated equivalent statements (e.g., `INSERT`, `MERGE`), then
    re-translate.

--------------------------------------------------------------------------------

## 8. Stored Procedures (JavaScript / Snowflake Scripting)

Snowflake stored procedures written in JavaScript or Snowflake Scripting (PL/SQL
style loops, `VAR`, `LET`) cannot be transpiled automatically if they mix
procedural control flow with dynamic SQL generation.

-   **Symptom**: `UnsupportedFeatureError` with message `Unsupported SQL` or
    `FeatureNotYetImplementedError` (for procedural loops or cursors).
-   **Resolution Workflow**:
    1.  Extract the embedded SQL queries from the procedural wrapper.
    2.  Translate the raw SQL statements using BigQuery Migration Service
        (BQMS).
    3.  Convert procedural control flow to BigQuery Procedural Language (`CREATE
        PROCEDURE` with `LOOP`, `WHILE`, `IF...ELSE`).

[snowflake_ref]: https://cloud.google.com/bigquery/docs/migration/snowflake-sql
