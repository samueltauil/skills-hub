# BigQuery UDF IAM, Authorized Routines, and Quotas Reference

## Table of Contents

-   [1. IAM Roles Matrix by UDF Type](#iam-matrix)
-   [2. Sharing UDFs Across Datasets (Authorized Routines)](#authorized-routines)
-   [3. Quotas, Limits & Troubleshooting Common Errors](#quotas-troubleshooting)

--------------------------------------------------------------------------------

## 1. IAM Roles Matrix by UDF Type {#iam-matrix}

<a id="iam-matrix"></a>

Grant the least-privilege predefined IAM roles based on whether the principal
authors the UDF or invokes an existing UDF:

Persona & Action                                  | SQL / JS / Offline Python UDF                                              | Python UDF (`WITH CONNECTION`)                                                                                  | Remote Function (`REMOTE WITH CONNECTION`)
:------------------------------------------------ | :------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- | :-----------------------------------------
**UDF Author** (Create / Replace UDF)             | `roles/bigquery.dataEditor` (dataset) + `roles/bigquery.jobUser` (project) | Same + `roles/bigquery.connectionAdmin` (project); `roles/resourcemanager.projectIamAdmin` if running `GRANT ... ON PROJECT` | Same + `roles/bigquery.connectionAdmin` (project)
**UDF Caller** (Invoke in `SELECT`)               | `roles/bigquery.dataViewer` (dataset) + `roles/bigquery.user` (project)    | Same + `roles/bigquery.connectionUser` (connection)                                                             | Same + `roles/bigquery.connectionUser` (connection)
**Connection Service Account** (`connection-...`) | N/A (No connection used)                                                   | `roles/serviceusage.serviceUsageConsumer` (query project) + Target API role (e.g., `roles/cloudtranslate.user`) | `roles/run.invoker` on the Cloud Run service (or `roles/cloudfunctions.invoker`)

> [!NOTE] If a JavaScript or Python UDF loads files from Cloud Storage via
> `OPTIONS(library=['gs://...'])`, the user creating or running the UDF also
> requires `roles/storage.objectViewer` (`storage.objects.get`) on the bucket.

--------------------------------------------------------------------------------

## 2. Sharing UDFs Across Datasets (Authorized Routines) {#authorized-routines}

<a id="authorized-routines"></a>

Authorize a SQL UDF (or table function / stored procedure whose SQL body
references tables) to read tables in a protected source dataset without granting
end users direct `roles/bigquery.dataViewer` access to the underlying tables:

1.  **Create the UDF in a Shared Dataset (`{shared_dataset_id}`)**:

    ```sql
    CREATE OR REPLACE FUNCTION `{project_id}.{shared_dataset_id}.get_masked_salary`(
      emp_id INT64
    )
    RETURNS FLOAT64
    AS ((
      SELECT ROUND(salary, -3)
      FROM `{project_id}.{sensitive_dataset_id}.employees`
      WHERE employee_id = emp_id
    ));
    ```
2.  **Authorize the Routine on `{sensitive_dataset_id}`**: Updating the source
    dataset's `access` array requires `bigquery.datasets.update` (for example,
    `roles/bigquery.dataOwner` on `{sensitive_dataset_id}`, which is not
    included in `roles/bigquery.dataEditor`). Confirm with the user before
    modifying dataset ACLs, then update the `access` array using `bq show
    --format=prettyjson` and `bq update --source` to add an entry with
    `"routine"`:

    ```json
    {
      "routine": {
        "projectId": "{project_id}",
        "datasetId": "{shared_dataset_id}",
        "routineId": "get_masked_salary"
      }
    }
    ```
3.  **Grant End Users Access to `{shared_dataset_id}`**: Grant
    `roles/bigquery.dataViewer` on `{shared_dataset_id}` to the caller.

> [!WARNING] **Modifying a routine invalidates its authorization**: Every time
> you update an authorized routine via `CREATE OR REPLACE FUNCTION` (or `bq
> update`), BigQuery invalidates its existing dataset authorization and callers
> fail with `Access Denied: Table ...` until you re-authorize the routine on
> `{sensitive_dataset_id}`. For immediate effect without propagation delay,
> remove the stale routine entry from `{sensitive_dataset_id}`'s `access` array
> before re-adding it.

--------------------------------------------------------------------------------

## 3. Quotas, Limits & Troubleshooting Common Errors {#quotas-troubleshooting}

<a id="quotas-troubleshooting"></a>

Resource / Limit                            | Quota / Threshold                                                                                                  | Remediation / Best Practice
:------------------------------------------ | :----------------------------------------------------------------------------------------------------------------- | :--------------------------
**Python UDF Container Size / Storage**     | **10 GiB** sum total per project per region (applies to built container image size, not runtime RAM)               | Drop unused Python UDFs (`DROP FUNCTION`) to free container image quota.
**Python UDF Container Specs**              | Max **4 vCPU** and **16 GiB** memory                                                                               | Use vectorized execution (`pd.DataFrame` / `pa.RecordBatch`) or offload heavier workloads to a Remote Function.
**JavaScript UDF Limits**                   | 5 MB output/row; 32 KB inline code; 1 MB/file; 50 files; ~5 min timeout                                            | Split large lookups into BigQuery tables; bundle JS libraries under 1 MB.
**Python UDF Quotas**                       | 30 creates/updates/min; 10 concurrent queries per project                                                          | Stagger DDL deploys; pool concurrent query traffic across projects.
**Remote Function HTTP Response & Timeout** | 15 MB (Cloud Run / 2nd gen) / 10 MB (1st gen); 20 min (Cloud Run) / 9 min (1st gen) timeout; 10 concurrent queries | Lower `max_batching_rows` in `OPTIONS(...)` if row payloads are large.

### Common Error Diagnosis

-   **`Connection timeout` inside a Python UDF**: The Python code attempted an
    outbound network request without a `WITH CONNECTION` clause (or inside a
    VPC-SC perimeter to an unsupported host). Attach `WITH CONNECTION` and grant
    `roles/serviceusage.serviceUsageConsumer` to the connection service account.
-   **`Access Denied: Response code 403` on Remote Function**: The connection
    service account (`bq show --connection`) is missing `roles/run.invoker` on
    the target Cloud Run service.

-   **`Invalid CPU/Memory combination` on Python UDF**: Verify `container_cpu`
    and `container_memory` against the compatibility matrix in
    [python-udfs.md](python-udfs.md).

-   **`Flight error: ... unexpected indent` on Python UDF**: Module-level Python
    code (`import`, `def`) inside `AS r'''...'''` has leading indentation. Flush
    all top-level statements to column 0 (no leading spaces).

-   **Query invoking a Python UDF remains queued in `RUNNING`**: The first query
    after creating/updating a Python UDF waits for the container image build to
    complete (check `build_status.build_state` in
    `INFORMATION_SCHEMA.ROUTINES`).
