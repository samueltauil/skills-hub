# Translation configuration YAML reference

Guides the configuration of various translation settings using unified BigQuery
Migration Service (BQMS) configuration YAML files.

**Official Documentation**: For the complete list of YAML options and advanced
examples, see
[Transform SQL translations using configuration YAML files][yaml_guide].

All configuration YAML files must have names ending in `.config.yaml` (e.g.,
`mapping.config.yaml`).

## Table of Contents

-   [Passing configuration files to the BigQuery Migration Service (BQMS) MCP tools](#passing-configuration-files-to-the-bigquery-migration-service-bqms-mcp-tools)
    (lines 31–48)
-   [Schemas and Reference Examples](#schemas-and-reference-examples) (lines
    52–89)
-   [1. Object rewriter](#1-object-rewriter) (lines 93–252)
-   [2. Environment configuration (`type: environment`)](#2-environment-configuration-type-environment)
    (lines 256–267)
-   [3. Metadata configuration (`type: metadata`)](#3-metadata-configuration-type-metadata)
    (lines 271–280)
-   [4. Optimizer configuration (`type: optimizer`)](#4-optimizer-configuration-type-optimizer)
    (lines 284–313)
-   [5. Statement rewriter (`type: experimental_statement_rewriter`)](#5-statement-rewriter-type-experimental_statement_rewriter)
    (lines 317–339)
-   [6. Input formats (`type: experimental_input_formats`)](#6-input-formats-type-experimental_input_formats)
    (lines 343–355)

## Passing configuration files to the BigQuery Migration Service (BQMS) MCP tools

-   **`translate_query`**: pass each file inline in `translationConfigs`, as an
    object with a `displayName` that ends in `.config.yaml` and the YAML text as
    `content`. The tool rejects a bare YAML string or a parsed YAML object.

    ```json
    "translationConfigs": [
      {
        "displayName": "optimizer.config.yaml",
        "content": "type: optimizer\ntransformations:\n  - name: DROP_TEMP_TABLE\n"
      }
    ]
    ```

-   **`translate_batch_queries`**: upload the `.config.yaml` files to the Cloud
    Storage folder in `sourceBaseUri`, next to the input SQL files. To keep them
    elsewhere, list their Cloud Storage paths in `configurationFilePaths`.

--------------------------------------------------------------------------------

## Schemas and Reference Examples

Before writing or debugging a configuration file, inspect the corresponding JSON
schema in `assets/translation_config_schemas/` and reference YAML example in
`assets/translation_config_examples/`:

-   **Root Combined Schema**:
    `assets/translation_config_schemas/transpiler_config_spec.json`
-   **Object Rewriter**:
    -   Schema: `assets/translation_config_schemas/object_rewriter.json` (or
        `experimental_object_rewriter.json`)
    -   Example:
        `assets/translation_config_examples/object_rewriter_example.yaml` (or
        `experimental_object_rewriter_example.yaml`)
-   **Environment Configuration**:
    -   Schema: `assets/translation_config_schemas/environment.json`
    -   Example: `assets/translation_config_examples/environment_example.yaml`
-   **Metadata Configuration**:
    -   Schema: `assets/translation_config_schemas/metadata.json` (or
        `experimental_metadata.json`)
    -   Example: `assets/translation_config_examples/metadata_example.yaml` (or
        `experimental_metadata_example.yaml`)
-   **Optimizer Configuration**:
    -   Schema: `assets/translation_config_schemas/optimizer.json` (or
        `experimental_optimizer.json`)
    -   Example: `assets/translation_config_examples/optimizer_example.yaml` (or
        `experimental_optimizer_example.yaml`)
-   **Statement Rewriter**:
    -   Schema: `assets/translation_config_schemas/statement_rewriter.json` (or
        `experimental_statement_rewriter.json`)
    -   Example:
        `assets/translation_config_examples/statement_rewriter_example.yaml` (or
        `experimental_statement_rewriter_example.yaml`)
-   **Input Formats**:
    -   Schema: `assets/translation_config_schemas/input_formats.json` (or
        `experimental_input_formats.json`)
    -   Example: `assets/translation_config_examples/input_formats_example.yaml`
        (or `experimental_input_formats_example.yaml`)

--------------------------------------------------------------------------------

## 1. Object rewriter

Transforms object names, types, and properties. Configured using `type:
object_rewriter` or `type: experimental_object_rewriter`.
`experimental_object_rewriter` may be required for advanced features like regex
replacements or dynamic naming.

### 1.1 Object mapping (database/schema redirection)

Redirects source database and schema references to target BigQuery projects and
datasets.

```yaml
type: experimental_object_rewriter
relation:
  - match:
      database: "SOURCE_DATABASE"
      schema: "SOURCE_SCHEMA"
    outputName:
      database: "target-gcp-project-id"
      schema: "target_bigquery_dataset"
      relation: "${relation}"
```

### 1.2 Name mapping (identifier overrides)

Renames specific tables, columns, or functions.

#### Renaming tables (relations)

```yaml
type: experimental_object_rewriter
relation:
  - match: "SOURCE_DB.SOURCE_SCHEMA.OFFENDING#TABLE"
    outputName:
      relation: "clean_table_name"
```

#### Renaming columns (attributes)

```yaml
type: experimental_object_rewriter
attribute:
  - match:
      database: "SOURCE_DB"
      schema: "SOURCE_SCHEMA"
      relation: "MY_TABLE"
      attribute: "OLD#COLUMN"
    outputName:
      attribute: "new_column_name"
```

### 1.3 Global name rules (regex & case)

Automatically clean invalid characters or change case across all objects.

```yaml
type: experimental_object_rewriter
global:
  outputName:
    # Change table names to uppercase and everything else to lowercase.
    relation:
      case: UPPERCASE
    all:
      case: LOWERCASE
      # Replace invalid characters
      replace:
        - regex: "#"
          replaceWith: "_"
        - regex: '\$'
          replaceWith: "_dollar_"
        # Replace whitespace with underscore
        - regex: '\s'
          replaceWith: "_"
```

### 1.4 Temporary tables

Transform specific relations to temporary tables.

```yaml
type: object_rewriter
relation:
  - match: "testdb.testschema.x"
    temporary: true
  - match:
      schema: tmp_schema
      relationRegex: "tmp_.*"
    temporary: true
```

### 1.5 Attribute type conversion

Override data types for specific columns.

```yaml
type: object_rewriter
attribute:
  - match:
      database: testdb
      schema: testschema
      attributeRegex: "a+"
    type:
      target: NUMERIC(10,2)
```

### 1.6 Table partitioning and clustering

Inject or modify table partitioning and clustering specifications directly in
translated BigQuery DDL.

#### Simple column partitioning

Partitions tables by date, timestamp, or datetime columns:

```yaml
type: object_rewriter
relation:
  - match: "testdb.testschema.x"
    partition:
      simple:
        add: [a]
  - match: "testdb.testschema.y"
    partition:
      simple:
        remove: [a]
```

#### Integer range bucket partitioning

Partitions tables by integer range using `RANGE_BUCKET`:

```yaml
type: object_rewriter
relation:
  - key: "testdb.testschema.mytable"
    partition:
      range_bucket:
        column: "id"
        start: 0
        end: 100
        step: 10
        options:
          require_partition_filter: "TRUE"
```

#### Table clustering

Clusters tables by up to four columns:

```yaml
type: object_rewriter
relation:
  - match: "testdb.testschema.x"
    clustering:
      add: [a]
  - match: "testdb.testschema.y"
    clustering:
      remove: [b]
```

--------------------------------------------------------------------------------

## 2. Environment configuration (`type: environment`)

Specifies session defaults including default database, schema search paths, and
session date formatting (e.g., Oracle `NLS_DATE_FORMAT`).

```yaml
type: environment
session:
  defaultDatabase: target-gcp-project-id
  schemaSearchPath: [dataset_primary, dataset_secondary]
  dateFormat: "DD/MM/YYYY"  # Formats date literals; equivalent to Oracle NLS_DATE_FORMAT
```

--------------------------------------------------------------------------------

## 3. Metadata configuration (`type: metadata`)

Specifies signatures of user-defined functions (UDFs) to improve translation
accuracy.

```yaml
type: metadata
udfs:
  - "date parse_short_date(dt int)"
```

--------------------------------------------------------------------------------

## 4. Optimizer configuration (`type: optimizer`)

Enables optional transformations that can improve the performance or cost of the
translated SQL. Their effect depends on the query, so compare the result against
the unmodified translation.

Transformation                               | Effect                                                                                                                                               | Parameters
:------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :---------
`PRECOMPUTE_INDEPENDENT_SUBSELECTS`          | Extracts independent scalar subqueries into `DECLARE` variables that are evaluated once, reducing the data scanned in `WHERE` and `JOIN-ON` clauses. | `scope: [PREDICATE, PROJECTION]` (default `PREDICATE`)
`REWRITE_CTE_TO_TEMP_TABLE`                  | Rewrites a CTE that is referenced multiple times into a temporary table, so it is evaluated once.                                                    | `threshold: N`, the minimum number of references
`REWRITE_ZERO_SCALE_NUMERIC_AS_INTEGER`      | Rewrites zero-scale `NUMERIC`/`BIGNUMERIC` columns (such as Snowflake `NUMBER(38,0)` / `INTEGER`) to `INT64`.                                        | `bigint: N`, the maximum precision to convert (default 18)
`DROP_TEMP_TABLE`                            | Appends `DROP TABLE` statements for temporary tables that the script creates but doesn't drop.                                                       | None
`REGEXP_CONTAINS_TO_LIKE`                    | Rewrites `REGEXP_CONTAINS` calls into `LIKE` when `LIKE` can express the pattern.                                                                    | None
`ADD_DISTINCT_TO_SUBQUERY_IN_SET_COMPARISON` | Adds `DISTINCT` to subqueries used as the value set of `[NOT] IN` predicates.                                                                        | None
`APPROXIMATE_RANGE_PARTITIONS`               | Approximates irregular integer partitioning (such as Teradata `RANGE_N`) with contiguous, equal-size `RANGE_BUCKET` ranges.                          | None

Values that need more than 18 digits don't fit in `INT64`. Don't raise `bigint`
above 18 unless the data stays within the `INT64` range.

```yaml
type: optimizer
transformations:
  - name: PRECOMPUTE_INDEPENDENT_SUBSELECTS
    parameters:
      scope: PREDICATE
  - name: REWRITE_CTE_TO_TEMP_TABLE
    parameters:
      threshold: 2
  - name: DROP_TEMP_TABLE
```

--------------------------------------------------------------------------------

## 5. Statement rewriter (`type: experimental_statement_rewriter`)

Controls statement-level syntax generation, clause representation, and decimal
precision behavior.

-   **`select.starProjection`**: Controls wildcard expansion (`ALLOW`,
    `PRESERVE` [default], `EXPAND`).
-   **`select.groupBy`**: Controls `GROUP BY` clause output format
    (`EXPRESSION`, `ALIAS`, `INDEX`).
-   **`select.orderBy`**: Controls `ORDER BY` clause output format
    (`EXPRESSION`, `ALIAS`, `INDEX`).
-   **`common.decimalPrecision`**: `STRICT` keeps the source decimal precision.
-   **`common.stringPrecision`**: `STRICT` keeps the source string length.

```yaml
type: experimental_statement_rewriter
select:
  starProjection: EXPAND        # Expand SELECT * into explicit column lists
  groupBy: ALIAS                # GROUP BY column_alias instead of full expression
  orderBy: INDEX                # ORDER BY 1, 2 positional column indices
common:
  decimalPrecision: STRICT      # Enforce strict decimal precision matching
```

--------------------------------------------------------------------------------

## 6. Input formats (`type: experimental_input_formats`)

Specifies character encoding (charset) of input files.

```yaml
type: experimental_input_formats
formats:
- source:
    pathGlob: "*.sql"
  contents:
    raw:
      charset: iso-8859-1
```

[yaml_guide]: https://cloud.google.com/bigquery/docs/config-yaml-translation
