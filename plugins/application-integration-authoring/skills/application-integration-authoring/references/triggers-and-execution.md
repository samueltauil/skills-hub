# Triggers and Execution Reference

This reference covers trigger types, `triggerId` formats, synchronous versus asynchronous execution, `:execute` and `:schedule` request and response schemas, OpenAPI spec generation, and resuming suspended runs.

- [Trigger Types and `triggerId` Formats](#trigger-types-and-triggerid-formats): Lines 12-30
- [Execution Modes (SYNC vs ASYNC)](#execution-modes-sync-vs-async): Lines 31-39
- [Comparing `:execute` and `:schedule`](#comparing-execute-and-schedule): Lines 40-70
- [Reading Execution Responses and Verifying Success](#reading-execution-responses-and-verifying-success): Lines 71-101
- [Generating OpenAPI Specifications](#generating-openapi-specifications): Lines 102-121
- [Resuming Suspended Executions (`suspensions:lift` and `suspensions:resolve`)](#resuming-suspended-executions-suspensionslift-and-suspensionsresolve): Lines 122-151

## Trigger Types and `triggerId` Formats

An integration can have multiple triggers. Each trigger starts from its own `startTasks` list, and simultaneous trigger events run separate copies of the integration.

| Trigger Type | `triggerType` Enum | Documented `triggerId` Format | Rules and Gotchas |
| :--- | :--- | :--- | :--- |
| API Trigger | `API` | `api_trigger/TRIGGER_NAME` | `TRIGGER_NAME` max 64 characters. Multiple API triggers allowed per integration (each unique). Max 8 MB total input variables. |
| Private Trigger | `PRIVATE_TRIGGER` | `private_trigger/TRIGGER_NAME` | Callable only from other integrations (not public REST APIs). Exempt like API triggers from the October 15, 2026 `runAsServiceAccount` rule, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount` (unless region governance is enabled). Cannot test while published (unpublish first). Shares the 30 MB data limit with the parent integration. |
| Cloud Pub/Sub | `CLOUD_PUBSUB_EXTERNAL` | Configured via topic | Topic format `projects/PROJECT_ID/topics/TOPIC_ID`. Auto-creates a Pub/Sub subscription on publish (billed at Pub/Sub rates). New or modified Pub/Sub triggers require a trigger service account (the identity that invokes the integration at runtime); integrations created on or after October 15, 2026 with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce, or Connector Event) cannot be tested or published unless `runAsServiceAccount` is set (whenever `runAsServiceAccount` is set, the user publishing or testing the version needs `roles/iam.serviceAccountUser` on it, and at runtime the trigger service account needs `roles/iam.serviceAccountUser` on it). Outputs `CloudPubSubMessage` (JSON). |
| Schedule | `CRON` | Configured via cron | 5-field cron expression. Runs cannot be canceled or replayed. Google recommends the Cloud Scheduler trigger for higher reliability. |
| Cloud Scheduler | `CLOUD_SCHEDULER` | Configured via scheduler | Requires Cloud Scheduler API (`cloudscheduler.googleapis.com`, billed separately). Supports cross-region scheduling. Editing it in Application Integration overwrites the cron job in a new integration version. Requires `runAsServiceAccount`. |
| Salesforce | `SFDC_CHANNEL` / `SFDC_CDC_CHANNEL` | Configured via channel | Event-driven Salesforce channel or Change Data Capture trigger. Runs asynchronously. |
| Webhook (Preview) | `INTEGRATION_CONNECTOR_TRIGGER` | Connector subscription | Needs an Integration Connectors Webhook connection with an event subscription. Accepts JSON payloads only. Outputs `ConnectorEventPayload`. |
| Connector Event | `INTEGRATION_CONNECTOR_TRIGGER` | Connector subscription | Supported for Apache Kafka, Azure AD, HubSpot, IBM MQ, Jira Cloud, Jira Server Data Center, HL7, RabbitMQ, SAP ERP, SAP Gateway, ServiceNow, Solace, TIBCO EMS, Webhook, and Zendesk. |
| Error Catcher | Error catcher config | Referenced by `errorCatcherId` | One catcher per `errorCatcherId`. Cannot attach multiple catchers to one task or trigger. Cannot nest catchers. No edges can connect catcher tasks back to the main flow. |

- **Public REST invocation**: Only `api_trigger/TRIGGER_NAME` is used with public `integrations:execute` and `integrations:schedule`. Trigger ID formats for Pub/Sub, Schedule, Cloud Scheduler, and Salesforce triggers are not documented for direct public REST calls.
- **Run-as service account requirement (October 15, 2026+)**: Integrations created on or after October 15, 2026 with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce, or Connector Event) cannot be tested or published unless `runAsServiceAccount` is set. Private triggers are exempt like API triggers, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount` (unless region governance is enabled). Whenever `runAsServiceAccount` is set, the user publishing or testing the version needs `roles/iam.serviceAccountUser` on it (and at runtime, the invoking caller or trigger service account needs `roles/iam.serviceAccountUser` on it).

## Execution Modes (SYNC vs ASYNC)

| Mode | How It Is Started | Execution Timeout | Max Lifetime |
| :--- | :--- | :--- | :--- |
| **SYNC** | `integrations:execute`, Call Integration task in SYNC mode, Timer task < 60 seconds | **2 minutes** (status becomes `CANCELLED` on timeout) | 2 minutes |
| **ASYNC** | `integrations:schedule`, Schedule trigger, Cloud Scheduler trigger, Cloud Pub/Sub trigger, Salesforce trigger, Call Integration task in ASYNC mode, Timer task >= 60 seconds, and **any execution resumed from a suspension or approval** | **10 minutes** | **31 days** (including pause time in Suspend or Approval tasks) |

- **Resumed runs always switch to ASYNC**: Even if an integration started synchronously via `integrations:execute`, once it pauses at a `Suspend` or `Approval` task and resumes, the remainder of the run executes in asynchronous mode.

## Comparing `:execute` and `:schedule`

### 1. Synchronous Execution (`integrations:execute`)

- **Endpoint**: `POST https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME:execute`
- **State requirement**: The integration must have an `ACTIVE` (published) version. To test an integration before production, publish the version in a non-production project (`versions:publish`) and invoke `integrations:execute` there.
- **Wildcard `-`**: Passing `-` as `INTEGRATION_NAME` (`/integrations/-:execute`) runs **every** published integration in that region that has the matching `triggerId`.
- **Timeout header**: Set `X-Server-Timeout: SECONDS` (default `120`; max synchronous runtime is 2 minutes).

| Request Body Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `triggerId` | string | Yes | `api_trigger/TRIGGER_NAME`. |
| `inputParameters` | map (`string` -> `ValueType`) | No | Input variables (max 8 MB cumulative for API triggers). |
| `requestId` | string | No | Deduplication token. Sending a duplicate `requestId` returns the previous execution's response without re-running. |
| `doNotPropagateError` | boolean | No | Default `false`. When `true`, returns HTTP 200 with an `ExecuteIntegrationsResponse` containing `executionId` and error details instead of throwing an HTTP error. |

### 2. Asynchronous Execution (`integrations:schedule`)

- **Endpoint**: `POST https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME:schedule`
- **State requirement**: The integration must have an `ACTIVE` (published) version.

| Request Body Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `triggerId` | string | Yes | `api_trigger/TRIGGER_NAME`. |
| `scheduleTime` | string (RFC 3339 Timestamp) | No | When to run (for example, `"2026-10-17T20:00:00Z"`). If omitted or <= current time, runs immediately in async mode. |
| `inputParameters` | map (`string` -> `ValueType`) | No | Input variables mapped to `ValueType`. |
| `requestId` | string | No | Deduplication token. |
| `userGeneratedExecutionId` | string | No | Custom UUID string (at most 36 characters, alphanumerics and hyphens only) used as the `executionId`. |

- **Response (`ScheduleIntegrationsResponse`)**: Returns `{"executionInfoIds": ["EXECUTION_ID"]}`. Poll or inspect completion via `executions.list`.

## Reading Execution Responses and Verifying Success

`ExecuteIntegrationsResponse` returns `executionId`, `outputParameters`, and `parameters`:

```json
{
  "executionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "outputParameters": {
    "`ExecutionId`": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "orderStatus": "PROCESSED"
  },
  "parameters": {
    "orderStatus": {
      "stringValue": "PROCESSED"
    }
  }
}
```

### Verification Checklist After `:execute`

1. **Verify the execution record (`executions.list`)**: Do not rely on HTTP 200 alone (or the legacy, deprecated `executionFailed` field, which is not a supported public signal). Query the execution record by `executionId`:
   ```bash
   curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/-/executions?filter=execution_id%3D%22EXECUTION_ID%22"
   ```
   Check `executionDetails.state` (`PENDING`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `RETRY_ON_HOLD`, `SUSPENDED`) and each task's `taskExecutionState` (`SUCCEED`, `FAILED`, `FATAL`, `SKIPPED`, `SUSPENDED`, and so on).
2. **Do not trust HTTP 200 or `SUCCEEDED` without checking task states**: If a task has `failurePolicy.retryStrategy` set to `IGNORE` ("assumes this task succeeded") or `NONE` with an alternate branch, the integration can still return HTTP 200 and state `SUCCEEDED` even though a task failed.
3. **Check system keys in `outputParameters`**: System-generated variable names inside `outputParameters` are wrapped in backticks (for example, `` `ExecutionId` ``, `` `ErrorInfo` ``). User-defined output variables use their plain `key` name.
4. **Check `ErrorInfo` on errors**: Without `doNotPropagateError: true`, a failed `:execute` call throws an HTTP error rather than returning response parameters. Per the API reference, when `doNotPropagateError` is `true` on `:execute`, errors are returned in event parameters (`PostWithTriggerIdExecutionException`), while the `ErrorInfo` shape (`{"ErrorInfo": {"message": "...", "code": 400}}`) is documented on the execution record (`Execution.responseParameters`).

## Generating OpenAPI Specifications

You can generate an OpenAPI 3.0.1 specification for published integrations that use API triggers in a single region (`fileFormat` accepts `"JSON"` or `"YAML"`):

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "apiTriggerResources": [{
      "integrationResource": "INTEGRATION_NAME",
      "triggerId": ["api_trigger/TRIGGER_NAME"]
    }],
    "fileFormat": "JSON"
  }' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION:generateOpenApiSpec"
```

ADK (`ApplicationIntegrationToolset`) roles depend on mode. In **integration mode**, `ApplicationIntegrationToolset` calls `POST .../locations/LOCATION:generateOpenApiSpec` automatically when turning published API-triggered integrations into agent tools; calling `:generateOpenApiSpec` requires `integrations.integrations.generateOpenApiSpec` (included in `roles/integrations.integrationViewer` and `roles/integrations.integrationEditor`, but **not** in `roles/integrations.integrationInvoker`), so grant `roles/integrations.integrationInvoker` + `roles/integrations.integrationViewer` as the least-privilege combination for integration mode (use `roles/integrations.integrationEditor` only as the broad option—it also grants version create, update, delete, and publish permissions, and holds no `connectors.*` permissions). In **connection mode**, the toolset does **not** call `:generateOpenApiSpec` (so `roles/integrations.integrationViewer` is only needed in integration mode); instead, when constructed using the agent's own credentials, it calls `GET .../connections/CONNECTION?view=BASIC`, `connectionSchemaMetadata:getEntityType`, and `connectionSchemaMetadata:getAction`, which require `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata` (`roles/connectors.viewer` has both; `roles/connectors.invoker` does **not**). Grant `roles/integrations.integrationInvoker` (to `:execute` the `ExecuteConnection` integration) + `roles/connectors.viewer` (or a custom role with `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata`) for connection mode. `roles/secretmanager.secretAccessor` is not needed for the toolset itself (the ADK client does not read Secret Manager).

## Resuming Suspended Executions (`suspensions:lift` and `suspensions:resolve`)

An execution paused at a **Suspend** or **Approval** task waits until its expiration timer elapses (up to 44,640 minutes / 31 days) or until resolved via the Suspensions REST API (or the Cloud console UI). Once resumed, the remainder of the execution runs asynchronously. Always confirm with the user before lifting or resolving a suspension.

- **Required IAM**: `integrations.suspensions.resolve` for `suspensions:resolve` (Approval), `integrations.suspensions.lift` for `suspensions:lift` (Suspend), and `integrations.suspensions.list` for `suspensions.list` (all three are included in `roles/integrations.suspensionResolver` and `roles/integrations.integrationAdmin`, and none are in `roles/integrations.integrationEditor`; `roles/integrations.suspensionResolver` alone cannot read execution records, so also grant `roles/integrations.integrationViewer` to inspect `taskExecutionDetails` or run `:troubleshoot`, or use the approval email link, which carries the execution and task IDs) **plus** `roles/iam.serviceAccountUser` on the integration's `runAsServiceAccount`.
- **Approve or reject an Approval task (`suspensions:resolve`)** — this is the same call the Cloud console Approve/Reject buttons make (confirm with user before running):
  ```bash
  curl -sS --fail-with-body -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "suspension": {
        "eventExecutionInfoId": "EXECUTION_ID",
        "integration": "INTEGRATION_NAME",
        "taskId": "TASK_ID",
        "state": "LIFTED"
      }
    }' \
    "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions/SUSPENSION_ID:resolve"
  ```
  Pass `"state": "LIFTED"` to approve or `"state": "REJECTED"` to reject (`Suspension.state` enum values: `PENDING`, `REJECTED`, `LIFTED`).
- **Lift a Suspend task (`suspensions:lift`)** — the Suspend-task variant, which accepts an optional `suspensionResult` (defaults to `Resolved`, or `Expired` on timeout; `-` can replace `INTEGRATION_NAME` and either `EXECUTION_ID` or `SUSPENSION_ID`, provided at least one of `EXECUTION_ID` or `SUSPENSION_ID` is concrete—omitting both returns an error; confirm with user before running):
  ```bash
  # Both IDs known (or replace INTEGRATION_NAME with "-" and either EXECUTION_ID or SUSPENSION_ID with "-")
  curl -sS --fail-with-body -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{"suspensionResult": "Approved"}' \
    "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions/SUSPENSION_ID:lift"
  ```
