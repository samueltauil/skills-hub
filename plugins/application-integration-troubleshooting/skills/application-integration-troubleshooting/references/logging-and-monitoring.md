# Cloud Logging and Cloud Monitoring

Use this reference to check why execution logs are missing, enable Cloud Logging on an integration or connector, run Logs Explorer and `gcloud logging read` queries, and inspect Cloud Monitoring metrics and alerts.

- [Local Logging vs Cloud Logging](#local-logging-vs-cloud-logging): Lines 11-28
- [Enabling Cloud Logging on an Integration](#enabling-cloud-logging-on-an-integration): Lines 29-45
- [Cloud Logging Queries (`gcloud logging read` and Logs Explorer)](#cloud-logging-queries-gcloud-logging-read-and-logs-explorer): Lines 46-110
- [Cloud Monitoring Metrics](#cloud-monitoring-metrics): Lines 111-138
- [Dashboards and Alerting](#dashboards-and-alerting): Lines 139-147

## Local Logging vs Cloud Logging

Application Integration has two logging layers. Cloud Logging depends on local logging being active.

| Setting (`databasePersistencePolicy`) | Console default | Behavior and caveats |
|---|---|---|
| **Local logging: `Enable (async)`** (`DATABASE_PERSISTENCE_ASYNC`) | Yes | Writes execution logs asynchronously with minimal latency overhead (the Cloud console default). Can, rarely, miss logs. |
| **Local logging: `Enable (sync)`** (`DATABASE_PERSISTENCE_POLICY_UNSPECIFIED`) | No (API default) | The API default—a version built over REST without `databasePersistencePolicy` persists synchronously. Guarantees execution logs are written before continuing, but adds execution latency. |
| **Local logging: `Disable`** (`DATABASE_PERSISTENCE_DISABLED`) | No | Generates no execution logs (and `REPLAY_MODE_POINT_OF_FAILURE` is refused because no execution snapshots are stored). **Nothing is sent to Cloud Logging even if Cloud Logging is enabled.** |
| **Cloud Logging** (`cloudLoggingDetails.enableCloudLogging`) | No (disabled by default) | Exports execution logs to the project's `_Default` bucket under `integrations.googleapis.com/IntegrationVersion`. |

### Critical Size and Truncation Rules

- **10 MB local-logging cutoff:** Total integration data (inputs, outputs, and variables) can be up to 30 MB, but **above 10 MB, local logging is automatically disabled**. The integration still runs, but you cannot view full logs, apply a task retry strategy, or see the run in the monitoring dashboard.
- **256 KiB Cloud Logging limit:** Each Cloud Logging entry is limited to 256 KiB. Above 256 KiB, request and response parameters are omitted from the log entry.
- **2,000-character message truncation:** Event parameters inside log messages are truncated at 2,000 characters. Use the Cloud console **Task Execution Details** pane (or download the execution log as JSON) to view untruncated task variables and request/response parameters.
- **Latency note:** Do not use the Execution Logs `Duration` column as end-to-end client latency; it excludes time spent on authentication and quota enforcement.

## Enabling Cloud Logging on an Integration

Cloud Logging is configured per integration version (`IntegrationVersion.cloudLoggingDetails`), while local logging corresponds to `IntegrationVersion.databasePersistencePolicy`: `DATABASE_PERSISTENCE_POLICY_UNSPECIFIED` = `Enable (sync)` (the API default—a version built over REST without `databasePersistencePolicy` persists synchronously), `DATABASE_PERSISTENCE_ASYNC` = `Enable (async)` (the console default), and `DATABASE_PERSISTENCE_DISABLED` = `Disable`.

1. Open the integration in `https://console.cloud.google.com/integrations` and switch to a **DRAFT** version (click **Enable Editing** if it is published).
2. Open **Integration summary / settings > Log settings**.
3. Enable **Cloud Logging**, choose a **Severity**, click **Save**, and **Publish** the version.

| Severity (`cloudLoggingSeverity`) | Execution states captured in Cloud Logging (`jsonPayload.integrationExecutionDetails.integrationExecutionState`) |
|---|---|
| `INFO` | All states: `SUCCEEDED`, `FAILED`, `IN_PROCESS`, `ON_HOLD`, `SUSPENDED`, `RETRY_ON_HOLD`, `CANCELLED` |
| `WARNING` | `FAILED` and `CANCELLED` only |
| `ERROR` | `FAILED` and `CANCELLED` only |

The Cloud Logging payload enum (`jsonPayload.integrationExecutionDetails.integrationExecutionState`) uses `ON_HOLD` and `IN_PROCESS` where the API and filter enum (`ExecutionDetails.state`) uses `PENDING` and `PROCESSING`; `FAILED`, `SUCCEEDED`, `CANCELLED`, `RETRY_ON_HOLD`, and `SUSPENDED` are the same as in the API.
Check whether Cloud Logging was enabled on a past run by reading `Execution.cloudLoggingDetails` via `executions.list`.

## Cloud Logging Queries (`gcloud logging read` and Logs Explorer)

All Application Integration execution logs use `resource.type="integrations.googleapis.com/IntegrationVersion"`. Audit logs are viewable only in Cloud Logging. Logs live in `_Default` by default and can be routed to other buckets, BigQuery, or Pub/Sub.

### Common Query Patterns

```text
# 1. All Application Integration logs in the project
resource.type="integrations.googleapis.com/IntegrationVersion"

# 2. One parent execution only (excludes child sub-executions)
resource.type="integrations.googleapis.com/IntegrationVersion"
jsonPayload.executionId="EXECUTION_ID"

# 3. Parent execution AND all child sub-executions (free-text match on EXECUTION_ID)
resource.type="integrations.googleapis.com/IntegrationVersion"
"EXECUTION_ID"

# 4. All runs for one integration
resource.type="integrations.googleapis.com/IntegrationVersion"
jsonPayload.integration="INTEGRATION_NAME"

# 5. Failed executions for one integration
resource.type="integrations.googleapis.com/IntegrationVersion"
jsonPayload.integration="INTEGRATION_NAME"
jsonPayload.integrationExecutionDetails.integrationExecutionState="FAILED"

# 6. Search by request parameter name (for example requestUrl)
resource.type="integrations.googleapis.com/IntegrationVersion"
"requestUrl"
```

### Running Queries with `gcloud logging read`

```bash
# Read failed execution logs for INTEGRATION_NAME
gcloud logging read \
  'resource.type="integrations.googleapis.com/IntegrationVersion" AND jsonPayload.integration="INTEGRATION_NAME" AND jsonPayload.integrationExecutionDetails.integrationExecutionState="FAILED"' \
  --project="PROJECT_ID" \
  --limit=25 \
  --format=json
```

### Tracing a Failed Integration Connectors Task

Connector logs are **disabled by default** on each connection. When enabled on the connection (levels: `Error`, `Info`, or `Debug`), every Connectors task attempt logs with a trace ID joining the integration execution ID, task ID, and attempt number.

```bash
# Query all logs for a specific connection in LOCATION
gcloud logging read \
  'resource.type="connectors.googleapis.com/Connection" AND resource.labels.location="LOCATION" AND resource.labels.connection="CONNECTION_NAME"' \
  --project="PROJECT_ID" \
  --limit=25 \
  --format=json

# Trace one exact Connectors task attempt (format: EXECUTIONID_TASKID_ATTEMPTNUMBER)
gcloud logging read \
  'resource.type="connectors.googleapis.com/Connection" AND jsonPayload.integration_connectors_trace_id="EXECUTIONID_TASKID_ATTEMPTNUMBER"' \
  --project="PROJECT_ID" \
  --limit=20 \
  --format=json
```

In the Cloud console Execution Logs table, clicking **Failed** in the Status column of a Connectors task opens Logs Explorer pre-populated with `jsonPayload.integration_connectors_trace_id`.

## Cloud Monitoring Metrics

Application Integration metrics are GA, sampled every 60 seconds (up to 86,400 seconds visibility delay), and emitted **only for published integrations**. Skipped tasks do not emit step counts. Metric values are informational and must not be used to calculate billing.

### Monitored Resource: `integrations.googleapis.com/IntegrationVersion`

- **Resource labels:** `resource_container` (project ID), `location`, `integration`, `version`.

| Metric (`integrations.googleapis.com/...`) | Kind / Type | Metric labels | What it measures |
|---|---|---|---|
| `integration/execution_count` | DELTA / INT64 | `status` (`SUCCEEDED`, `FAILED`, `CANCELLED`, `RETRY_ON_HOLD`), `trigger_name`, `trigger_id`, `error_enum` (for example `PERMISSION_DENIED`), `is_retry` | Total integration executions. |
| `integration/execution_latencies` | DELTA / DISTRIBUTION (ms) | `status`, `trigger_name`, `trigger_id`, `error_enum`, `is_retry` | Integration execution duration distribution. |
| `processed_bytes_count` | DELTA / INT64 (By) | `step_type`, `step_name`, `step_id` | Input/output parameter size plus Call REST Endpoint and Connectors task payload size. |
| `step/execution_count` | DELTA / INT64 | `status`, `step_type`, `step_name`, `step_id`, `error_enum`, `is_retry`, `is_step_external` | Task and trigger execution count (excludes skipped tasks). |
| `step/execution_latencies` | DELTA / DISTRIBUTION (ms) | `status`, `step_name`, `step_id`, `error_enum`, `is_retry`, `is_step_external` | Task and trigger execution duration distribution (no `step_type` label). |

### Integration Connectors Metrics (`connectors.googleapis.com/...` - Beta)

Monitored resource: `connectors.googleapis.com/Connection`.
- `connection/connection_status` (GAUGE / BOOL, label `status`)
- `connection/state`
- `connection/nodes`
- `connection/request_count`
- `connection/response_count` (labels: `code`, `service`, `method`, `connector_fault`)
- `connection/latencies`
- `connection/request_sizes` and `connection/response_sizes`
- `connection/event_count` and `connection/event_request_sizes`

## Dashboards and Alerting

- **Sample dashboards:** In Cloud Monitoring, open **Dashboards > Sample library > Application Integration** to install prebuilt views for:
  - Integration executions
  - Step executions
  - Integration and task execution duration
  - Data processed
- **Metric alerts:** Requires `roles/monitoring.editor`. Create an alert policy on resource **Integration Version** (`integrations.googleapis.com/IntegrationVersion`) filtered by `status="FAILED"` or `error_enum`.
- **Log-based alerts:** Create a Cloud Logging alert matching `resource.type="integrations.googleapis.com/IntegrationVersion"` and `jsonPayload.integrationExecutionDetails.integrationExecutionState="FAILED"`.
