# BigQuery Managed Python UDFs Reference

## Table of Contents

-   [1. Runtime Environment & Limitations](#runtime-environment)
-   [2. Data Type Mappings](#data-type-mappings)
-   [3. Vectorized Execution (Pandas & PyArrow)](#vectorized-execution)
-   [4. Third-Party Dependencies (PyPI & GCS)](#dependencies)
-   [5. Container Resource Limits](#resource-limits)
-   [6. Calling Online Services & APIs](#calling-apis)
-   [7. End-to-End Validation & Debugging](#validation-workflow)

--------------------------------------------------------------------------------

## 1. Runtime Environment & Limitations {#runtime-environment}

<a id="runtime-environment"></a>

BigQuery builds and executes Python UDFs on managed containers using the
`python-3.11` base image.

### Pre-installed Packages (`python-3.11`)

Do not list these packages in `OPTIONS(packages=[...])`. Listing one without a
version is a no-op (BigQuery uses the pre-installed version); only list it with
an explicit version specifier (e.g., `'pandas==2.2.2'`) when you need a
different version, which triggers an install during the container build:

Package                   | Pre-installed Version
:------------------------ | :-----------------------------------
`numpy`                   | `1.26.3`
`pandas`                  | `2.1.4`
`pyarrow`                 | `14.0.2`
`python-dateutil`         | `2.8.2`
`absl-py`                 | `2.0.0`
`pytz` / `tzdata` / `six` | `2023.3.post1` / `2023.4` / `1.16.0`

### Hard Constraints

-   **No temporary functions**: Never use `CREATE TEMP FUNCTION` or `TEMPORARY`
    with `LANGUAGE python`; BigQuery requires a persistent dataset target to
    store and track the built container artifact.
-   **Unsupported BigQuery types**: Do not use `JSON`, `RANGE`, `INTERVAL`, or
    `GEOGRAPHY` as parameter or `RETURNS` types. Pass JSON payloads as `STRING`
    and parse with Python's `json.loads()` inside the UDF.
-   **No query result caching**: Queries invoking a Python UDF are never cached
    because Python UDFs are always treated as non-deterministic.
-   **No Materialized Views or CMEK**: Do not reference Python UDFs in
    materialized views or encrypt them with CMEK.
-   **Regional Container Size Quota**: The size of all Python UDF containers per
    project and per region is restricted to a sum total of **10 GiB**. Note that
    this limit is for the **container size** (the built container image storage
    footprint on disk), not the runtime container execution memory
    (`container_memory`). Drop unused Python UDFs to reclaim quota.
-   **Zero top-level indentation**: Module-level Python lines (`import`, helper
    functions, classes, and `def {entry_point}(...)`) inside `AS r'''...'''`
    must have **zero leading spaces** (flush to the left margin). Indenting
    module-level Python to match SQL indentation causes `IndentationError`.

--------------------------------------------------------------------------------

## 2. Data Type Mappings {#data-type-mappings}

<a id="data-type-mappings"></a>

Match the Python type annotation and return value to whether you are authoring a
standard row-by-row UDF or a vectorized (`pandas` / `pyarrow`) UDF:

BigQuery Type | Standard UDF (Python)       | Vectorized UDF (`pandas`)             | Vectorized UDF (`pyarrow`)
:------------ | :-------------------------- | :------------------------------------ | :-------------------------
`BOOL`        | `bool`                      | `BooleanDtype`                        | `DataType(bool)`
`INT64`       | `int`                       | `Int64Dtype`                          | `DataType(int64)`
`FLOAT64`     | `float`                     | `FloatDtype`                          | `DataType(double)`
`STRING`      | `str`                       | `StringDtype`                         | `DataType(string)`
`BYTES`       | `bytes`                     | `binary[pyarrow]`                     | `DataType(binary)`
`DATE`        | `datetime.date`             | `date32[pyarrow]`                     | `DataType(date32[day])`
`TIME`        | `datetime.time`             | `time64[pyarrow]`                     | `Time64Type(time64[us])`
`DATETIME`    | `datetime.datetime` (no tz) | `timestamp[us][pyarrow]`              | `TimestampType(timestamp[us])`
`TIMESTAMP`   | `datetime.datetime` (`UTC` on input; any tz on return, converted to `UTC`) | `timestamp[us, tz=UTC][pyarrow]`      | `TimestampType(timestamp[us], tz)`
`ARRAY<T>`    | `list`                      | `list<...>[pyarrow]` (`ArrowDtype`)   | `ListType`
`STRUCT<...>` | `dict`                      | `struct<...>[pyarrow]` (`ArrowDtype`) | `StructType`

--------------------------------------------------------------------------------

## 3. Vectorized Execution (Pandas & PyArrow) {#vectorized-execution}

<a id="vectorized-execution"></a>

Prefer vectorized execution for analytical transformations over large tables
because processing batches of rows eliminates per-row Python call overhead.

> [!WARNING] **Vectorized operations must be row-independent**: BigQuery calls
> vectorized UDFs on arbitrary batches of rows (up to `max_batching_rows`). Do
> NOT compute global column statistics (such as z-scores, dataset mean/std, or
> rank) across `df`, because each batch only sees an arbitrary slice of rows.
> Use SQL window functions (`(val - AVG(val) OVER()) / NULLIF(STDDEV(val)
> OVER(), 0)`) for dataset-wide statistics. Vectorized Python UDFs should
> perform row-independent calculations (e.g. `df['x'] * df['y']` or geometric
> formulas).

### Pandas Vectorization (`pd.DataFrame`)

1.  Annotate the single entrypoint parameter as `df: pd.DataFrame`.
2.  Access SQL arguments by their column names in `df['{param_name}']`.
3.  Return a `pd.Series` or single-column `pd.DataFrame` with the exact same row
    count as `df`:

```sql
CREATE OR REPLACE FUNCTION `{project_id}.{dataset_id}.multiply_vectorized`(
  x FLOAT64, y FLOAT64
)
RETURNS FLOAT64
LANGUAGE python
OPTIONS (
  runtime_version = 'python-3.11',
  entry_point = 'vectorized_multiply'
)
AS r'''
import pandas as pd

def vectorized_multiply(df: pd.DataFrame) -> pd.Series:
    return df['x'] * df['y']
''';
```

### Apache Arrow Vectorization (`pa.RecordBatch`)

Annotate the single entrypoint parameter as `batch: pa.RecordBatch` for
zero-copy columnar compute with `pyarrow.compute`:

```sql
CREATE OR REPLACE FUNCTION `{project_id}.{dataset_id}.multiply_arrow`(
  x FLOAT64, y FLOAT64
)
RETURNS FLOAT64
LANGUAGE python
OPTIONS (
  runtime_version = 'python-3.11',
  entry_point = 'vectorized_multiply_arrow'
)
AS r'''
import pyarrow as pa
import pyarrow.compute as pc

def vectorized_multiply_arrow(batch: pa.RecordBatch):
    return pc.multiply(batch.column('x'), batch.column('y'))
''';
```

--------------------------------------------------------------------------------

## 4. Third-Party Dependencies (PyPI & Cloud Storage) {#dependencies}

<a id="dependencies"></a>

### Installing PyPI Packages (`packages`)

Specify wheel-compatible packages in `OPTIONS(packages=[...])` using PEP 440
version specifiers. Source-only (`sdist`) packages without binary wheels fail
container build:

```sql
OPTIONS (
  entry_point = 'area_handler',
  runtime_version = 'python-3.11',
  packages = ['scipy==1.15.3', 'pydantic>=2.0,<3.0']
)
```

### Importing Custom `.py` Files from Cloud Storage (`library`)

1.  Ensure the user creating the UDF has `storage.objects.get` permission on the
    Cloud Storage object.
2.  Ensure every folder segment and filename after `gs://{bucket_name}/` is a
    valid Python identifier (`[A-Za-z_][A-Za-z0-9_]*`, no hyphens).
3.  Import the file using dot-separated path notation relative to the bucket
    root:

```sql
CREATE OR REPLACE FUNCTION `{project_id}.{dataset_id}.run_custom_lib`(
  a FLOAT64, b STRING
)
RETURNS STRING
LANGUAGE python
OPTIONS (
  entry_point = 'compute',
  runtime_version = 'python-3.11',
  library = ['gs://{bucket_name}/my_pkg/utils/helper.py']
)
AS r'''
import my_pkg.utils.helper as helper

def compute(a: float, b: str) -> str:
    return helper.transform(a, b)
''';
```

--------------------------------------------------------------------------------

## 5. Container Resource Limits (CPU, Memory, Concurrency) {#resource-limits}

<a id="resource-limits"></a>

By default, BigQuery allocates `container_memory = '512Mi'`, `container_cpu =
1.0`, and `container_request_concurrency = 80` to each Python UDF container.
Omit these options when default resources are sufficient, and specify them in
`OPTIONS(...)` only when tuning container memory, CPU, or concurrency for
resource-intensive workloads.

> [!IMPORTANT] If you set `container_cpu < 1.0` without explicitly setting
> `container_request_concurrency`, BigQuery automatically drops concurrency to
> `1` at runtime.

Always select a valid `(container_memory, container_cpu)` pair from the table
below, or the `CREATE FUNCTION` statement will fail validation:

`container_memory` (`Mi`, `M`, `Gi`, `G`) | Minimum `container_cpu` | Maximum `container_cpu`
:---------------------------------------- | :---------------------- | :----------------------
`256Mi` to `512Mi`                        | `0.33`                  | `2`
`> 512Mi` to `1Gi`                        | `0.5`                   | `2`
`> 1Gi` to `< 2Gi`                        | `1`                     | `2`
`2Gi` to `4Gi`                            | `1`                     | `4`
`> 4Gi` to `8Gi`                          | `2`                     | `4`
`> 8Gi` to `16Gi`                         | `4`                     | `4`

-   **Allowed `container_cpu` values**: Either a fractional float in `[0.33,
    1.0]` or one of the discrete integers `{1, 2, 4}` (values above `1` other
    than `2` or `4`, such as `3`, are rejected).
-   **Allowed `container_request_concurrency` bounds**: Integer in `[1, 1000]`
    (default `80` when `container_cpu >= 1.0`, or `1` when `container_cpu <
    1.0`).

Example configuring high-memory containers:

```sql
OPTIONS (
  entry_point = 'heavy_transform',
  runtime_version = 'python-3.11',
  container_memory = '8Gi',
  container_cpu = 2,
  container_request_concurrency = 16
)
```

> [!NOTE] Runtime `container_memory` (RAM allocated to an executing container
> instance, up to 16 GiB) is distinct from the 10 GiB regional container quota.
> The 10 GiB limit is for the **container size** (the sum total storage size of
> all built Python UDF container images per project and region).

--------------------------------------------------------------------------------

## 6. Calling Online Services & APIs (`WITH CONNECTION`) {#calling-apis}

<a id="calling-apis"></a>

By default (without `WITH CONNECTION`), Python UDF containers run in a
network-isolated sandbox where all outbound traffic is blocked and times out.

### When & How to Configure `WITH CONNECTION`

Attach a `CLOUD_RESOURCE` connection whenever the Python UDF invokes Google
Cloud APIs or external HTTP services at runtime:

1.  **Create the Connection**:

    ```sql
    CREATE CONNECTION IF NOT EXISTS `{project_id}.{region}.{connection_id}`
    OPTIONS (connection_type = 'CLOUD_RESOURCE');
    ```
2.  **Retrieve the Connection Service Account**:

    ```bash
    bq show --connection {project_id}.{region}.{connection_id}
    ```
3.  **Grant Required IAM Roles to the Connection Service Account**: Running
    `GRANT ... ON PROJECT` modifies the project's IAM policy and requires
    `resourcemanager.projects.setIamPolicy` (for example,
    `roles/resourcemanager.projectIamAdmin`); **confirm with the user before
    running project-level IAM grants**:

    -   Grant `roles/serviceusage.serviceUsageConsumer` on `{query_project_id}`.
        The `connection:` grantee takes the connection path, not the service
        account email (use `"serviceAccount:{connection_sa_email}"` to grant by
        email):

        ```sql
        GRANT `roles/serviceusage.serviceUsageConsumer`
        ON PROJECT `{query_project_id}`
        TO "connection:{project_id}.{region}.{connection_id}";
        ```
    -   Grant the target API role (e.g., `roles/cloudtranslate.user` or
        `roles/aiplatform.user`) on the target service project.
4.  **Enforce Timeouts, Logging, and Prescriptive Exception Handling in
    Python**:

    -   Initialize SDK clients in the global scope (outside `entry_point`) so
        connections are reused across invocations and batches.
    -   Pass an explicit per-attempt `timeout=` on each client call.
        `Retry(timeout=...)` only caps the total retry duration, not each
        attempt.
    -   Differentiate transient errors from unrecoverable user/configuration
        errors:
        -   **Transient errors** (`google.api_core.exceptions.TooManyRequests`,
            `ServiceUnavailable`, `DeadlineExceeded`, `InternalServerError`,
            `RetryError`): log a warning and return `None` (`NULL`) so transient
            row-level issues do not fail the overall query job.
        -   **Unrecoverable / Fatal errors** (`PermissionDenied`,
            `Unauthenticated`, `InvalidArgument`, bad configuration): log the
            error and raise (such as `RuntimeError`). BigQuery surfaces
            unhandled Python exceptions directly as user query errors
            (`Encounter an error when invoking the function: ...`) along with
            the stack trace.
        -   Do **not** catch the base class `GoogleAPICallError` as "transient";
            it also matches the fatal errors above and silently converts auth
            failures into `NULL`s.
    -   Log with `logging.warning(...)` / `logging.error(...)`. Logs are written
        to `bigquery.googleapis.com/ManagedRoutineInvocation` **only** when the
        session enables `SET @@udf.properties = JSON '{"enableDebugOutput":
        true}';` (logging is off by default to prevent data exfiltration).
    -   **Never log row values** (inputs or outputs). Anyone with Cloud Logging
        access can read UDF logs regardless of their BigQuery table permissions;
        log exception types and messages instead.

### VPC Service Controls (VPC-SC) Constraints

-   **Without `WITH CONNECTION`**: All outbound traffic is blocked.
-   **With `WITH CONNECTION` inside a VPC-SC perimeter**: Public internet access
    is blocked; the UDF can only reach Google Cloud services supported by VPC-SC
    over `restricted.googleapis.com`. Ensure both the query project and target
    service project are inside the same perimeter (or bridged) and add the
    target API (e.g., `translate.googleapis.com`) to the perimeter's restricted
    services.

--------------------------------------------------------------------------------

## 7. End-to-End Validation & Debugging Workflow {#validation-workflow}

<a id="validation-workflow"></a>

Always validate a Python UDF in three sequential stages, because BigQuery
container builds take 1–3+ minutes per iteration and the `CREATE FUNCTION` DDL
statement returns **before** the container build actually completes.

### Stage 1: Validate the Python Code Before Running BigQuery DDL

Verify syntax, data handling (`None`/NULLs, edge cases), and PyPI wheel
compatibility before creating the routine in BigQuery:

#### Option A: Local Validation with Test Input

Extract the entrypoint function into a local test script and verify both valid
and `None` inputs using Python 3.11:

```bash
python3 -c "
import pandas as pd
# Paste UDF function body here
def vectorized_multiply(df: pd.DataFrame) -> pd.Series:
    return df['x'] * df['y']

test_df = pd.DataFrame({'x': [2.0, 4.0, None], 'y': [3.0, 5.0, 10.0]})
out = vectorized_multiply(test_df)
assert len(out) == len(test_df), 'Output Series length must match input'
print('Local validation passed:', out.tolist())
"
```

#### Option B: Container & Cloud API Validation via Cloud Run Jobs

When validating Linux wheel builds (`requirements.txt`), container memory
limits, or Google Cloud API calls in a serverless container environment (see
[Build and create a Python job in Cloud Run](https://docs.cloud.google.com/run/docs/quickstarts/jobs/build-create-python.md.txt)):

> [!NOTE] This Cloud Run Job buildpack execution serves as an approximation of
> the BigQuery UDF container, since it validates wheel resolution and network
> connectivity, though it does not share BigQuery's exact internal base image or
> pre-installed package versions.

1.  Create a temporary directory with `main.py` (invoking your UDF entrypoint on
    sample inputs), `requirements.txt` (matching `OPTIONS(packages=[...])`),
    `.python-version` (containing `3.11` to pin buildpack resolution), and a
    `Procfile` (no file extension):

    ```text
    web: python3 main.py
    ```

    ```bash
    echo "3.11" > .python-version
    ```
2.  Build and deploy the source to a Cloud Run Job, then execute it
    synchronously:

    ```bash
    gcloud services enable run.googleapis.com cloudbuild.googleapis.com --quiet

    gcloud run jobs deploy bq-udf-validator \
      --source . \
      --tasks 1 \
      --max-retries 0 \
      --region={region} \
      --project={project_id}

    gcloud run jobs execute bq-udf-validator --region={region} --wait
    ```
3.  Clean up the temporary validation job after verification:

    ```bash
    gcloud run jobs delete bq-udf-validator --region={region} --quiet
    ```

--------------------------------------------------------------------------------

### Stage 2: Execute DDL and Poll Container Build Status

Running `CREATE OR REPLACE FUNCTION` for a Python UDF returns `DONE` as soon as
the metadata is registered—**before** the container image finishes building. Do
**not** assume the UDF is ready to use solely because the DDL command succeeded.

1.  **Submit the `CREATE OR REPLACE FUNCTION` DDL**:

    ```bash
    bq query --use_legacy_sql=false "{create_function_ddl}"
    ```
2.  **Poll `INFORMATION_SCHEMA.ROUTINES` Until `build_state` Reaches Terminal**:
    Repeatedly query `build_status` until `build_state` transitions from
    `IN_PROGRESS` to either `SUCCEEDED` or `FAILED`:

    ```sql
    SELECT
      routine_name,
      build_status.build_state,
      build_status.build_state_update_time,
      build_status.build_duration_seconds,
      build_status.image_size_bytes
    FROM
      `{project_id}.{dataset_id}`.INFORMATION_SCHEMA.ROUTINES
    WHERE
      routine_name = '{udf_name}';
    ```

--------------------------------------------------------------------------------

### Stage 3: Test the UDF in BigQuery & Debug with Cloud Logging

Once `build_status.build_state` is confirmed as `SUCCEEDED`, execute a test
query in BigQuery covering `NULL` and valid inputs.

If runtime debugging is needed (note that `print()` does not log and is
ignored):

1.  Enable debug output for your session and run a bounded test query:

    ```sql
    SET @@udf.properties = JSON '{"enableDebugOutput": true}';
    SELECT
      `{project_id}.{dataset_id}.{udf_name}`(NULL) AS null_case,
      `{project_id}.{dataset_id}.{udf_name}`('sample_input') AS valid_case;
    ```
2.  Use Python's standard `logging` module (`logging.info`, `logging.warning`,
    `logging.error`) inside your UDF:

    ```python
    import logging

    def parse_record(raw: str) -> str:
        try:
            return raw.strip() if raw is not None else None
        except Exception as e:
            logging.error(f"Failed to parse record: {e}")
            return None
    ```
3.  Query logs in Cloud Logging using resource type
    `bigquery.googleapis.com/ManagedRoutineInvocation` and filter by
    `resource.labels.routine_id="{udf_name}"`.
