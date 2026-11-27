# Teradata translation gotchas reference

Optimizes Teradata SQL translation to GoogleSQL (BigQuery) and addresses common
dialect differences.

**Official Documentation**: For the complete list of Teradata SQL translation
differences, see the [Teradata SQL translation guide][teradata_guide].

## 1. SET vs MULTISET tables

-   **Teradata Behavior**: Teradata supports `SET` tables which automatically
    enforce uniqueness by rejecting duplicate rows.
-   **BigQuery Behavior**: BigQuery only supports `MULTISET` behavior (allows
    duplicates). BigQuery Migration Service (BQMS) translates `SET` tables to
    standard BigQuery tables without uniqueness enforcement.
-   **Optimization**:
    -   Flag any `SET` tables to the user and warn them that uniqueness will not
        be enforced.
    -   If uniqueness is critical, propose a deduplication query structure
        (e.g., using `ROW_NUMBER()` or a `MERGE` statement) for their target
        ingestion pipeline.

## 2. SAMPLE clause

-   **Teradata Behavior**: Teradata uses `SAMPLE N` to return N random rows.
-   **BigQuery Behavior**: BigQuery Migration Service (BQMS) translates `SAMPLE
    N` to `ORDER BY rand() LIMIT N`.
-   **Performance Impact**: `ORDER BY rand()` forces BigQuery to perform a full
    table scan and global sort, which is extremely expensive on large tables.
-   **Optimization**:
    -   Suggest replacing `SAMPLE N` with `TABLESAMPLE SYSTEM (N PERCENT)` if an
        exact row count is not required (this is much faster as it avoids full
        scans).
    -   If a specific number of rows is needed, suggest pre-filtering or using a
        partitioned/clustered column to limit the scan.

## 3. Indexes (UPI, USI, NUPI, NUSI)

-   **Teradata Behavior**: Teradata relies heavily on primary and secondary
    indexes for data distribution and query performance.
-   **BigQuery Behavior**: BigQuery does not support indexes. BigQuery Migration
    Service (BQMS) ignores Teradata index definitions during DDL translation.
-   **Optimization**:
    -   Guide the user to configure **Partitioning** and **Clustering** in
        BigQuery to replace Teradata indexes.
    -   Suggest partitioning by date/time columns that are frequently used in
        filters.
    -   Suggest clustering by high-cardinality columns frequently used in joins
        or filters (similar to Teradata Secondary Indexes).

[teradata_guide]: https://cloud.google.com/bigquery/docs/migration/teradata-sql
