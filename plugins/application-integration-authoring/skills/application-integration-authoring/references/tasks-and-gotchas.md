# Tasks, Variables, and Gotchas Reference

This reference lists the limits, configuration rules, and runtime pitfalls for common Application Integration tasks, variable expressions, and retry policies.

- [Core Data and Integration Tasks](#core-data-and-integration-tasks): Lines 12-24
- [Pause and Wait Tasks (`Approval`, `Suspend`, `Timer`)](#pause-and-wait-tasks-approval-suspend-timer): Lines 25-40
- [Loop and Sub-Integration Tasks](#loop-and-sub-integration-tasks): Lines 41-51
- [Variable Reference Syntax and System Variables](#variable-reference-syntax-and-system-variables): Lines 52-73
- [Error Handling and Retry Strategies](#error-handling-and-retry-strategies): Lines 74-101
- [Project and Integration Quotas](#project-and-integration-quotas): Lines 102-114

## Core Data and Integration Tasks

| Task | Key Limits | Documented Rules and Gotchas |
| :--- | :--- | :--- |
| **Data Mapping** | Array <= 100,000 elements; JSON or String variable <= 20 MB | Input and output types must match exactly; cast explicitly with transformation functions such as `TO_STRING` or `TO_INT`. Always configure a fallback value, or `null` inputs cause the task to fail. |
| **Data Transformer Script** (Preview) | 300 MB evaluation memory | Supports Diagram mode and Jsonnet Script mode. Jsonnet identifiers cannot contain hyphens (`-`). |
| **JavaScript** | Script request size <= 25 MB | Uses the V8 JavaScript engine (the legacy Rhino engine was deprecated on January 24, 2025). Do not delete or rename the `executesScript(event)` entrypoint function. |
| **Call REST Endpoint** | Request <= 20 MB; Response <= 34 MB; <= 100 concurrent calls | Reaches the **public internet only** (cannot connect to private VPC-only hosts). Fails on HTTP `4xx` and `5xx` responses. Outputs task variables such as `` `Task_1_responseBody` `` (for `taskId` `"1"`). An authentication profile (`authConfig`) configured on the task takes precedence over the integration's `runAsServiceAccount` (which generates the auth token when no auth config is set on the task). If you change its authentication profile, publish the version so the updated profile takes effect. |
| **Connectors** | Timeout 3 minutes; data to/from connection <= 8 MB (Application Integration quota; Integration Connectors quota lists 10 MB max Connectors task payload); response <= 20 MB; default page size 25 (max 50,000 pages); custom query <= 180 seconds and <= 50,000 rows | Requires a provisioned Integration Connectors connection (billed per active node) and `roles/connectors.admin` to create connections. Uses the integration's `runAsServiceAccount` to generate the auth token when no auth config is configured on the task. Outputs `connectorOutputPayload`. HTTP 429 indicates connection node throttling (increase min/max nodes or add a retry strategy). |
| **Cloud Function** | Standard HTTP limits | Supports Cloud Functions 1st gen and v2 (`.run.app`). Function source must follow the required template (`main.py`, `task.py`, `requirements.txt`). Stops working if VPC Service Controls is enabled for Application Integration. An attached OIDC authentication profile (`authConfig`) takes precedence over the integration's `runAsServiceAccount` (which generates the auth token when no auth config is set on the task). |
| **Send Email** | Max 30 recipients | Supports `$variableName$` substitution inside both the email subject and body. |
| **Other Built-in Tasks** | Service-specific | Also available: Return, Apps Script, and Google Cloud service tasks (Cloud KMS, Dataflow, Drive, Document AI, Firestore, Natural Language, Secret Manager, Sheets, Translate, Vertex AI, and Workflows). |

## Pause and Wait Tasks (`Approval`, `Suspend`, `Timer`)

Integrations containing any of these three tasks cannot be tested in draft state and must be published before testing or execution (for example, by publishing to a non-production project and calling `integrations:execute`).

| Feature | Approval Task | Suspend Task | Timer Task |
| :--- | :--- | :--- | :--- |
| **Purpose** | Emails recipients to approve or reject | Pauses for an external event or timeout | Pauses for a fixed delay |
| **Resume via REST API?** | **Yes** (`POST .../executions/EXECUTION_ID/suspensions/SUSPENSION_ID:resolve` with `state` `"LIFTED"` or `"REJECTED"`, the same call the console Approve/Reject buttons make; confirm with user first) | **Yes** (`POST .../integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions/SUSPENSION_ID:lift` with optional `suspensionResult`; `-` can replace `INTEGRATION_NAME` and either `EXECUTION_ID` or `SUSPENSION_ID` if at least one ID is concrete; confirm with user first) | **No** (resumes automatically when timer expires) |
| **Max / Default Duration** | Configurable hours (max total run lifetime 31 days) | Max and default 44,640 minutes (31 days) | Default 120 seconds, max 44,640 minutes (31 days) |
| **Expiration Behavior** | Defaults to `REJECTED` (can be set to lift) | Resumes with `suspensionResult` = `Expired` | Resumes automatically |
| **Required Approver IAM** | `integrations.suspensions.resolve` (`roles/integrations.suspensionResolver` or `roles/integrations.integrationAdmin`) + `roles/iam.serviceAccountUser` on `runAsServiceAccount` (`suspensions.list` needs `integrations.suspensions.list`) | `integrations.suspensions.lift` (`roles/integrations.suspensionResolver` or `roles/integrations.integrationAdmin`) + `roles/iam.serviceAccountUser` on `runAsServiceAccount` (`suspensions.list` needs `integrations.suspensions.list`) | None |
| **Execution Mode After Resume** | Always ASYNC | Always ASYNC | `< 60 s` behaves like SYNC; `>= 60 s` runs ASYNC |
| **Key Output / Branching** | Boolean `isApproved` (for example, `taskId` `"2"` -> `` $`Task_2_isApproved`$ = TRUE ``) | `suspensionResult` string (defaults to `Resolved` if lifted without a value) | None |

- **Publish side effect**: Publishing a new version of an integration automatically cancels all currently suspended executions of the previous version.

## Loop and Sub-Integration Tasks

All loop and sub-integration tasks invoke another published integration (the sub-integration) by its API trigger (`api_trigger/TRIGGER_NAME`) or Private trigger (`private_trigger/TRIGGER_NAME`). For sub-integration calls (`Call Integration`, `For Each Loop`, `For Each Parallel`), child responses/output parameters are returned to the parent only in `SYNC` mode; `ASYNC` calls return no output parameters.

| Task | Max Iterations / Scale | Key Rules and Gotchas |
| :--- | :--- | :--- |
| **For Each Loop** | 8,000 iterations; <= 50 MB total collected output | Calls a sub-integration sequentially per array item. Child responses/output parameters are returned to the parent only in SYNC mode (ASYNC calls return no output parameters). Prefer underscore loop-metadata keys (such as `current_iteration_count`). |
| **For Each Parallel** | 10,000 iterations; default parallelism 50 | Calls sub-integrations concurrently. Child responses/output parameters are returned to the parent only in SYNC mode (ASYNC calls return no output parameters); avoid SYNC mode if the sub-integration runs longer than 2 minutes or contains an Approval task. Selecting "run all integrations with this trigger ID" makes sub-integration responses unavailable to the parent. |
| **While Loop** | 8,000 iterations | Repeats a sub-integration while a condition holds. |
| **Call Integration** | Up to 10,000 sub-integrations | Callee must have an API trigger or a Private trigger (Private triggers are invokable only from other integrations). Supports SYNC or ASYNC mode (child responses/output parameters are returned to the parent only in SYNC mode; ASYNC calls return no output parameters). The caller's service account (or default Application Integration service agent `service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com` if none is attached) needs `roles/integrations.integrationInvoker`. |

## Variable Reference Syntax and System Variables

### Four Variable Categories

1. **Integration variables**: Defined in `integrationParameters` (`inputOutputType` of `IN`, `OUT`, `IN_OUT`, or `IN_OUT_TYPE_UNSPECIFIED` for internal variables). Referenced as `$variableName$`.
2. **Task variables**: Auto-generated outputs from tasks, named `` `Task_<taskId>_<variableName>` `` where `taskId` is the bare task number in `taskConfigs[].taskId`. Referenced with backticks inside dollar signs (for example, `taskId` `"5"` -> `` $`Task_5_responseBody`$ ``).
3. **Config variables**: Environment values defined in `integrationConfigParameters` with prefix `CONFIG_`. Referenced as `` $`CONFIG_endpoint_url`$ ``.
4. **System variables**: keys are backtick-wrapped; reference them as `` $`ExecutionId`$ `` (a bare `$ExecutionId$` names a nonexistent integration variable and fails).

### Built-in System Variables

| System Variable | Type | Contents |
| :--- | :--- | :--- |
| `` `ExecutionId` `` | String | Unique UUID for the current execution. |
| `` `ExecutionMode` `` | String | `SYNC` or `ASYNC`. |
| `` `ErrorInfo` `` | JSON (`message`, `code`) | Populated when a task or trigger fails (for example, `` $`ErrorInfo.code`$ ``). |
| `` `IntegrationName` `` | String | Name of the running integration. |
| `` `Region` `` | String | Region (`LOCATION`) where the integration runs. |
| `` `ProjectId` `` | String | Google Cloud project ID. |

- **Override precedence**: A value supplied dynamically by a trigger at runtime always overrides a static `defaultValue` defined on the integration variable.

## Error Handling and Retry Strategies

Error handling strategies apply to temporary (server-side) errors. Combine a task retry strategy with an Error Catcher trigger so the catcher runs after all retries are exhausted.

### Task `FailurePolicy.retryStrategy` Options

| UI Strategy Name | API Enum (`retryStrategy`) | Behavior |
| :--- | :--- | :--- |
| Fatal | `FATAL` | Fails the entire integration execution immediately. |
| Ignore | `IGNORE` | Ignores the task failure and continues downstream tasks as if this task succeeded. |
| None | `NONE` | Downstream tasks dependent on this task do not run, though parallel branches can still complete. |
| Restart integration with backoff | `RESTART_INTEGRATION_WITH_BACKOFF` | Restarts the entire integration from the first task using your configured `intervalTime` (retry interval in seconds) and `maxRetries` (maximum retry count). |
| Retry task (exponential / fixed / linear) | `EXPONENTIAL_BACKOFF` / `FIXED_INTERVAL` / `LINEAR_BACKOFF` | Retries only the failed task using `maxRetries` and `intervalTime` (adds a random 1–5 second jitter). |

### Conditional Failure Policies and Edge Conditions

- **Operators**: `=`, `!=`, `<`, `<=`, `>`, `>=`, `:`, `AND`, `OR`, `NOT`.
- **Functions**: `exists()`, `does_not_exist()`, `is_empty()`, `is_not_empty()`.
- **Condition example**: `` $`ErrorInfo.code`$ = 404 OR $`ErrorInfo.code`$ = 503 ``.
- **Evaluation order**: Conditional policies in `conditionalFailurePolicies.failurePolicies` are checked in list order; if none match, `defaultFailurePolicy` applies.

### Error Catcher Constraints

- Started by an Error Catcher trigger (`errorCatcherConfigs`) and linked via `errorCatcherId` on a task or trigger.
- Event-level catchers handle integration, edge-condition, task, and retry failures when no task-level catcher is attached.
- Only one error catcher can be attached per task or trigger.
- Error catchers cannot be nested, and no edges may connect error catcher tasks back into the main workflow flow.

## Project and Integration Quotas

| Resource or Limit | Value | Notes |
| :--- | :--- | :--- |
| Max cumulative integration data | 30 MB | Applies per integration and per sub-integration. **Above 10 MB, local logging is disabled** (no full logs, no retry strategy, no dashboard metrics). |
| Max API trigger input size | 8 MB | Exceeding 8 MB prevents the integration from starting and returns an error. |
| Max integrations per project | 1,000 | Integration name max 64 characters. |
| Max tasks per integration | 100 | Maximum number of tasks allowed in an integration. |
| Max versions per integration | 100 | Delete (`ARCHIVE`) old unused versions before hitting 100. |
| Default concurrent executions | 50 per project per region; 10 per integration | Both caps are adjustable. A burst on a single integration hits the 10-per-integration cap, not 50. Per the error-handling documentation ("Backoff retries"): "The default concurrency limit is set to 50 executions for each project and region. Failed executions are queued and retried using an exponential backoff algorithm" (10, 20, 40 minutes, and so on), up to 10 times. |
| Execution request rate | Shown on Cloud Quotas page | The execution request rate quota is shown on the Cloud Quotas page for the project and can be adjusted there. Execution-log reads cap at 18,000 per minute. |
| Eventual consistency after publish | Up to 10 minutes | An older published version can continue serving for up to 10 minutes after a new version is published. |
| Integration Connectors limits | 50 connections / region | Max 100 nodes per connection; max 20 unique regions; max 10 MB Connectors task payload (Integration Connectors quota; Application Integration quota caps data to/from connections at 8 MB). |
