# Common Errors: IAM, Run-As Service Account, Quotas, Tasks, and ADK

Use this reference to diagnose HTTP/gRPC error codes, 403 permission denials, the October 15, 2026 run-as service account requirement, missing APIs, quotas and timeouts, task gotchas, and ADK `ApplicationIntegrationToolset` errors.

- [HTTP and gRPC Error Codes](#http-and-grpc-error-codes): Lines 13-27
- [Two-Sided 403 `PERMISSION_DENIED` Diagnosis](#two-sided-403-permission_denied-diagnosis): Lines 28-70
- [October 15, 2026 Run-As Service Account Requirement](#october-15-2026-run-as-service-account-requirement): Lines 71-80
- [APIs Not Enabled](#apis-not-enabled): Lines 81-90
- [Quotas, Timeouts, and Data Limits](#quotas-timeouts-and-data-limits): Lines 91-106
- [Task-Specific Configuration Gotchas](#task-specific-configuration-gotchas): Lines 107-118
- [ADK (`ApplicationIntegrationToolset`) Troubleshooting](#adk-applicationintegrationtoolset-troubleshooting): Lines 119-129

## HTTP and gRPC Error Codes

| HTTP | `google.rpc.Code` | Common cause in Application Integration |
|---|---|---|
| `400` | `FAILED_PRECONDITION` / `INVALID_ARGUMENT` | Invalid request payload, parameter type mismatch, or failed precondition. |
| `401` | `UNAUTHENTICATED` | Missing, invalid, or expired OAuth access token. Refresh with `gcloud auth print-access-token`. |
| `403` | `PERMISSION_DENIED` | Missing caller IAM role, missing `roles/iam.serviceAccountUser` on the run-as service account, run-as SA missing downstream access, wrong OAuth scope, or required API not enabled. |
| `404` | `NOT_FOUND` | Wrong `PROJECT_ID`, `LOCATION`, `INTEGRATION_NAME`, `VERSION_ID`, or `CONNECTION_NAME`. |
| `409` | `ALREADY_EXISTS` | Resource already exists. |
| `409` | `ABORTED` | `Response size is too large`. |
| `429` | - | Integration Connectors connection exceeded its provisioned nodes (throttling). |
| `500` | `INTERNAL` | Often caused when a task or trigger in the integration is misconfigured. Check per-task `ErrorInfo` and task parameters. |
| `501` | `UNIMPLEMENTED` | API method not implemented by the server. |
| `503` | `UNAVAILABLE` | Transient backend or network unavailability; retry with backoff. |

## Two-Sided 403 `PERMISSION_DENIED` Diagnosis

Every integration run evaluates **two separate identities**. Fixing only one leaves the 403 in place.

1. **Caller / trigger identity** (the user or service account calling `:execute`, `:schedule`, `:publish`, or firing the trigger).
2. **Run-as service account** (`IntegrationVersion.runAsServiceAccount`, or the default Application Integration service agent `service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com` on older integrations without one).

### Required IAM Roles by Action

| Action | Required role on caller | Additional role when `runAsServiceAccount` is set |
|---|---|---|
| View integration | `roles/integrations.integrationViewer` | - |
| View execution logs | `roles/integrations.integrationViewer` or `roles/integrations.integrationInvoker` (**not** in `roles/integrations.suspensionResolver`) | - |
| Run / invoke (`:execute`, `:schedule`) | `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, or `roles/integrations.integrationAdmin` (`integrations.integrations.invoke`) | `roles/iam.serviceAccountUser` on `runAsServiceAccount` |
| Replay execution (`:replay`) | `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, or `roles/integrations.integrationAdmin` (`integrations.executions.replay`; **not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`) | `roles/iam.serviceAccountUser` on `runAsServiceAccount` |
| Cancel execution (`:cancel`) | `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, or `roles/integrations.integrationAdmin` (`integrations.executions.cancel`; **not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`, so approvers with only `roles/integrations.suspensionResolver` cannot cancel a stuck `SUSPENDED` run) | - |
| Edit or test draft | `roles/integrations.integrationEditor` | `roles/iam.serviceAccountUser` on `runAsServiceAccount` (for the user testing the version) |
| Publish / unpublish | `roles/integrations.integrationDeployer` or `roles/integrations.integrationEditor` (plus `roles/integrations.serviceAgent` on the Application Integration service agent) | `roles/iam.serviceAccountUser` on `runAsServiceAccount` (for the user publishing the version) |
| List, approve (`:resolve`), or lift (`:lift`) suspension | `roles/integrations.suspensionResolver` or `roles/integrations.integrationAdmin` (`integrations.suspensions.list` for `suspensions.list`, `integrations.suspensions.resolve` for `:resolve` [Approval], `integrations.suspensions.lift` for `:lift` [Suspend]). `roles/integrations.suspensionResolver` alone cannot read execution records (no `integrations.executions.list` or `integrations.executions.get`, returning HTTP 403 on `executions.list` and v2 `:troubleshoot`); to inspect `taskExecutionDetails` (or run `:troubleshoot`), also grant `roles/integrations.integrationViewer` (or use the approval email link, which carries the execution and task IDs). | `roles/iam.serviceAccountUser` on `runAsServiceAccount` |

### Typical Error Message and Trigger Behavior

Typical error:
`PRINCIPAL needs roles/iam.serviceAccountUser on SERVICE_ACCOUNT (or its project) to run this integration.`

How each trigger surfaces a run-as service account (`roles/iam.serviceAccountUser`) 403:
- **API trigger (`:execute`):** returns HTTP 403 directly to the caller. **Nothing appears in Execution Logs.**
- **Cloud Pub/Sub, Eventarc, and Connector Event triggers:** records a `FAILED` execution in logs, and **the event is not redelivered**.
- **Cloud Scheduler trigger:** reports `PERMISSION_DENIED` in Cloud Scheduler logs.

### Why a 403 Persists After Granting IAM

- **Wrong project:** `roles/iam.serviceAccountUser` must be granted on the service account (or in the project that **owns** that service account), not necessarily the integration's project.
- **Propagation delay:** IAM binding changes take a short time to propagate.
- **Second service account:** an authentication profile (`authConfig`) or a called sub-integration uses a different service account.
- **Wrong trigger principal:** for Cloud Scheduler, Cloud Pub/Sub, Eventarc, or Integration Connectors event triggers, the principal that needs `roles/iam.serviceAccountUser` is the trigger's service account, not your user account.
- **IAM conditions:** a condition on the binding does not match the integration resource.

```bash
# Inspect IAM policy on the run-as service account (read-only)
gcloud iam service-accounts get-iam-policy "RUN_AS_SA_EMAIL" --project="SA_OWNER_PROJECT_ID"
```

## October 15, 2026 Run-As Service Account Requirement

- **Rule:** For integrations created on or after **October 15, 2026** (and for existing integrations at a later date), every execution requires an explicit identity (either the triggering user or a run-as service account set per integration version via `IntegrationVersion.runAsServiceAccount`; region provisioning via `clients:provision` does not apply `runAsServiceAccount`).
- **Triggers other than API or Private:** Integrations created on or after **October 15, 2026** with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce, or Connector Event) cannot be tested or published unless `runAsServiceAccount` is set (Private triggers are exempt like API triggers, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount`); whenever `runAsServiceAccount` is set on a version, the user publishing or testing the version needs `roles/iam.serviceAccountUser` on it (and at runtime, the invoking caller or trigger service account needs `roles/iam.serviceAccountUser` on it).
- **Governance mode:** If governance is enabled on the region, a run-as service account is mandatory for all new integrations and versions regardless of trigger type.
- **Token precedence on tasks:** For Connector, Call REST Endpoint, and Cloud Function tasks:
  1. If an OAuth 2.0 / OIDC authentication profile (`authConfig`) is attached to the task, it takes precedence.
  2. Otherwise, if `runAsServiceAccount` is set on the version, it mints the token.
  3. On legacy integrations with neither set, the default Application Integration service agent (`service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com`) is used.

## APIs Not Enabled

Missing APIs surface as HTTP 403 `PERMISSION_DENIED`.

- **Application Integration core:** `integrations.googleapis.com`, `secretmanager.googleapis.com`, `connectors.googleapis.com`
- **CMEK regions:** `cloudkms.googleapis.com`
- **Cloud Scheduler triggers:** `cloudscheduler.googleapis.com`

Ask the user for confirmation before enabling any missing API with `gcloud services enable`.

## Quotas, Timeouts, and Data Limits

| Limit / Quota | Value | Failure symptom |
|---|---|---|
| **SYNC execution timeout** | 2 minutes | Status becomes `CANCELLED` after 2 minutes (includes external calls and sub-integrations). |
| **ASYNC execution timeout** | 10 minutes | Execution fails or cancels at 10 minutes. |
| **`:execute` HTTP timeout** | 120 seconds default | Controlled by `X-Server-Timeout` request header. |
| **Max execution lifetime** | 31 days (44,640 min) | Includes time paused in Approval or Suspend tasks. |
| **Concurrent executions** | 50 per project per region; 10 per integration (defaults) | Both caps are adjustable. A burst on a single integration hits the 10-per-integration cap, not 50. Backoff retry concurrency also defaults to 50 per project and region. |
| **Execution rate** | Shown on Cloud Quotas page | The execution request rate quota is shown on the Cloud Quotas page for the project and can be adjusted there. |
| **Execution-log reads** | 18,000 reads / minute | Rate limit on reading execution logs. |
| **Max cumulative integration data** | 30 MB | Shared between parent and Private-trigger sub-integration. Above 10 MB, local logging is disabled. |
| **API trigger input size** | 8 MB | Cumulative input variables > 8 MB prevent execution from starting. |
| **Connectors task timeout & size** | 3 minutes; 8 MB to/from connection (Application Integration quota) | Max 10 MB Connectors task payload (Integration Connectors quota); max 20 MB connector response; custom query max 180 s and 50,000 rows. |
| **Publish eventual consistency** | Up to 10 minutes | An older published version can keep running for up to 10 minutes after publishing a new version. |

## Task-Specific Configuration Gotchas

- **Call REST Endpoint:** reaches public internet hosts only (no VPC-private hosts); fails on HTTP 4xx/5xx; max 20 MB request and 34 MB response; max 100 concurrent calls. **Gotcha:** if you change the task's authentication profile, publish the version before testing (for example, in a non-production project via `:execute`) so the updated profile takes effect.
- **Cloud Function task:** stops working if VPC Service Controls is enabled for Application Integration; an OIDC profile overrides a user-managed service account; function code must follow the required `main.py` / `task.py` template.
- **Data Mapping task:** input and output types must match (use `TO_STRING`, `TO_INT`, etc.); null inputs cause an error unless a fallback value is configured; arrays max 100,000 elements; JSON/string variables max 20 MB.
- **Data Transformer Script (Preview):** Jsonnet identifiers cannot contain hyphens; 300 MB evaluation memory limit.
- **JavaScript task:** Rhino is deprecated (use V8); do not delete `executesScript(event)`; max 25 MB script request size.
- **Private trigger:** cannot test a published Private-trigger workflow (unpublish it first to test, or call it from a parent integration).
- **Call Integration / Loops:** callee must have an API trigger or a Private trigger (Private triggers are invokable only from other integrations); caller SA needs `roles/integrations.integrationInvoker`. Child responses/output parameters are returned to the parent only in SYNC mode (ASYNC calls return no output parameters). For Each Loop and While Loop max 8,000 iterations. For Each Parallel max 10,000 iterations (default parallelism 50); avoid SYNC mode if the sub-integration takes > 2 minutes or has an Approval task; choosing "run all integrations with this trigger ID" makes sub-integration responses unavailable.
- **Error Catcher:** cannot nest error catchers; only one catcher per task or trigger; cannot draw edges from error catcher tasks back into the main workflow.
- **Config variables:** stored in plain text on download and template export (not a secret store; use an auth profile or Secret Manager task for credentials). Keys in `configParameters` on `versions:publish` must **exactly match** a key in `integrationConfigParameters`, backticks included (for example, `` "`CONFIG_target_url`" ``); unknown keys are **silently ignored**, not rejected (`versions:publish` returns 200 and the default stays). Cannot parameterize connector entity operations or actions.

## ADK (`ApplicationIntegrationToolset`) Troubleshooting

| Error / Symptom | Cause | Fix |
|---|---|---|
| `ValueError: Invalid request, Either integration or (connection and (entity_operations or actions)) should be provided.` | Missing constructor arguments in Python (in Java, `IllegalArgumentException` is emitted via `Flowable.error` from `getTools()`). | Pass `integration="..."` and `triggers=["api_trigger/..."]` (or `triggers=[]` for all API triggers; omitting `triggers` raises `Exception: An unexpected error occurred: Integration name and triggers are required to generate an integration OpenAPI spec.`), or pass `connection="..."` with `entity_operations` or `actions`. |
| `ValueError: Invalid request. Please check the provided values of project(...), location(...), integration\|connection(...)` | Underlying API returned HTTP 400 or 404. | Verify `project`, `location`, and resource names. For connector mode, Application Integration must be provisioned in the **same region** as the connection. |
| `Exception: An unexpected error occurred: Please provide a service account that has the required permissions to access the connection.` | Application Default Credentials (ADC) missing or expired. | Run `gcloud auth application-default login` (changes host or credential state; get the user's approval first), or pass `service_account_json`. |
| HTTP 403 in integration mode or connection mode (anywhere the agent runs, including Agent Runtime) | Required IAM roles depend on mode. **Integration mode**: `ApplicationIntegrationToolset` fetches the tool schema via `POST .../locations/LOCATION:generateOpenApiSpec`, which requires `integrations.integrations.generateOpenApiSpec` (`roles/integrations.integrationViewer` and `roles/integrations.integrationEditor` include it; `roles/integrations.integrationInvoker` does **not**, so `integrationInvoker` alone fails with 403 wherever the agent runs). **Connection mode**: When constructed and using the agent's own credentials, the toolset calls `GET .../connections/CONNECTION?view=BASIC`, `connectionSchemaMetadata:getEntityType`, and `connectionSchemaMetadata:getAction`, which require `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata` (`roles/connectors.viewer` has both; `roles/connectors.invoker` does **not**, and `roles/integrations.integrationEditor` holds no `connectors.*` permissions). Connection mode does **not** call `:generateOpenApiSpec`. | **Integration mode**: grant `roles/integrations.integrationInvoker` + `roles/integrations.integrationViewer` (`roles/integrations.integrationEditor` only as the broad option—it also grants version create/update/delete/publish and holds no `connectors.*` permissions). **Connection mode**: grant `roles/integrations.integrationInvoker` (to `:execute` the `ExecuteConnection` integration) + `roles/connectors.viewer` (or a custom role with `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata`; `integrationViewer` is only needed in integration mode). `roles/secretmanager.secretAccessor` is not needed for the toolset itself (the ADK client does not read Secret Manager). |
| Connector mode fails to find workflow | Missing `ExecuteConnection` integration. | Connector mode requires a published integration named `ExecuteConnection` (created from the Connection Tool template) in the connection's region, or `connection_template_override` (ADK Python v1.21.0+). |
| `tool_name_prefix` / `tool_instructions` ignored | Passed with `integration=...`. | Those parameters apply only when passing `connection=...`; on the `integration=` path they are silently ignored. |
| Dynamic OAuth (`auth_scheme` / `auth_credential`) ignored | Connection lacks override support. | Enable `authOverrideEnabled` on the Integration Connectors connection; otherwise ADK logs a warning and ignores dynamic credentials. |
