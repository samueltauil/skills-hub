# BigQuery SQL and JavaScript UDFs Reference

## Table of Contents

-   [1. SQL Scalar & Templated UDFs (ANY TYPE)](#sql-templated)
-   [2. SQL & JavaScript Aggregate UDFs](#aggregate-udfs)
-   [3. JavaScript UDF Type Mapping & Precision Rules](#js-types)
-   [4. Loading External JavaScript Libraries from Cloud Storage](#js-libraries)

--------------------------------------------------------------------------------

## 1. SQL Scalar & Templated UDFs (`ANY TYPE`) {#sql-templated}

<a id="sql-templated"></a>

Prefer SQL UDFs whenever logic can be expressed in GoogleSQL, because the query
optimizer inlines SQL UDF bodies directly into the execution plan with zero
serialization overhead.

### Templated Parameters (`ANY TYPE`)

Use `ANY TYPE` to write polymorphic functions that accept multiple data types. A
templated function can declare an explicit return type (e.g. `RETURNS STRING`),
or omit `RETURNS` when the return type depends on the argument types, allowing
BigQuery to infer it per call site:

```sql
CREATE OR REPLACE FUNCTION `{project_id}.{dataset_id}.clamp_value`(
  x ANY TYPE,
  min_val ANY TYPE,
  max_val ANY TYPE
)
AS (
  GREATEST(min_val, LEAST(max_val, x))
);
```

### Subquery Expressions in SQL UDFs

SQL UDFs can reference tables or views using scalar subqueries `(SELECT ...)`:

```sql
CREATE OR REPLACE FUNCTION `{project_id}.{dataset_id}.lookup_country_name`(
  iso_code STRING
)
RETURNS STRING
AS ((
  SELECT country_name
  FROM `{project_id}.{dataset_id}.iso_countries`
  WHERE code = iso_code
  LIMIT 1
));
```

--------------------------------------------------------------------------------

## 2. SQL & JavaScript Aggregate UDFs {#aggregate-udfs}

<a id="aggregate-udfs"></a>

Use `CREATE OR REPLACE AGGREGATE FUNCTION` to compute a single result across a
group of rows.

### SQL Aggregate UDF

Mark non-aggregated parameters (constants across each group) with `NOT
AGGREGATE`:

```sql
CREATE OR REPLACE AGGREGATE FUNCTION `{project_id}.{dataset_id}.scaled_sum`(
  val FLOAT64,
  scale_factor FLOAT64 NOT AGGREGATE
)
RETURNS FLOAT64
AS (
  SUM(val) * scale_factor
);
```

### JavaScript Aggregate UDF Lifecycle

JavaScript aggregate UDFs must implement four lifecycle functions
(`initialState`, `aggregate`, `merge`, and `finalize`) to support distributed
parallel execution across BigQuery slots:

```sql
CREATE OR REPLACE AGGREGATE FUNCTION `{project_id}.{dataset_id}.geometric_mean`(
  x FLOAT64
)
RETURNS FLOAT64
LANGUAGE js
AS r"""
  export function initialState() {
    return { logSum: 0.0, count: 0 };
  }
  export function aggregate(state, x) {
    if (x !== null && x > 0) {
      state.logSum += Math.log(x);
      state.count += 1;
    }
  }
  export function merge(state, partialState) {
    state.logSum += partialState.logSum;
    state.count += partialState.count;
  }
  export function finalize(state) {
    return state.count === 0 ? null : Math.exp(state.logSum / state.count);
  }
""";
```

--------------------------------------------------------------------------------

## 3. JavaScript UDF Type Mapping & Precision Rules {#js-types}

<a id="js-types"></a>

BigQuery maps SQL types to JavaScript V8 objects according to strict rules.

> [!WARNING] BigQuery does **not** support `INT64` as an input parameter type in
> JavaScript UDFs because JavaScript `Number` (IEEE 754 double) loses integer
> precision beyond `2^53 - 1`. Pass 64-bit integers as `FLOAT64` or `STRING`
> (and parse with JavaScript `BigInt(str)`). Note that BigQuery **does** support
> `INT64` as a return type (returning either a Number or String from JS).

BigQuery Data Type       | JavaScript Data Type                                      | Notes
:----------------------- | :-------------------------------------------------------- | :----
`BOOL`                   | `Boolean`                                                 | Direct mapping
`INT64`                  | Unsupported input; supported return type (`Number`/`str`) | For input, cast to `STRING` or `FLOAT64` in SQL. Supported as return type (return Number/String).
`FLOAT64`                | `Number`                                                  | IEEE 754 double-precision float
`NUMERIC` / `BIGNUMERIC` | `Number` or `String`                                      | Encoded as `Number` only when integral and within `[-2^53, 2^53]`; otherwise `String` (including all fractional values). Coerce explicitly in JS (e.g. `Number(x)` or a decimal library).
`STRING`                 | `String`                                                  | UTF-8 string
`BYTES`                  | base64-encoded `String`                                   | Base64 string in scalar JS UDFs (`Uint8Array` in aggregate UDFs)
`DATE`                   | `Date`                                                    | JavaScript `Date` object
`TIMESTAMP`              | `Date` with `microsecond` field                           | Contains `microsecond` fraction of timestamp
`JSON`                   | Object / Array / Value                                    | Numbers in [-2^53, 2^53] exact; others rounded
`ARRAY<T>`               | `Array`                                                   | Nested arrays are unsupported in BigQuery
`STRUCT<...>`            | `Object`                                                  | Struct field names map to JS object keys

> [!NOTE] Encodings differ in JavaScript Aggregate UDFs (`CREATE AGGREGATE
> FUNCTION ... LANGUAGE js`): `INT64` maps to JavaScript `BigInt`, and `BYTES`
> maps to `Uint8Array`.

### Determinism Option

Specify `DETERMINISTIC` if the JavaScript UDF always produces the same output
for the same inputs (allowing BigQuery to cache results), or `NOT DETERMINISTIC`
if it uses `Math.random()` or `Date.now()`.

--------------------------------------------------------------------------------

## 4. Loading External JavaScript Libraries from Cloud Storage {#js-libraries}

<a id="js-libraries"></a>

Bundle third-party npm packages into a single self-contained file (using
`esbuild` or `webpack` with IIFE/global output) and upload the bundle to Cloud
Storage:

1.  **Bundle the Library Locally**:

    ```bash
    npx esbuild index.js --bundle --format=iife --global-name=MyLib --outfile=bundle.js
    gcloud storage cp bundle.js gs://{bucket_name}/udf_libs/bundle.js
    ```
2.  **Reference the Bundle via `OPTIONS(library=[...])`**:

    ```sql
    CREATE OR REPLACE FUNCTION `{project_id}.{dataset_id}.parse_with_bundle`(
      input_str STRING
    )
    RETURNS STRING
    DETERMINISTIC
    LANGUAGE js
    OPTIONS (
      library = ['gs://{bucket_name}/udf_libs/bundle.js']
    )
    AS r"""
      if (!input_str) return null;
      return MyLib.transform(input_str);
    """;
    ```
