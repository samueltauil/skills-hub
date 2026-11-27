# BigQuery Remote Functions Reference

## Table of Contents

-   [1. Architecture & JSON Request/Response Contract](#architecture-contract)
-   [2. Cloud Run Endpoint Implementation](#endpoint-implementation)
-   [3. Creating & Configuring the BigQuery Remote Function](#creating-remote-function)
-   [4. Performance, Batching & Retry Handling](#performance-batching)

--------------------------------------------------------------------------------

## 1. Architecture & JSON Request/Response Contract {#architecture-contract}

<a id="architecture-contract"></a>

BigQuery Remote Functions send batches of row arguments via HTTP `POST` to an
external HTTPS endpoint hosted on Cloud Run or Cloud Run functions using a
`CLOUD_RESOURCE` connection service account.

### Request JSON Schema (Sent by BigQuery)

BigQuery sends a `Content-Type: application/json` body with the following keys:

```json
{
  "requestId": "124ab1c",
  "caller": "//bigquery.googleapis.com/projects/my-project/jobs/bquxjob_1234",
  "sessionUser": "user@example.com",
  "userDefinedContext": {
    "env": "prod",
    "mode": "strict"
  },
  "calls": [
    ["row1_arg1", 42],
    ["row2_arg1", null]
  ]
}
```

### Response JSON Schema (Returned by Your Endpoint)

The HTTP endpoint must return HTTP `200 OK` with a `replies` array whose length
**strictly matches** the number of elements in `calls`:

```json
{
  "replies": [
    {"status": "enriched", "score": 0.95},
    null
  ]
}
```

-   **Error Reporting**: If a non-retryable error occurs, return an HTTP `4xx`
    code other than `408` or `429` (e.g., `400 Bad Request`) with
    `{"errorMessage": "Detailed reason"}` (must be under 1 KB) so BigQuery
    surfaces the message immediately without retrying.
-   **Retry Triggering**: BigQuery automatically retries requests that return
    HTTP `408`, `429`, `500`, `503`, or `504` (other HTTP codes like `501` or
    `502` are not retried and will fail the query).

--------------------------------------------------------------------------------

## 2. Cloud Run Endpoint Implementation (Python Functions Framework) {#endpoint-implementation}

<a id="endpoint-implementation"></a>

Deploy a stateless HTTP handler that processes `calls` in order and preserves
exact array length:

```python
import functions_framework
from flask import jsonify, make_response

@functions_framework.http
def handle_bq_remote_udf(request):
    try:
        body = request.get_json(silent=True)
        if not body or "calls" not in body:
            return make_response(
                jsonify({"errorMessage": "Missing 'calls' in request."}),
                400,
            )

        context = body.get("userDefinedContext", {})
        calls = body["calls"]
        replies = []

        for row_args in calls:
            street, postal_code = row_args[0], row_args[1]
            if street is None and postal_code is None:
                replies.append(None)
            else:
                replies.append({
                    "normalized": f"{street or ''} {postal_code or ''}".strip(),
                    "env": context.get("env", "default"),
                })

        return jsonify({"replies": replies})
    except Exception as exc:
        return make_response(
            jsonify({"errorMessage": f"Permanent execution error: {exc}"}),
            400,
        )
```

Deploy the service to Cloud Run with `--no-allow-unauthenticated`:

```bash
gcloud run deploy {cloud_run_service} \
  --source=. \
  --function=handle_bq_remote_udf \
  --region={region} \
  --no-allow-unauthenticated
```

--------------------------------------------------------------------------------

## 3. Creating & Configuring the BigQuery Remote Function {#creating-remote-function}

<a id="creating-remote-function"></a>

1.  **Create the Cloud Resource Connection** (must be in the same location as
    the BigQuery dataset containing the remote function):

    ```bash
    bq mk --connection --connection_type=CLOUD_RESOURCE \
      --location={region} --project_id={project_id} {connection_id}
    ```
2.  **Grant `roles/run.invoker` to the Connection's Service Account**: Retrieve
    the service account via `bq show --connection
    {project_id}.{region}.{connection_id}` and bind `roles/run.invoker` on the
    Cloud Run service (**confirm with the user before modifying the Cloud Run
    service IAM policy**):

    ```bash
    gcloud run services add-iam-policy-binding {cloud_run_service} \
      --region={region} \
      --member="serviceAccount:{connection_sa_email}" \
      --role="roles/run.invoker"
    ```
3.  **Create the Remote Function in BigQuery** (`ARRAY`, `STRUCT`, `INTERVAL`,
    and `GEOGRAPHY` parameters and return values are unsupported; serialize
    complex structures as `JSON`):

    ```sql
    CREATE OR REPLACE FUNCTION `{project_id}.{dataset_id}.enrich_address`(
      street STRING,
      postal_code STRING
    )
    RETURNS JSON
    REMOTE WITH CONNECTION `{project_id}.{region}.{connection_id}`
    OPTIONS (
      endpoint = 'https://{cloud_run_service_url}',
      max_batching_rows = 1000,
      user_defined_context = [
        ('env', 'prod'),
        ('mode', 'strict')
      ]
    );
    ```

--------------------------------------------------------------------------------

## 4. Performance, Batching & Retry Handling {#performance-batching}

<a id="performance-batching"></a>

-   **Idempotency & Retry Cap**: BigQuery retries failed batches up to **20
    times** and may resend the same batch (with the same `requestId`) even after
    your endpoint returns HTTP `200 OK` if the network response is interrupted.
    Design remote endpoints to be idempotent (or deduplicate side effects using
    `requestId`).
-   **Batch Sizing (`max_batching_rows`)**: BigQuery batches rows up to
    `max_batching_rows` (or determines batch size automatically) to avoid HTTP
    endpoint timeouts. Set `max_batching_rows` (e.g. between `500` and `5000`)
    when calling downstream rate-limited APIs to avoid Cloud Run request
    timeouts. Key limits to note:
    -   **Maximum input size**: 5 MB total size of all input arguments from a
        single row.
    -   **HTTP response size limit**: 15 MB for Cloud Run / 2nd gen (10 MB for
        1st gen).
    -   **HTTP invocation timeout**: Up to 20 minutes for Cloud Run / 2nd gen (9
        minutes for 1st gen).
    -   **Concurrency**: Up to 10 concurrent queries containing remote functions
        per project.
-   **Cloud Run Concurrency & Max Instances**: Configure `--concurrency` and
    `--max-instances` on the Cloud Run service to match downstream quota limits
    so parallel BigQuery slots do not overwhelm external databases or APIs.
-   **VPC Egress for Private Network Targets**: Configure Direct VPC Egress
    (`--network` / `--subnet`) or a Serverless VPC Access connector
    (`--vpc-connector`) on the Cloud Run service when the remote function needs
    to reach private IP endpoints inside a VPC network.
-   **Filter Before Calling**: Push `WHERE` predicates into a subquery or CTE
    before invoking a Remote Function so the endpoint is only called on filtered
    rows.
