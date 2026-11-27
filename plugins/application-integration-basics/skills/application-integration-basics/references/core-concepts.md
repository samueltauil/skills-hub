# Core Concepts

This reference explains Application Integration regionality, triggers, execution modes, task categories, version states and edit locks, variable types, suspensions, and authentication profiles.

- [Regionality and Architecture](#regionality-and-architecture): Lines 13-18
- [Triggers and Execution Modes](#triggers-and-execution-modes): Lines 19-39
- [Tasks and Failure Policies](#tasks-and-failure-policies): Lines 40-59
- [Integration Versions and Edit Locks](#integration-versions-and-edit-locks): Lines 60-75
- [Variables and Data Types](#variables-and-data-types): Lines 76-92
- [Suspensions, Approvals, and Timers](#suspensions-approvals-and-timers): Lines 93-102
- [Authentication Profiles](#authentication-profiles): Lines 103-110

## Regionality and Architecture

- **Serverless iPaaS**: Application Integration is fully managed and auto-scales across all zones in a Google Cloud region.
- **Regional scope**: Every integration, version, execution log, and authentication profile lives under `projects/PROJECT_ID/locations/LOCATION`.
- **Cross-region connections**: An integration in one region can use an Integration Connectors connection in a different region. The one exception is ADK `ApplicationIntegrationToolset` in connection mode, which requires Application Integration to be provisioned in the same region as the connection.

## Triggers and Execution Modes

A trigger is an external event that starts a sequence of tasks in an integration. An integration can have multiple triggers; each trigger starts from its own start task, and simultaneous triggers run separate execution copies.

| Execution mode | How it starts | Behavior |
| :--- | :--- | :--- |
| **Synchronous (`SYNC`)** | `projects.locations.integrations.execute`, console Test / Publish test, or `Call Integration` task in SYNC mode. | Blocks until fulfilled or failed. Timeout is 2 minutes (`CANCELLED` on timeout). |
| **Asynchronous (`ASYNC`)** | `projects.locations.integrations.schedule`, Schedule trigger, Cloud Scheduler trigger, Cloud Pub/Sub trigger, Salesforce trigger, or any execution resumed from a suspension or approval. | Fire-and-forget. Timeout is 10 minutes. |

### Supported trigger types

- **API trigger**: `triggerType: "API"`, trigger ID format `api_trigger/TRIGGER_NAME` (`TRIGGER_NAME` up to 64 characters). Multiple API triggers are allowed per integration if each ID is unique.
- **Private trigger**: `triggerType: "PRIVATE_TRIGGER"`, trigger ID format `private_trigger/TRIGGER_NAME`. Invokable only from other integrations (not public APIs). Exempt like API triggers from the October 15, 2026 `runAsServiceAccount` requirement, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount` (unless region governance is enabled). Shares the 30 MB cumulative data limit with its parent integration. A published private-trigger integration cannot be tested without unpublishing first.
- **Cloud Pub/Sub trigger**: `triggerType: "CLOUD_PUBSUB_EXTERNAL"`, topic format `projects/PROJECT_ID/topics/TOPIC_ID`. Publishing creates the Pub/Sub subscription automatically and exposes the `CloudPubSubMessage` JSON output variable. New or modified Pub/Sub triggers require a trigger service account (the identity that invokes the integration at runtime). Integrations created on or after October 15, 2026 with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce, or Connector Event) cannot be tested or published unless `runAsServiceAccount` is set; whenever `runAsServiceAccount` is set, the user (or principal) publishing or testing the version needs `roles/iam.serviceAccountUser` on it (and at runtime, the trigger's service account needs `roles/iam.serviceAccountUser` on it).
- **Schedule trigger**: `triggerType: "CRON"`, uses a 5-field cron schedule. Google recommends the Cloud Scheduler trigger for higher scheduling reliability.
- **Cloud Scheduler trigger**: `triggerType: "CLOUD_SCHEDULER"`. Requires the Cloud Scheduler API, supports cross-region scheduling, and is billed separately. Editing it in Application Integration overwrites the cron job in a new integration version.
- **Salesforce trigger**: `triggerType: "SFDC_CHANNEL"` or `SFDC_CDC_CHANNEL`.
- **Connector Event triggers**: `triggerType: "INTEGRATION_CONNECTOR_TRIGGER"`. Starts from an Integration Connectors event subscription (such as Apache Kafka, Azure AD, HubSpot, IBM MQ, Jira Cloud, Jira Server Data Center, HL7, RabbitMQ, SAP ERP, SAP Gateway, ServiceNow, Solace, TIBCO EMS, Webhook in Preview, or Zendesk).
- **Eventarc trigger**: `triggerType: "EVENTARC_TRIGGER"`.
- **Error Catcher trigger**: Starts an error-catcher flow attached to a trigger or task (`errorCatcherId`). One catcher per error catcher ID; cannot be nested and cannot connect back to the main flow.

## Tasks and Failure Policies

A task is a unit of work that takes inputs, performs an action, and writes task output variables.

| Task category | Examples and key constraints |
| :--- | :--- |
| **Data transformation** | `Data Mapping` (input/output types must match; cast with `TO_STRING`, `TO_INT`, etc.; null inputs error without a fallback value), `Data Transformer Script` (Preview, Jsonnet; identifiers cannot contain hyphens). |
| **Code & HTTP** | `JavaScript` (V8 runtime; Rhino deprecated January 24, 2025; keep `executesScript(event)`), `Call REST Endpoint` (public internet only, fails on HTTP 4xx/5xx), `Cloud Function` (1st gen and v2 `.run.app`; stops working if VPC Service Controls is enabled for Application Integration). |
| **Enterprise & Cloud** | `Connectors` (calls an Integration Connectors connection; 3-minute timeout), Google Cloud service tasks (KMS, Dataflow, Drive, Document AI, Firestore, Natural Language, Secret Manager, Sheets, Translate, Vertex AI, Workflows), `Apps Script`, `Send Email` (up to 30 recipients). |
| **Flow control & sub-workflows** | `For Each Loop` (up to 8,000 iterations), `For Each Parallel` (up to 10,000 iterations, default parallelism 50), `While Loop` (up to 8,000 iterations), `Call Integration` (callee must have an API trigger or a Private trigger [Private triggers are invokable only from other integrations]; SYNC or ASYNC; for `Call Integration`, `For Each Loop`, and `For Each Parallel`, child responses/output parameters are returned to the parent only in SYNC mode—ASYNC calls return no output parameters), `Return`. |
| **Human & time pauses** | `Approval`, `Suspend`, `Timer`. Integrations containing any of these three tasks cannot be tested in draft state and must be published first (for example, by publishing to a non-production project and calling `:execute`). |

### Per-task failure policies (`FailurePolicy.retryStrategy`)

- `NONE` (default when unset): Dependent tasks do not run if this task fails.
- `FATAL`: Immediately fails the entire integration execution.
- `IGNORE`: Marks the failed task as succeeded so downstream tasks still run.
- `EXPONENTIAL_BACKOFF`, `FIXED_INTERVAL`, `LINEAR_BACKOFF`: Retries the task from the failed task onwards (`maxRetries` and `intervalTime` in seconds required; exponential and linear backoff add 1-5 seconds of delay).
- `RESTART_INTEGRATION_WITH_BACKOFF`: Restarts the entire integration from the first task with initial parameters (`maxRetries` and `intervalTime` in seconds required).

## Integration Versions and Edit Locks

Only a `DRAFT` version can be edited, and only an `ACTIVE` version runs from configured triggers or the `:execute` endpoint.

| State | Meaning |
| :--- | :--- |
| `DRAFT` | Editable version. Locked to its author (`lockHolder`) for 15 minutes after the last update, then released. |
| `ACTIVE` | Published version serving live traffic. |
| `SNAPSHOT` | Prior draft saved when another author clicks **Take Over** in the console, or a previously active version after calling `:unpublish` (tagged `PREVIOUSLY_PUBLISHED`). |
| `ARCHIVED` (API) / `DELETED` (docs) | The REST API `IntegrationVersion.state` enum uses `ARCHIVED`, while the Integration versions documentation page lists `DELETED`. Calling `versions.delete` soft-deletes a version into `ARCHIVED` with no undelete mechanism. |

- **Publishing**: Calling `versions:publish` deploys the version as `ACTIVE`, automatically unpublishes any previously active version, releases any edit lock, and **automatically cancels suspended executions of the previous version**.
- **Eventual consistency**: After publishing a new version, the prior version can continue running for up to 10 minutes.
- **Editing an active integration**: In the console, clicking **Enable Editing** creates a new `DRAFT` version while the `ACTIVE` version keeps running. Uploading a version via `versions:upload` also creates a new `DRAFT` version.
- **Deleting**: Deleting every version of an integration deletes the integration itself.

## Variables and Data Types

Reference standard variables as `$varName$`, and task output or system variables with backticks as `` $`Task_1_responseBody`$ `` or `` $`ExecutionId`$ ``. Dynamic trigger inputs override static defaults.

| Variable kind | Purpose and rules |
| :--- | :--- |
| **Integration variables** | Explicitly defined on `integrationParameters[]` with `inputOutputType` (`IN`, `OUT`, `IN_OUT`, or `IN_OUT_TYPE_UNSPECIFIED` when used only internally). |
| **Task variables** | Auto-generated outputs from tasks, named `` `Task_<taskId>_<variableName>` `` where `taskId` is the bare task number in `taskConfigs[].taskId` (for example, `taskId` `"1"` -> `` $`Task_1_responseBody`$ ``). |
| **System variables** | Auto-generated per run; keys are backtick-wrapped: `` `ExecutionId` ``, `` `ExecutionMode` `` (`SYNC` or `ASYNC`), `` `ErrorInfo` `` (`message`, `code`), `` `IntegrationName` ``, `` `Region` ``, `` `ProjectId` ``. Reference them as `` $`ExecutionId`$ `` (a bare `$ExecutionId$` names a nonexistent integration variable and fails). |
| **Config variables** (Preview) | Environment-specific design-time values (`integrationConfigParameters` on the version with defaults in `parameter.defaultValue` [a top-level `value` on a draft is discarded], `configParameters` on `versions:publish`, named `` `CONFIG_<NAME>` ``; keys in `configParameters` must **exactly match** a key in `integrationConfigParameters`, backticks included, such as `` "`CONFIG_target_url`" ``, because unknown keys are silently ignored—publish returns 200 and the default stays). **Not a secret store**: values export in plain text even when variable masking is enabled. Config variables cannot parameterize connector entity operations or actions. |

### Supported data types (`ValueType` / `IntegrationParameter.dataType`)

- Scalar types: `STRING_VALUE` (`stringValue`), `INT_VALUE` (`intValue`, string-encoded int64 in JSON), `DOUBLE_VALUE` (`doubleValue`), `BOOLEAN_VALUE` (`booleanValue`).
- Array types: `STRING_ARRAY` (`stringArray`), `INT_ARRAY` (`intArray`), `DOUBLE_ARRAY` (`doubleArray`), `BOOLEAN_ARRAY` (`booleanArray`).
- Structured type: `JSON_VALUE` (`jsonValue`, JSON-serialized string).

## Suspensions, Approvals, and Timers

All three tasks pause an execution, and any resumed execution runs in **asynchronous (`ASYNC`)** mode even if the initial call was synchronous. Maximum total execution duration (including pause time) is 31 days (44,640 minutes).

| Task | How it resumes | Key details |
| :--- | :--- | :--- |
| **Suspend** | Automatic timeout or REST API (`POST .../executions/EXECUTION_ID/suspensions/SUSPENSION_ID:lift`). | Suspension `state` is `PENDING`, `REJECTED`, or `LIFTED`. `:lift` is the Suspend-task variant and accepts an optional `suspensionResult` (defaults to `Resolved`, or `Expired` on timeout). Caller needs `integrations.suspensions.lift` (included in `roles/integrations.suspensionResolver`) plus `roles/iam.serviceAccountUser` on the integration's run-as SA (`suspensions.list` needs `integrations.suspensions.list`). Always confirm with the user before lifting. |
| **Approval** | Cloud console Approve/Reject buttons or REST API (`POST .../executions/EXECUTION_ID/suspensions/SUSPENSION_ID:resolve` with `{"suspension": {"eventExecutionInfoId": "EXECUTION_ID", "integration": "INTEGRATION_NAME", "taskId": "TASK_ID", "state": "LIFTED"}}` or `"REJECTED"`, the same call the console buttons make). | Emails recipients. Caller needs `integrations.suspensions.resolve` (included in `roles/integrations.suspensionResolver`) plus `roles/iam.serviceAccountUser` on the integration's run-as SA (`suspensions.list` needs `integrations.suspensions.list`; always confirm with the user before resolving). Outputs boolean `` `Task_<taskId>_isApproved` `` (for example, `taskId` `"2"` -> `` $`Task_2_isApproved`$ ``). Defaults to rejected if unresolved at expiration. |
| **Timer** | Automatic timeout only. | Default 120 seconds, max 44,640 minutes. Waits under 60 seconds behave like sync mode; 60 seconds or more run async. |

## Authentication Profiles

An authentication profile (`projects.locations.authConfigs`, resource name `projects/PROJECT_ID/locations/LOCATION/authConfigs/AUTH_CONFIG_ID`) stores reusable credentials for tasks such as `Call REST Endpoint` and `Cloud Function`.

- **Credential types (`credentialType`)**: `AUTH_TOKEN`, `OIDC_TOKEN` (Google OIDC ID Token), `JWT`, `OAUTH2_AUTHORIZATION_CODE`, `OAUTH2_CLIENT_CREDENTIALS`, `OAUTH2_RESOURCE_OWNER_CREDENTIALS`, `CLIENT_CERTIFICATE_ONLY` (SSL/TLS client cert), `SERVICE_ACCOUNT`, `USERNAME_AND_PASSWORD`, `API_KEY`, `OAUTH2_IMPLICIT`.
- **OAuth 2.0 redirect URI**: `https://console.cloud.google.com/integrations/callback/locations/LOCATION`.
- **Portability**: Authentication profiles are **not** included when you download an integration version (`versions:download`). Create or map them separately in the target project before publishing.
- **Testing gotcha**: If you change the authentication profile on a `Call REST Endpoint` task, publish the integration version before testing (for example, in a non-production project via `:execute`) so the updated profile takes effect.
