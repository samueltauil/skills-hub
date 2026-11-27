# Suspensions, Approval Tasks, and Timer Tasks

Use this reference when an execution is paused in `SUSPENDED` state, when an Approval email link fails to resume a run, or when you need to list suspensions, lift a Suspend task, or resolve (approve/reject) an Approval task via the REST API.

- [Comparison: Suspend vs Approval vs Timer Tasks](#comparison-suspend-vs-approval-vs-timer-tasks): Lines 12-19
- [Lifecycle Rules and Gotchas](#lifecycle-rules-and-gotchas): Lines 20-26
- [IAM Required to View, Approve, or Lift Suspensions](#iam-required-to-view-approve-or-lift-suspensions): Lines 27-38
- [Listing Suspensions (`suspensions.list`)](#listing-suspensions-suspensionslist): Lines 39-59
- [Resolving an Approval Task or Lifting a Suspend Task (Requires User Confirmation)](#resolving-an-approval-task-or-lifting-a-suspend-task-requires-user-confirmation): Lines 60-104
- [Troubleshooting Stuck Approval Tasks](#troubleshooting-stuck-approval-tasks): Lines 105-113

## Comparison: Suspend vs Approval vs Timer Tasks

| Task | How it resumes | Resumable via REST API? | Max / default duration | Output / branching |
|---|---|---|---|---|
| **Suspend** | Manual via Suspensions API (`suspensions:lift`), or automatically on timeout expiry. | **Yes** (`suspensions:lift`, which accepts an optional `suspensionResult`) | Max and default: 44,640 minutes (31 days). | Sets suspension result (`Resolved` if lifted with no value, `Expired` on timeout, or custom `suspensionResult`). |
| **Approval** | Approve/Reject in the Cloud console UI or via the REST API (`suspensions:resolve` with `state` `"LIFTED"` or `"REJECTED"`—the same call the console buttons make). | **Yes** (`suspensions:resolve`; always confirm with user first) | Configurable `Time until expiration` (hours) and `Reminder frequency` (hours). | Outputs boolean `` `Task_<taskId>_isApproved` `` where `taskId` is the bare task number in `taskConfigs[].taskId` (for example, `taskId` `"2"` -> `` $`Task_2_isApproved`$ = TRUE ``). |
| **Timer** | Automatically when the timer elapses. | **No** (automatic only) | Default 120 seconds; max 44,640 minutes (31 days). | < 60 s behaves like synchronous mode; >= 60 s runs in asynchronous mode. |

## Lifecycle Rules and Gotchas

- **Cannot test before publishing:** Integrations that contain an Approval, Suspend, or Timer task cannot be tested in draft state. Publish the version first (for example, to a non-production project and invoke `integrations:execute`).
- **Publishing a new version cancels suspended runs:** Publishing a new version of an integration **automatically cancels** all suspended executions of the previously published version.
- **31-day maximum lifetime:** An integration execution can last at most **31 days total**, including all time paused in Approval or Suspend tasks.
- **Resumed runs are always asynchronous:** When an execution resumes from a suspension or approval, the remainder of the run always executes in **asynchronous (`ASYNC`)** mode, even if the original trigger was synchronous (`:execute`).

## IAM Required to View, Approve, or Lift Suspensions

Many stuck approvals happen because the recipient can open the integration but lacks suspension or run-as service account permissions.

1. **Suspension permissions (`integrations.suspensions.list`, `integrations.suspensions.resolve`, `integrations.suspensions.lift`):**
   - `:resolve` (Approval task) requires `integrations.suspensions.resolve`; `:lift` (Suspend task) requires `integrations.suspensions.lift`; `suspensions.list` requires `integrations.suspensions.list`. All three permissions are included in `roles/integrations.suspensionResolver` (Application Integration Approver) and `roles/integrations.integrationAdmin`.
   - **Gotcha:** `roles/integrations.integrationEditor` does **not** include `integrations.suspensions.list`, `integrations.suspensions.resolve`, or `integrations.suspensions.lift`. Conversely, `roles/integrations.suspensionResolver` contains only `integrations.suspensions.list`, `integrations.suspensions.resolve`, and `integrations.suspensions.lift` (plus `resourcemanager.projects.get` and `resourcemanager.projects.list`): it does **not** include `integrations.executions.cancel` (held by `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`), so approvers with only `roles/integrations.suspensionResolver` cannot cancel a stuck `SUSPENDED` run via `executions:cancel`. In addition, `roles/integrations.suspensionResolver` alone cannot read execution records (no `integrations.executions.list` or `integrations.executions.get`, returning HTTP 403 on `executions.list` and v2 `:troubleshoot`); to inspect `taskExecutionDetails` (or run `:troubleshoot`), also grant `roles/integrations.integrationViewer` (or use the approval email link, which carries the execution and task IDs).
   - **Visibility rule:** Calling `suspensions.list` requires `integrations.suspensions.list`, and only callers who hold permission to resolve the relevant suspensions can view them.
2. **Run-as service account permission (`roles/iam.serviceAccountUser`):**
   - If the integration version has a `runAsServiceAccount` configured, the approver or resolver must also hold `roles/iam.serviceAccountUser` on that service account (in the project that owns the service account).
   - **Gotcha:** Without `roles/iam.serviceAccountUser`, clicking approve or attempting to resume fails to advance the workflow, and the execution **stays paused until it expires**.

## Listing Suspensions (`suspensions.list`)

Use `suspensions.list` (read-only; requires `integrations.suspensions.list`, included in `roles/integrations.suspensionResolver`) to inspect pending suspensions for an execution.

```bash
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions"
```

### Suspension States and Expiration Fields

- `Suspension.state`:
  - `RESOLUTION_STATE_UNSPECIFIED`: unset state.
  - `PENDING`: waiting for resolution or expiration.
  - `LIFTED`: approved / lifted; execution resumes.
  - `REJECTED`: rejected (either manually or by default upon expiration).
- `SuspensionApprovalExpiration`:
  - `expireTime`: timestamp when the suspension expires.
  - `remindTime`: timestamp for the next reminder email.
  - `liftWhenExpired`: boolean controlling expiration behavior. For Approval tasks, **reject (`REJECTED`) is the default** on expiration unless configured to lift.

## Resolving an Approval Task or Lifting a Suspend Task (Requires User Confirmation)

Both **Approval** tasks (`suspensions:resolve`) and **Suspend** tasks (`suspensions:lift`) can be resumed via the public REST API. Always show the exact command and obtain user confirmation before calling `:resolve` or `:lift`.

### Approve or Reject an Approval Task (`suspensions:resolve`)

`suspensions:resolve` approves (`"state": "LIFTED"`) or rejects (`"state": "REJECTED"`) an **Approval** task by passing the `Suspension` record (`eventExecutionInfoId`, `integration`, `taskId`, and target `state`). This is the same call the Cloud console Approve/Reject buttons make. The caller needs `integrations.suspensions.resolve` (such as `roles/integrations.suspensionResolver`) plus `roles/iam.serviceAccountUser` on the integration's run-as service account.

```bash
curl -X POST \
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

### Lift a Suspend Task (`suspensions:lift`)

`suspensions:lift` is the **Suspend**-task variant (requires `integrations.suspensions.lift`, included in `roles/integrations.suspensionResolver`, plus `roles/iam.serviceAccountUser` on the integration's run-as service account). `LiftSuspensionRequest` takes an optional `suspensionResult` (string), which you can match in downstream edge conditions. If you omit `suspensionResult`, Application Integration sets the result to `Resolved`.

- **Wildcard `-` rules:** You may pass `-` for `INTEGRATION_NAME`. You may also pass `-` for either `EXECUTION_ID` or `SUSPENSION_ID`, provided at least **one** of `EXECUTION_ID` or `SUSPENSION_ID` is a real ID.

```bash
# Lift by EXECUTION_ID and SUSPENSION_ID with a custom suspensionResult
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"suspensionResult": "Approved"}' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions/SUSPENSION_ID:lift"

# Lift using EXECUTION_ID and wildcard '-' for INTEGRATION_NAME and SUSPENSION_ID
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"suspensionResult": "Approved"}' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/-/executions/EXECUTION_ID/suspensions/-:lift"
```

## Troubleshooting Stuck Approval Tasks

If an Approval task is stuck in `SUSPENDED` or failed after approval:

1. **Use the matching endpoint for the task type:** Approval tasks use `suspensions:resolve` (with `state` set to `"LIFTED"` or `"REJECTED"`, the same call the Cloud console Approve/Reject buttons make; confirm with the user first), whereas `suspensions:lift` (which takes an optional `suspensionResult`) is the Suspend-task variant.
2. **Check approver IAM:** Verify the recipient has `integrations.suspensions.resolve` (`roles/integrations.suspensionResolver` or `roles/integrations.integrationAdmin`) on the project (or `integrations.suspensions.lift` when lifting a Suspend task), **plus** `roles/iam.serviceAccountUser` on `IntegrationVersion.runAsServiceAccount`.
3. **Check whether a new version was published:** Run `versions.list` on the integration. If a new version was published after the execution started, the suspended execution was automatically canceled (`CANCELLED`).
4. **Check expiration (`expireTime`):** If the approval window elapsed, check whether `On expiration` was set to **Reject** (default, setting `` `Task_<taskId>_isApproved` ``, such as `` $`Task_2_isApproved`$ `` for `taskId` `"2"`, to `FALSE`) or **Lift**.
5. **Check the 31-day cap:** If the execution has been paused for 31 days total, it hits the maximum execution lifetime limit.
