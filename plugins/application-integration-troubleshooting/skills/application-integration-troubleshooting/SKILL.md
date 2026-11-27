---
name: application-integration-troubleshooting
metadata:
  version: "1.0.2"
  category: ApplicationDevelopment
description: >-
  Diagnoses failed, stuck, or silent Google Cloud Application Integration runs and
  Integration Connectors tasks using the REST API, Cloud Logging, and Cloud Monitoring.
  Use when an integration fails, returns HTTP 200 without doing the expected work, hangs
  in a suspended or retry state, or hits IAM, run-as service account, connector health,
  or quota errors. Do not use for initial region provisioning (use
  application-integration-basics) or building and deploying versions (use application-integration-authoring).
---

# Application Integration Troubleshooting

Diagnose and recover Google Cloud Application Integration executions that fail, stall, or appear to do nothing. This skill walks through execution state verification, per-task failure inspection, Cloud Logging and Cloud Monitoring checks, Integration Connectors health probes, suspension resolution, and IAM or quota checks.

## Attribution

**MUST READ**: Before executing any `gcloud` command, REST API call, or Python
discovery-client call, you MUST read
[Usage Attribution](references/attribution.md). For commands executed directly
in the terminal (never in generated scripts, Terraform, ADK agents, or user
code), prefix `gcloud` with
`CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0 (skill:application-integration-troubleshooting)"`
and add `agent-skills/1.0 (skill:application-integration-troubleshooting)` to
the `User-Agent` header of `curl` requests.

## Tooling and Scope Boundaries

- **REST is the interface.** There is no `gcloud integrations` command group and no Google-managed MCP server for Application Integration. Use `curl` with `gcloud auth print-access-token`, or the discovery-based Python client (`googleapiclient.discovery.build("integrations", "v1")` and `build("connectors", "v1")`; install with `pip install "google-api-python-client>=2.100.0,<3" "google-auth>=2.20.0,<3"`) (changes host or credential state; get the user's approval first).
- **Generic `gcloud` commands apply** for authentication (`gcloud auth`), enabling APIs (`gcloud services`), IAM checks (`gcloud projects get-iam-policy`, `gcloud iam service-accounts get-iam-policy`), and log queries (`gcloud logging read`).
- **Regional scope.** Integrations, executions, connections, and execution logs live in a single Google Cloud region (`LOCATION`), which is the `LOCATION` in every REST path; no `gcloud` default-region setting applies. Ask the user which region the integration is deployed in. If they don't know, start with `us-central1` and, if `executions.list` is empty there, check the other [Application Integration locations](https://docs.cloud.google.com/application-integration/docs/locations.md.txt) before concluding nothing ran (Step 2).
- **Sibling skills:**
  - Use `application-integration-basics` for product concepts, enabling APIs, provisioning a region, initial IAM roles, and service limits.
  - Use `application-integration-authoring` for creating drafts, editing tasks and triggers, config variables, publishing, `:execute` and `:schedule` payloads, and CI/CD export/import.

## Safety and Confirmation Rules

- **Read-only checks run freely:** `executions.list`, `suspensions.list`, `connections.get`, `connectionSchemaMetadata` get calls, runtime v2 `actions.list` / `entityTypes.list`, `gcloud logging read`, and `v2` `executions:troubleshoot`.
- **State-changing actions require explicit user confirmation.** Before canceling or replaying an execution, lifting or resolving a suspension, refreshing connector schema metadata, repairing connector eventing, publishing or unpublishing a version, or changing IAM bindings, show the exact command and wait for user approval.
- **Host changes require approval.** Before installing packages (`pip install`) or changing global gcloud or credential state (`gcloud config set ...` such as `auth/impersonate_service_account`, `gcloud auth application-default login` / `set-quota-project`), show the exact command and wait for the user's approval.
- **Never bundle destructive scripts** or delete integrations, versions, connections, or auth profiles during troubleshooting unless the user specifically asks.

## Prerequisites and Setup Check

Before querying APIs, confirm the environment has credentials, active APIs, and the right target region:

```bash
# Verify active identity and project
gcloud config get-value account
gcloud config get-value project

# Check that required APIs are enabled on PROJECT_ID
gcloud services list --enabled --project="PROJECT_ID" \
  --filter="config.name:(integrations.googleapis.com OR connectors.googleapis.com OR secretmanager.googleapis.com)"
```

- If an API is missing, ask the user before running `gcloud services enable integrations.googleapis.com connectors.googleapis.com secretmanager.googleapis.com --project="PROJECT_ID"`.
- Ensure an active billing account is attached to `PROJECT_ID` (required even when usage stays within the monthly free tier; see the [Application Integration pricing page](https://cloud.google.com/application-integration/pricing)).
- For Python discovery clients (install with `pip install "google-api-python-client>=2.100.0,<3" "google-auth>=2.20.0,<3"`) or ADK (`ApplicationIntegrationToolset`), authenticate with `gcloud auth application-default login` and `gcloud auth application-default set-quota-project PROJECT_ID` (changes host or credential state; get the user's approval first).

## Diagnostic Decision Flow

Follow these steps in order whenever a user reports that an integration failed, did nothing, or is stuck.

### Step 1: Confirm Whether an Execution Ran and Check Its True State

Do not rely on an HTTP 200 status from `:execute` as proof that every task succeeded (note: `integrations:test` also exists in the v1 REST API, but its required `TestIntegrationsRequest.clientId` value is not publicly documented, so do not invent one; test by publishing to a non-production project and calling `:execute`). As a diagnostic rule, always check the response payload and execution record because:
- The required verification is the execution record from `executions.list?filter=execution_id="EXECUTION_ID"`—inspect `executionDetails.state`, each task's `taskExecutionState`, and `ErrorInfo` in `responseParameters` (do not rely on the legacy/deprecated `executionFailed` field, which is not a supported public signal).
- If the caller passed `"doNotPropagateError": true` on `:execute`, the API returns HTTP 200 with an `executionId` and places error details inside event parameters instead of returning an HTTP error.
- A duplicate `requestId` on `:execute` or `:schedule` returns the previous execution's response without running a new execution.
- Task failure policies (`IGNORE` and `NONE`) allow an integration to continue or finish as `SUCCEEDED` down an alternate branch even when an individual task failed.

List executions for the integration (use `-` as `INTEGRATION_NAME` to search across all integrations in the region; the discovery doc does not specify whether `orderBy=create_time` sorts ascending or descending, so add a `CreateTimestamp` filter or paginate with `pageToken` if needed):

```bash
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions?pageSize=10&orderBy=create_time&snapshotMetadataWithoutParams=true"
```

Once you have the `EXECUTION_ID`, fetch its full `ExecutionDetails` and per-task states (use `filter`, `snapshotMetadataWithoutParams=true`, and `readMask` on `executions.list`—never the deprecated `truncateParams` [UI-only] or `filterParams.*` [internal-only] parameters):

```bash
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions?filter=execution_id%3D%22EXECUTION_ID%22"
```

To filter `executions.list` by state, use the `state` field (`=` or `!=`) with unquoted `ExecutionDetails.state` values (for example, `filter=state=FAILED`, `filter=state!=SUCCEEDED`, `filter=state=CANCELLED`, or `filter=state=FAILED OR state=CANCELLED`, URL-encoded as `filter=state%3DFAILED` or `filter=state%3DFAILED%20OR%20state%3DCANCELLED`); use `state` (not `eventExecutionState`, as shown on the REST reference page, or `event_execution_state` in the API reference's filter description), and use the supported filter keys (`execution_id`, `state`, `update_time`, `workflow_name`, `trigger_id`, `CreateTimestamp`, `parameter_type`)—camelCase variants such as `executionId` are not supported even though some docs examples show them.

### Step 2: What If No Execution Record Exists?

If `executions.list` returns no matching run, check these five causes before assuming the trigger never fired:

| Cause | Symptom | What to verify |
|---|---|---|
| **Wrong region** | Empty list in `LOCATION` | Check `https://console.cloud.google.com/integrations` or list integrations in other regions. |
| **API trigger 403** | Caller got HTTP 403 `PERMISSION_DENIED` | API trigger auth denials fail before execution creation; nothing is written to execution logs. Check caller IAM and `roles/iam.serviceAccountUser` on the run-as service account. |
| **API trigger payload > 8 MB** | Caller got an error | Cumulative API trigger input variables exceed the 8 MB limit, so the integration does not start. |
| **Local logging disabled** | Integration ran, but logs are empty | Check `IntegrationVersion.databasePersistencePolicy` (`DATABASE_PERSISTENCE_DISABLED` = `Disable`; `DATABASE_PERSISTENCE_POLICY_UNSPECIFIED` = `Enable (sync)`, the API default; `DATABASE_PERSISTENCE_ASYNC` = `Enable (async)`, the console default). Also, if total integration data exceeds 10 MB (up to the 30 MB limit), local logging is disabled automatically. |
| **Version not `ACTIVE`** | Trigger never fires | Only an `ACTIVE` (published) version runs from triggers. After publishing, an older version can keep serving for up to 10 minutes due to eventual consistency. |

### Step 3: Branch by Execution State (`ExecutionDetails.state`)

See [Execution States](references/execution-states.md) for the full state reference, task-level states (`TaskExecutionDetails.taskExecutionState`), filter syntax, and cancel/replay rules.

| `ExecutionDetails.state` | Console status | Meaning and next step |
|---|---|---|
| `FAILED` | Failed | Check `ErrorInfo` (`message`, `code`) in `responseParameters`, inspect the failing task's `taskExecutionState` (`FAILED` or `FATAL`), and run Step 4 (`:troubleshoot` and Cloud Logging). |
| `SUCCEEDED` | Succeeded | If expected work did not happen, inspect `taskExecutionDetails` for tasks in `SKIPPED` (edge condition false) or `FAILED` (masked by `IGNORE` or `NONE` retry strategy). |
| `CANCELLED` | Canceled | User canceled the run, a new integration version was published while the run was suspended, a SYNC run hit the 2-minute timeout, or a replayed run hit the 10-minute deadline. |
| `SUSPENDED` | Suspended | Waiting on an Approval task (resolvable in the Cloud console UI or via `suspensions:resolve`) or a Suspend task (resumable via `suspensions:lift`). See [Suspensions](references/suspensions.md). |
| `RETRY_ON_HOLD` | Retry on hold | A task or integration failed with a temporary error and is waiting in the backoff retry queue. |
| `PROCESSING` | In process | Currently running. Check whether an ASYNC run is approaching the 10-minute timeout. |
| `PENDING` | On hold | Scheduled or temporarily paused and waiting to be triggered. |

### Step 4: Inspect Logs, AI Root Cause, and Subsystem Health

1. **Run AI Troubleshoot (v2 REST API)** on a failed execution to get a structured root-cause summary (requires `integrations.executions.get`):
   ```bash
   curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://integrations.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID:troubleshoot"
   ```
2. **Query Cloud Logging** if Cloud Logging was enabled on the version. Note that Cloud Logging is **disabled by default** and writes nothing if local logging is disabled. See [Logging and Monitoring](references/logging-and-monitoring.md) for how to enable it, severity behavior, and exact queries.
   ```bash
   gcloud logging read \
     'resource.type="integrations.googleapis.com/IntegrationVersion" AND jsonPayload.executionId="EXECUTION_ID"' \
     --project="PROJECT_ID" --limit=20 --format=json
   ```
3. **If a Connectors task failed**, do not guess whether the connector or IAM is at fault. Inspect the connection resource (`connections.get`) and its schema metadata (`GET .../connections/CONNECTION_NAME/connectionSchemaMetadata` for `state` and `errorMessage`, and runtime v2 `GET .../v2/.../connections/CONNECTION_NAME/actions` and `.../entityTypes` for listing—v1 `connectionSchemaMetadata:listActions` and `:listEntityTypes` require a `filter` and reject unfiltered calls). See [Connectors Health](references/connectors-health.md) for connection states, schema metadata checks, and node throttling (HTTP 429).
   ```bash
   curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://connectors.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME?view=FULL"
   ```
4. **If an IAM (403), run-as service account, timeout, or quota error occurred**, check both the caller's role and the integration's run-as service account. Integrations created on or after **October 15, 2026** with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce, or Connector Event; Private triggers are exempt like API triggers, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount`) cannot be tested or published unless `runAsServiceAccount` is set; whenever `runAsServiceAccount` is set, the user publishing or testing the version needs `roles/iam.serviceAccountUser` on it. See [Common Errors](references/common-errors.md) for the two-sided 403 checklist, error codes, task limits, and ADK `ApplicationIntegrationToolset` errors.

## Common Diagnostic Scenarios

### Scenario A: Failed Connectors Task (Connection Health vs Caller IAM)

1. Run `connections.get` with `view=FULL` (command above) and inspect `status.state` and `status.status`.
2. **If `status.state` is `ERROR` or `AUTHORIZATION_REQUIRED`:** the connection itself cannot reach or authenticate to the target backend. Fix the connection's credentials in Secret Manager or the Cloud console (`https://console.cloud.google.com/connectors/connections`). If the connection uses a service account in another project, verify `service-PROJECT_NUMBER@gcp-sa-connectors.iam.gserviceaccount.com` has `roles/iam.serviceAccountTokenCreator` in that project.
3. **If `status.state` is `ACTIVE`:** the connection is healthy. Check whether the identity running the task (the integration's `runAsServiceAccount`, or if unset, `service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com`) has a required Integration Connectors role (such as `roles/connectors.invoker` or `roles/connectors.admin`) in the connection's project.
4. **If the task failed with HTTP 429:** the connection exceeded its provisioned nodes. Raise min/max nodes on the connection and add a task retry strategy (`EXPONENTIAL_BACKOFF`).
5. **Trace the exact connector attempt in Cloud Logging** (when connector logging is enabled on the connection):
   ```bash
   gcloud logging read \
     'resource.type="connectors.googleapis.com/Connection" AND jsonPayload.integration_connectors_trace_id="EXECUTIONID_TASKID_ATTEMPTNUMBER"' \
     --project="PROJECT_ID" --limit=20 --format=json
   ```

### Scenario B: Stuck in `SUSPENDED` (Approval vs Suspend Task)

1. Identify which task paused the execution from `taskExecutionDetails` and list pending suspensions (read-only; requires `integrations.suspensions.list`, included in `roles/integrations.suspensionResolver`) to find `SUSPENSION_ID` and `taskId`. Note that `roles/integrations.suspensionResolver` alone cannot read execution records (no `integrations.executions.list` or `integrations.executions.get`, returning HTTP 403 on `executions.list` and v2 `:troubleshoot`); to inspect `taskExecutionDetails` (or run `:troubleshoot`), also grant `roles/integrations.integrationViewer` (or use the approval email link, which carries the execution and task IDs). See [Suspensions](references/suspensions.md) for full details.
   ```bash
   # Read-only: list suspensions on EXECUTION_ID
   curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions"
   ```
2. **Approval task:** can be approved or rejected in the Cloud console UI or via the REST API (`POST https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions/SUSPENSION_ID:resolve` with body `{"suspension": {"eventExecutionInfoId": "EXECUTION_ID", "integration": "INTEGRATION_NAME", "taskId": "TASK_ID", "state": "LIFTED"}}` or `"REJECTED"`—the same call the console Approve/Reject buttons make). Always confirm with the user before resolving. Verify the caller holds `integrations.suspensions.resolve` (included in `roles/integrations.suspensionResolver`, which is not included in `roles/integrations.integrationEditor`) **and** `roles/iam.serviceAccountUser` on the integration's `runAsServiceAccount`. Without `roles/iam.serviceAccountUser`, approving leaves the execution paused until it expires.
3. **Suspend task:** `:lift` is the Suspend-task variant and requires `integrations.suspensions.lift` (included in `roles/integrations.suspensionResolver`) plus `roles/iam.serviceAccountUser` on the integration's `runAsServiceAccount`. After user confirmation, call `POST .../executions/EXECUTION_ID/suspensions/SUSPENSION_ID:lift` with an optional `suspensionResult`.
4. **Watch out for version publish cancellation:** publishing a new version of an integration automatically cancels all suspended executions of the previous version.

### Scenario C: HTTP 403 `PERMISSION_DENIED` on Trigger, Test, or Publish

Application Integration enforces two independent permission checks:
1. **Caller IAM check:** the caller needs permission on the integration (`roles/integrations.integrationInvoker` to invoke, `roles/integrations.integrationEditor` to edit/test, `roles/integrations.integrationDeployer` or `roles/integrations.integrationEditor` to publish).
2. **Run-as service account check:** whenever `runAsServiceAccount` is set on the version, the user (or principal) publishing or testing the version needs `roles/iam.serviceAccountUser` on `runAsServiceAccount` at publish/test time, and at runtime the invoking caller or trigger service account needs `roles/iam.serviceAccountUser` on `runAsServiceAccount` (granted in the project that owns the service account). In addition, `runAsServiceAccount` needs roles on downstream Google Cloud resources.

Check both bindings before retrying. For Pub/Sub, Eventarc, and Connector Event triggers, a run-as service account (`roles/iam.serviceAccountUser`) denial records a failed execution and the event is **not** redelivered.

## Recovery Actions (Require User Confirmation)

Always display the exact command and obtain user confirmation before running `:cancel`, `:replay`, `:lift`, or `:resolve`. `:cancel` requires `integrations.executions.cancel` and `:replay` requires `integrations.executions.replay` (both are held by `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`—**not** by `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`, so approvers with only `roles/integrations.suspensionResolver` cannot cancel a stuck `SUSPENDED` run). `:replay` also enforces two preconditions that return `FAILED_PRECONDITION`: (a) test-case runs cannot be replayed in any mode (`"Test runs cannot be replayed."`), and (b) `REPLAY_MODE_POINT_OF_FAILURE` is refused for executions that ran with database persistence (local logging / `databasePersistencePolicy: DATABASE_PERSISTENCE_DISABLED`) disabled because it needs execution snapshots—use `REPLAY_MODE_FROM_BEGINNING` in that case. When overriding inputs on `:replay` with `modifiedParameters` and `updateMask`, list every overridden key in `updateMask`; without `updateMask`, all original inputs are discarded and only `modifiedParameters` are used, and a key in `updateMask` missing from `modifiedParameters` is an error.

```bash
# Cancel an execution in PENDING (console "On hold"), RETRY_ON_HOLD, or SUSPENDED state (requires integrations.executions.cancel)
# (Cannot cancel executions in PROCESSING state [console "In process"], completed runs [SUCCEEDED, FAILED, CANCELLED], or Schedule-trigger runs; approvers with only roles/integrations.suspensionResolver cannot cancel a stuck SUSPENDED run)
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"cancelReason": "Canceling stuck execution after investigation"}' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID:cancel"

# Replay a SUCCEEDED, FAILED, or CANCELLED execution on a published integration (Preview; requires integrations.executions.replay; test-case runs and Schedule-trigger runs cannot be replayed)
# replayMode: REPLAY_MODE_FROM_BEGINNING or REPLAY_MODE_POINT_OF_FAILURE (failed runs only; refused with FAILED_PRECONDITION if databasePersistencePolicy was DATABASE_PERSISTENCE_DISABLED—use REPLAY_MODE_FROM_BEGINNING in that case)
# Optional modifiedParameters/updateMask: list every overridden key in updateMask; without updateMask, all original inputs are discarded and only modifiedParameters are used; a key in updateMask missing from modifiedParameters is an error
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"replayReason": "Replay after fixing downstream permission", "replayMode": "REPLAY_MODE_POINT_OF_FAILURE"}' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/executions/EXECUTION_ID:replay"
```

## Reference Files

Load the matching reference file when you need deeper details, exact field names, or edge-case checks:

- [Usage Attribution](references/attribution.md): Usage attribution for `gcloud` CLI commands, direct `curl` REST calls, and Python discovery-client snippets run in the terminal.
- [Execution States](references/execution-states.md): `ExecutionDetails.state` and `TaskExecutionDetails.taskExecutionState` enums, `executions.list` filter operators, large-log workarounds (> 300 MB), and `:cancel` / `:replay` constraints.
- [Logging and Monitoring](references/logging-and-monitoring.md): Local logging vs Cloud Logging interactions, enabling Cloud Logging on a draft version, Logs Explorer queries, `integrations.googleapis.com/*` and `connectors.googleapis.com/*` metric schemas, and alerting setup.
- [Common Errors](references/common-errors.md): HTTP/gRPC error codes, the two-sided 403 checklist, the October 15, 2026 run-as service account requirement, task-level limits and gotchas, and ADK `ApplicationIntegrationToolset` errors.
- [Connectors Health](references/connectors-health.md): `ConnectionStatus.state`, `EventingStatus.state`, `connectionSchemaMetadata` probes, runtime v2 readiness calls, node throttling (HTTP 429), and separating connection auth from caller IAM.
- [Suspensions](references/suspensions.md): Suspend vs Approval vs Timer behavior, `suspensions.list` / `:lift` / `:resolve` payloads, expiration settings, and why approvals stay stuck without `roles/iam.serviceAccountUser`.
