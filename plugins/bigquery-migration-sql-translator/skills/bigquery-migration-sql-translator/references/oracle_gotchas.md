# Oracle translation gotchas reference

Optimizes Oracle SQL and PL/SQL translation to BigQuery (GoogleSQL) and
addresses syntax emulation.

**Official Documentation**: For the complete list of Oracle SQL translation
differences, see the [Oracle SQL translation guide][oracle_guide].

## 1. PL/SQL stored procedures & packages

-   **BigQuery Translation**: BigQuery Migration Service (BQMS) translates
    Oracle PL/SQL procedures, functions, and packages into BigQuery Stored
    Procedures (using BigQuery scripting).
-   **Best Practices**:
    -   Warn the user that Oracle packages are translated into individual
        BigQuery stored procedures prefixed with the package name (e.g.,
        `package_name.procedure_name` becomes
        `dataset.package_name__procedure_name`).
    -   Examine the translated code to ensure variables and parameter modes
        (`IN`, `OUT`, `INOUT`) mapped correctly to BigQuery equivalents.

## 2. ROWNUM emulation

-   **BigQuery Migration Service (BQMS) Translation**:
    -   A comparison against a constant (`ROWNUM <= 10`, `ROWNUM < 10`) becomes
        a `LIMIT` clause (`LIMIT 10`, `LIMIT 9`).
    -   A comparison against a non-constant expression (`ROWNUM <= col`) can't
        become `LIMIT`. Check the output for `ROW_NUMBER()` in a `WHERE` clause,
        which BigQuery rejects, and rewrite it with `QUALIFY` or a subquery.
    -   `ROWNUM` in a projection becomes `ROW_NUMBER() OVER ()`.
-   **Patterns to verify in the output**:
    -   **`ROWNUM` with `ORDER BY` in the same query**: Oracle applies `ROWNUM`
        before sorting, so the query returns an arbitrary set of rows, sorted.
        Keep that behavior (apply `LIMIT` in a subquery, then sort), or use
        top-N after sorting and tell the user the rows change. Dry-run the
        output: the emitted `LIMIT` placement can be invalid.
    -   **Pagination (`ROWNUM rn` over an ordered subquery)**: BigQuery doesn't
        keep subquery order, and `ROW_NUMBER()` without `ORDER BY` is
        non-deterministic ([numbering functions][bq_numbering]). Use
        `ROW_NUMBER() OVER (ORDER BY ...)` and filter on the row number, or
        `ORDER BY ... LIMIT n OFFSET m` for small offsets. Large `OFFSET` values
        sort on a single compute unit; see
        [Troubleshoot query issues][bq_troubleshoot].

## 3. Sequence emulation

-   **Oracle Behavior**: Oracle uses `SEQUENCE` objects to generate unique
    sequential numbers.
-   **BigQuery Behavior**: BigQuery does not support native sequence objects.
-   **Emulation Strategies**:
    -   Suggest using `GENERATE_UUID()` if unique identifiers are needed and
        strict sequentiality is not required.
    -   If sequential IDs are strictly required (e.g., for business logic),
        explain that they must be emulated using Spark/Dataflow during data
        load, or by using identity columns (if applicable) or a control table
        (with performance caveats).

[oracle_guide]: https://cloud.google.com/bigquery/docs/migration/oracle-sql
[bq_numbering]: https://cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions#row_number
[bq_troubleshoot]: https://cloud.google.com/bigquery/docs/troubleshoot-queries
