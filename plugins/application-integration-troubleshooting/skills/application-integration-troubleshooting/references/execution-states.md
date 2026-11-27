# Execution States, Listing Filters, Cancel, and Replay

Use this reference to interpret execution-level and task-level states, inspect executions through `executions.list`, run v2 AI troubleshooting, and safely cancel or replay runs.

- [Why HTTP 200 Does Not Prove Every Task Succeeded](#why-http-200-does-not-prove-every-task-succeeded): Lines 13-32
- [Execution-Level States (`ExecutionDetails.state`)](#execution-level-states-executiondetailsstate): Lines 33-47
- [Execution Methods (`Execution.executionMethod`)](#execution-methods-executionexecutionmethod): Lines 48-58
- [Task-Level States (`TaskExecutionDetails.taskExecutionState`)](#task-level-states-taskexecutiondetailstaskexecutionstate): Lines 59-78
- [Listing and Filtering Executions (`executions.list`)](#listing-and-filtering-executions-executionslist): Lines 79-121
- [AI Troubleshooting (`v2` `executions:troubleshoot`)](#ai-troubleshooting-v2-executionstroubleshoot): Lines 122-134
- [Canceling and Replaying Executions](#canceling-and-replaying-executions): Lines 135-179

## Why HTTP 200 Does Not Prove Every Task Succeeded

An HTTP 200 return from `integrations.execute` means the synchronous API request finished, not necessarily that every task in the workflow succeeded. Treat HTTP 200 as a transport status and always check the payload and execution record:

- **Inspect the execution record (`executions.list`):** Query `executions.list?filter=execution_id="EXECUTION_ID"` and check `executionDetails.state` and each task's `taskExecutionState` in `executionSnapshots` (do not rely on the legacy/deprecated `executionFailed` response field, which is not a supported public signal).
- **Check `doNotPropagateError`:** When `ExecuteIntegrationsRequest.doNotPropagateError` is `true`, a failing execution does not return an HTTP error. Instead, it returns HTTP 200 with an `executionId` and places error messages inside the event parameters.
- **Check `ErrorInfo` in `responseParameters`:** On failure, `Execution.responseParameters` includes:
  ```json
  {
    "ErrorInfo": {
      "message": "Error description",
      "code": 403
    }
  }
  ```
- **Check `requestId` deduplication:** If `ExecuteIntegrationsRequest.requestId` matches a previous request, Application Integration returns the previous execution's response without running the tasks again.
- **Check task failure policies (`FailurePolicy.retryStrategy`):**
  - `IGNORE` ignores the task failure and runs the rest of the integration as if the task succeeded.
  - `NONE` (also applied when no `FailurePolicy` is set) stops dependent tasks on that branch, but an alternate branch can still finish and mark the overall execution `SUCCEEDED`.

## Execution-Level States (`ExecutionDetails.state`)

`Execution.executionDetails.state` tracks the overall run. It also holds `attemptStats` (start and end time of each attempt), `executionSnapshots`, and `eventExecutionSnapshotsSize`.

| API `ExecutionDetails.state` | Console Execution Logs status | Terminal? | Meaning |
|---|---|---|---|
| `STATE_UNSPECIFIED` | - | No | Default unspecified enum value. |
| `PENDING` | On hold | No | Scheduled or temporarily paused and waiting to be triggered. |
| `PROCESSING` | In process | No | Currently running. |
| `SUCCEEDED` | Succeeded | Yes | Completed without an unhandled fatal error. Verify per-task states if expected side effects are missing. |
| `FAILED` | Failed | Yes | Ended with an unhandled failure. Check `ErrorInfo` and per-task states. |
| `CANCELLED` | Canceled | Yes | Canceled by a user, canceled when a new version was published over a suspended run, or timed out (for example, SYNC > 2 min or replay > 10 min). |
| `RETRY_ON_HOLD` | Retry on hold | No | Failed with a temporary error and waiting in the backoff retry queue. |
| `SUSPENDED` | Suspended | No | Waiting for resolution of an Approval task (in the Cloud console UI or via `suspensions:resolve`) or a Suspend task (via `suspensions:lift`). |

## Execution Methods (`Execution.executionMethod`)

| `Execution.executionMethod` | Execution mode | Description |
|---|---|---|
| `EXECUTION_METHOD_UNSPECIFIED` | - | Default value. |
| `POST` | Synchronous (`SYNC`) | Sync post. |
| `POST_TO_QUEUE` | Asynchronous (`ASYNC`) | Async post. |
| `SCHEDULE` | Asynchronous (`ASYNC`) | Async post with schedule time. |

Synchronous runs include console test/publish, `projects.locations.integrations.execute`, and synchronous Call Integration sub-workflows. Asynchronous runs include Schedule, Cloud Scheduler, Cloud Pub/Sub, and Salesforce triggers, `projects.locations.integrations.schedule`, and executions resumed after a suspension or approval.

## Task-Level States (`TaskExecutionDetails.taskExecutionState`)

Inspect `taskExecutionState` inside each execution snapshot to see exactly which task failed or was skipped.

| `taskExecutionState` | Meaning |
|---|---|
| `TASK_EXECUTION_STATE_UNSPECIFIED` | Default value. |
| `PENDING_EXECUTION` | Task has not started yet. |
| `IN_PROCESS` | Task is currently executing. |
| `SUCCEED` | Task completed successfully. |
| `FAILED` | Task failed. Check its `FailurePolicy` (`IGNORE`, `NONE`, or backoff retry) to see how the workflow handled it. |
| `FATAL` | Task failed with strategy `FATAL`, causing the entire integration execution to fail immediately. |
| `RETRY_ON_HOLD` | Task failed and is waiting for its next retry attempt. |
| `SKIPPED` | Task edge precondition was not met, or the execution was canceled before reaching this task. |
| `CANCELLED` | Task execution was canceled. |
| `PENDING_ROLLBACK` | Task is queued for rollback. |
| `ROLLBACK_IN_PROCESS` | Task rollback is currently running. |
| `ROLLEDBACK` | Task rollback finished. |
| `SUSPENDED` | A SuspensionTask (Suspend or Approval) ran once and created a pending suspension. |

## Listing and Filtering Executions (`executions.list`)

`GET https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions` returns the same execution records shown in the Cloud console Execution Logs page. Pass `-` for `INTEGRATION_NAME` to query across all integrations in `LOCATION`.

### Supported `filter` Fields and Operators

| Filter field | Supported operators | Example |
|---|---|---|
| `state` | `=`, `!=` | `state=FAILED` or `state!=SUCCEEDED` (unquoted `ExecutionDetails.state` value: `PENDING`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `RETRY_ON_HOLD`, `SUSPENDED`; for example, `filter=state=FAILED`, `filter=state=CANCELLED`, or `filter=state=FAILED OR state=CANCELLED`, URL-encoded as needed) |
| `workflow_name` | `=` | `workflow_name="INTEGRATION_NAME"` |
| `execution_id` | `=` | `execution_id="EXECUTION_ID"` |
| `trigger_id` | `=` | `trigger_id="api_trigger/TRIGGER_NAME"` |
| `update_time` | Supported filter key (operators are documented only for `CreateTimestamp`: `=`, `<`, `>`; `state`: `=`, `!=`) | - |
| `CreateTimestamp` | `=`, `<`, `>` | `CreateTimestamp>"TIMESTAMP"` (illustrative; value format is not specified in the discovery doc) |
| `parameter_type` | `=`, `HAS` | `"parameter_type" HAS "string"` |

Combine clauses with `AND`, `OR`, and `NOT` (for example, `state=FAILED OR state=CANCELLED`, or `trigger_id="api_trigger/TRIGGER_NAME" AND workflow_name="INTEGRATION_NAME"`). Use the supported filter keys (`execution_id`, `state`, `update_time`, `workflow_name`, `trigger_id`, `CreateTimestamp`, `parameter_type`); camelCase variants such as `executionId` are not supported even though some docs examples show them. Use `state`, not `eventExecutionState` (as shown on the REST reference page) or `event_execution_state` (in the API reference's filter description).

### Useful Query Parameters

- `filter`: filters executions using the fields above (such as `state=FAILED` or `execution_id="EXECUTION_ID"`, URL-encoded as needed).
- `snapshotMetadataWithoutParams=true`: returns lightweight execution metadata and IDs without large parameter payloads.
- `readMask`: limits returned fields (for example, `execution_details.state,cloud_logging_details,replay_info`).
- `orderBy=create_time`: orders runs by creation time (sort direction is not specified in the discovery doc; paginate with `pageToken` or add a `CreateTimestamp` filter if needed).
- `pageSize` and `pageToken`: paginates through results.
- **Deprecated query parameters to avoid:** Do **not** use `truncateParams` (deprecated, `"Only works for UI"`) or `filterParams.*` (deprecated, internal-only). Use `filter`, `snapshotMetadataWithoutParams=true`, and `readMask` instead.

### Handling "Response size too large" (> 300 MB)

If an execution's logs exceed 300 MB, the Cloud console shows `Response size too large`. Bypass this by calling `executions.list` with `snapshotMetadataWithoutParams=true` or a narrow `readMask`, then inspect specific task variables or Cloud Logging entries.

### Example: Two-Step Execution Lookup

```bash
# Step 1: List recent failed executions without parameter payloads
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions?filter=state%3DFAILED&snapshotMetadataWithoutParams=true&pageSize=20"

# Step 2: Fetch full details for one EXECUTION_ID across any integration in LOCATION
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/-/executions?filter=execution_id%3D%22EXECUTION_ID%22"
```

## AI Troubleshooting (`v2` `executions:troubleshoot`)

The v2 REST API provides an LLM-powered root-cause explanation for a failed execution. It requires `integrations.executions.get` (included in `roles/integrations.integrationViewer`, `integrationInvoker`, `integrationEditor`, and `integrationAdmin`).

```bash
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID:troubleshoot"
```

- **Response fields:** `executionId`, `displayMessage`, `errorMessage`, `rootCause`, and `detailedExplanation`.
- **Console requirements:** In the Cloud console, Gemini AI troubleshooting works only on failed executions of published (`ACTIVE`) integrations, and AI features must be enabled for the region.
- **Other v2 read endpoints:** `v2` also exposes `executions.list` and `executions.taskExecutions.get`.

## Canceling and Replaying Executions

Both `:cancel` and `:replay` change runtime state. Show the exact command and obtain user confirmation before executing either call.

### Cancel (`executions:cancel`)

- **IAM required:** `integrations.executions.cancel` (included in `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`—**not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`, so approvers with only `roles/integrations.suspensionResolver` cannot cancel a stuck `SUSPENDED` run).
- **Allowed states:** Only executions in `PENDING` (console "On hold"), `RETRY_ON_HOLD` (console "Retry on hold"), or `SUSPENDED` (console "Suspended") can be canceled.
- **Disallowed cases:** Cannot cancel an execution in the `PROCESSING` state (console "In process"), a completed execution (`SUCCEEDED`, `FAILED`, `CANCELLED`), or any execution started by a Schedule trigger.
- **Behavior:** Cancels the execution and its sub-executions. Requires `cancelReason` in the request body.

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"cancelReason": "User requested cancel of stuck retry"}' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID:cancel"
```

### Replay (`executions:replay` - Preview)

- **Availability:** Preview feature; works only on published (`ACTIVE`) integrations.
- **IAM required:** `integrations.executions.replay` (included in `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`—**not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`).
- **Allowed states:** Only `SUCCEEDED`, `FAILED`, or `CANCELLED` (console "Succeeded", "Failed", or "Canceled") executions can be replayed. If an execution is paused or retrying, cancel it first before replaying.
- **Disallowed cases and preconditions (`FAILED_PRECONDITION`):**
  - Executions started by a Schedule trigger cannot be replayed.
  - **Test-case runs** cannot be replayed in any mode (returns `FAILED_PRECONDITION`: `"Test runs cannot be replayed."`).
  - **`REPLAY_MODE_POINT_OF_FAILURE` when database persistence is disabled:** Refused with `FAILED_PRECONDITION` for executions that ran with database persistence (local logging / `databasePersistencePolicy: DATABASE_PERSISTENCE_DISABLED`) disabled, because point-of-failure replay requires execution snapshots; use `REPLAY_MODE_FROM_BEGINNING` in that case.
- **Deadline and mode:** Replayed runs keep the original execution mode (`SYNC` or `ASYNC`) and have a 10-minute default deadline, after which their state becomes `CANCELLED`.
- **Replay modes (`replayMode`):**
  - `REPLAY_MODE_FROM_BEGINNING`: re-runs the entire execution from the trigger.
  - `REPLAY_MODE_POINT_OF_FAILURE`: re-runs starting from the failed task (available only for failed executions that ran with database persistence enabled; if the version used `databasePersistencePolicy: DATABASE_PERSISTENCE_DISABLED`, `REPLAY_MODE_POINT_OF_FAILURE` is refused with `FAILED_PRECONDITION` because it needs execution snapshots—use `REPLAY_MODE_FROM_BEGINNING` in that case).
- **Optional parameter override (`modifiedParameters` and `updateMask`):** Pass `modifiedParameters` and `updateMask` to override inputs on replay. List every overridden key in `updateMask`; without `updateMask`, all original inputs are discarded and only `modifiedParameters` are used, and a key in `updateMask` missing from `modifiedParameters` is an error.
- **Response fields:** `executionId`, `replayedExecutionId`, and `outputParameters`.

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "replayReason": "Replaying from failed task after fixing target service access",
    "replayMode": "REPLAY_MODE_POINT_OF_FAILURE"
  }' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID:replay"
```
