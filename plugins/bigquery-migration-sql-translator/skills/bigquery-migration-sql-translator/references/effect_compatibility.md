# Effect: COMPATIBILITY (unsupported features)

Guides the resolution of translation-time errors where the compiler parsed the
SQL but encountered features not supported by the target dialect or not yet
implemented in BigQuery Migration Service (BQMS).

## Common categories

-   `UnsupportedFeatureError`
-   `NoTargetSupportForFeature`

**Official Documentation**: For information on how to review translation
results, see the official guide on
[reviewing translation results][review_results].

## 1. Unsupported features & not yet implemented

These errors occur when the compiler successfully parses the SQL syntax but does
not have an automated translation rule implemented for that specific feature.

### Resolution workflow

#### 1. Identify the feature

-   Locate the error location (line/column) in the translation log or output.
-   Identify the specific function, statement, or syntax structure that is
    reported as unsupported.

#### 2. Source workaround (modify source)

-   If possible, modify the source SQL to use a different, supported syntax or
    simpler standard SQL (e.g., replacing a proprietary function).
-   Re-translate the query.

#### 3. Output patching (post-translation fix)

-   If the source cannot be modified, or if BigQuery Migration Service (BQMS)
    translates other parts successfully but leaves error placeholders (e.g., `/*
    ERROR: Unsupported ... */`), use your knowledge of both dialects to manually
    rewrite that specific block in the generated BigQuery output.
-   This is often required for complex procedural blocks or proprietary system
    functions.

--------------------------------------------------------------------------------

## 2. Dialect-specific unsupported features

For dialect-specific unsupported features or language wrappers, refer to the
single source of truth for your source database:

-   **Snowflake**: See [snowflake_gotchas.md](snowflake_gotchas.md) for
    JavaScript stored procedures, Streams, Stages, and Tags.
-   **Teradata**: See [teradata_gotchas.md](teradata_gotchas.md) for `SET`
    tables, `SAMPLE` clause, and primary/secondary indexes.
-   **Oracle**: See [oracle_gotchas.md](oracle_gotchas.md) for PL/SQL packages,
    `ROWNUM`, and `SEQUENCE` objects.

[review_results]: https://cloud.google.com/bigquery/docs/batch-sql-translator#summary_report
