# Application Integration REST API Cheatsheet

This reference covers the v1 and v2 REST endpoints for authoring, versioning, testing, publishing, and running Google Cloud Application Integration workflows.

- [Endpoint and Authentication Rules](#endpoint-and-authentication-rules): Lines 13-25
- [Integrations Resource (`projects.locations.integrations`)](#integrations-resource-projectslocationsintegrations): Lines 26-43
- [Versions Resource (`projects.locations.integrations.versions`)](#versions-resource-projectslocationsintegrationsversions): Lines 44-63
- [Authentication Profiles (`projects.locations.authConfigs`)](#authentication-profiles-projectslocationsauthconfigs): Lines 64-79
- [Test Cases (`versions.testCases`, Preview)](#test-cases-versionstestcases-preview): Lines 80-93
- [Templates (`projects.locations.templates`, Preview)](#templates-projectslocationstemplates-preview): Lines 94-106
- [Executions, Suspensions, and v2 Surface](#executions-suspensions-and-v2-surface): Lines 107-122

## Endpoint and Authentication Rules

- **Global base URL**: `https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION`
- **Regional base URL**: Some documentation pages use `https://LOCATION-integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION` for `:execute` and `:lift`. If you use the regional host, the host prefix and `locations/LOCATION` must match (the public API trigger guide contains a known typo pairing `us-east1` with `locations/us-central1`). Prefer the global host `https://integrations.googleapis.com` consistently.
- **Required OAuth scope**: `https://www.googleapis.com/auth/cloud-platform`
- **REST header**: `-H "Authorization: Bearer $(gcloud auth print-access-token)"`
- **Client libraries**: For the Python discovery client (`pip install "google-api-python-client>=2.100.0,<3" "google-auth>=2.20.0,<3"`), run `gcloud auth application-default login` and `gcloud auth application-default set-quota-project PROJECT_ID` to configure Application Default Credentials (changes host or credential state; get the user's approval first).
- **Service account impersonation**: Run `gcloud config set auth/impersonate_service_account SA_EMAIL` (caller needs `roles/iam.serviceAccountTokenCreator` on `SA_EMAIL`) (changes host or credential state; get the user's approval first).

| Header | Applies To | Default | Notes |
| :--- | :--- | :--- | :--- |
| `X-Server-Timeout` | `:execute` | `120` (seconds) | Sets the HTTP request wait timeout in seconds (synchronous execution max is 120 seconds). |

## Integrations Resource (`projects.locations.integrations`)

All paths below are relative to `https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION`.

| Method | HTTP & Path | Key Parameters / Body | IAM Permission | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `list` | `GET /integrations` | Query: `pageSize`, `pageToken`, `orderBy`, `filter` | `integrations.integrations.list` | Returns `integrations[]` (`name`, `description`, `active`, `createTime`, `updateTime`, `creatorEmail`, `lastModifierEmail`). |
| `search` | `GET /integrations:search` | Query search parameters | `integrations.integrations.list` | Searches integrations in the region. |
| `delete` | `DELETE /integrations/INTEGRATION_NAME` | None | `integrations.integrations.delete` | Permanently deletes the integration and **all** its versions. Cannot be undone. |
| `execute` | `POST /integrations/INTEGRATION_NAME:execute` | Body: `triggerId`, `inputParameters`, `requestId`, `doNotPropagateError` | `integrations.integrations.invoke` | Synchronous run; integration must be `ACTIVE`. Use `-` as `INTEGRATION_NAME` to run all integrations matching `triggerId`. |
| `schedule` | `POST /integrations/INTEGRATION_NAME:schedule` | Body: `triggerId`, `scheduleTime`, `inputParameters`, `requestId`, `userGeneratedExecutionId` | `integrations.integrations.invoke` | Asynchronous run; returns `executionInfoIds[]`. If `scheduleTime` <= now, runs immediately. |

### `integrations.list` Filtering and Ordering

- **Supported `orderBy` fields**: `last_modified_time`, `created_time`, `snapshot_number` (descending; the public `integrations.list` reference page writes these in camelCase as `lastModifiedTime`, `createdTime`, `snapshotNumber`), or `name` (ascending).
- **Supported `filter` operators**: `:`, `=`, `>`, `<`, `>=`, `<=`, `!=`, combined with `NOT`, `AND`, `OR`.
- **Limitation**: You cannot filter on repeated fields such as `taskConfig`.

## Versions Resource (`projects.locations.integrations.versions`)

All paths below are relative to `https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME`.

| Method | HTTP & Path | Key Parameters / Body | IAM Permission | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `create` | `POST /versions` | Query: `newIntegration` (bool, in discovery), `createSampleIntegrations` (bool); Body: `IntegrationVersion` | `integrations.integrationVersions.create` | Creates a `DRAFT` version (creates a new integration if none exists; pass `newIntegration=true` only when you want `ALREADY_EXISTS` if `INTEGRATION_NAME` already exists). |
| `get` | `GET /versions/VERSION_ID` | None | `integrations.integrationVersions.get` | Returns the full `IntegrationVersion` resource. |
| `list` | `GET /versions` | Query: `pageSize` (default 50, max 1000), `pageToken`, `orderBy`, `filter`, `fieldMask` | `integrations.integrationVersions.list` | `orderBy` supports `last_modified_time`, `created_time`, `snapshot_number` (desc), `name` (asc). |
| `patch` | `PATCH /versions/VERSION_ID` | Query: `updateMask` (FieldMask); Body: `IntegrationVersion` | `integrations.integrationVersions.update` | Updates an editable `DRAFT` version. |
| `delete` | `DELETE /versions/VERSION_ID` | None | `integrations.integrationVersions.delete` | Soft-deletes version to `ARCHIVED` (no undelete) and releases any edit lock. Fails if `DRAFT` and the caller is not `lockHolder`. Deleting all versions deletes the integration. |
| `download` | `GET /versions/VERSION_ID:download` | Query: `fileFormat` (`JSON` or `YAML`), `files[]` (`INTEGRATION`, `INTEGRATION_CONFIG_VARIABLES`) | `integrations.integrationVersions.get` | Returns `DownloadIntegrationVersionResponse` with `content` string and `files[]`. |
| `downloadJsonPackage` | `GET /versions/VERSION_ID:downloadJsonPackage` | Query: `files[]` (`INTEGRATION`, `INTEGRATION_CONFIG_VARIABLES`) | `integrations.integrationVersions.get` | Returns `files[]` with `type`, `integrationVersion`, and `integrationConfig` as JSON. |
| `upload` | `POST /versions:upload` | Body: `content` (string), `fileFormat` (`JSON` or `YAML`) | `integrations.integrationVersions.create` (in `roles/integrations.integrationEditor` and `roles/integrations.integrationAdmin`—not in `roles/integrations.integrationDeployer`, which can publish but cannot upload) | Creates a new `DRAFT` version from a downloaded payload (creates the integration if it does not exist yet; still requires `:publish`). Returns `UploadIntegrationVersionResponse.integrationVersion`. |
| `publish` | `POST /versions/VERSION_ID:publish` | Body: `configParameters` (Struct; keys must **exactly match** a key in `integrationConfigParameters`, backticks included, such as `` "`CONFIG_target_url`" ``, because unknown keys are silently ignored—publish returns 200 and the default stays) | `integrations.integrationVersions.deploy` (in `roles/integrations.integrationDeployer`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`, plus `roles/iam.serviceAccountUser` on `runAsServiceAccount` for the user publishing the version whenever `runAsServiceAccount` is set) | Makes version `ACTIVE`, auto-unpublishes prior `ACTIVE` version (dependents switch to the newly published version), and releases any edit lock. Fails if already `ACTIVE`/`ARCHIVED` or if `DRAFT` and the caller is not `lockHolder`. |
| `unpublish` | `POST /versions/VERSION_ID:unpublish` | Empty body | `integrations.integrationVersions.deploy` | Moves `ACTIVE` version to `SNAPSHOT` (tag `PREVIOUSLY_PUBLISHED`) and stops dependent services. Fails if not `ACTIVE`. |

- **Lock takeover**: `takeoverEditLock` does **not** exist on `projects.locations.integrations.versions` in v1. Wait 15 minutes for the lock to expire or use **Take Over** in the Cloud console.
- **Testing before production**: Test a draft version by publishing it to a non-production project (`versions:publish`) and invoking `integrations:execute` there.

## Authentication Profiles (`projects.locations.authConfigs`)

Authentication profiles store external credentials so secrets never enter `IntegrationVersion` JSON or config variables.

| Method | HTTP & Path | Key Parameters / Body | Notes |
| :--- | :--- | :--- | :--- |
| `create` | `POST /authConfigs` | Body: `AuthConfig` (`displayName` and `credentialType` required, `decryptedCredential`, `visibility`) | Requires `roles/integrations.integrationEditor` (or Admin). |
| `get` | `GET /authConfigs/AUTH_CONFIG_ID` | None | Returns `AuthConfig` (`state`: `VALID`, `INVALID`, `SOFT_DELETED`, `EXPIRED`, `UNAUTHORIZED`, `UNSUPPORTED`). |
| `list` | `GET /authConfigs` | Query: `pageSize`, `pageToken`, `filter`, `readMask` | Lists regional auth profiles. |
| `patch` | `PATCH /authConfigs/AUTH_CONFIG_ID` | Query: `updateMask`; Body: `AuthConfig` | Updates credentials or metadata. |
| `delete` | `DELETE /authConfigs/AUTH_CONFIG_ID` | None | Requires `roles/integrations.integrationAdmin`. |

- **Supported `credentialType` values**: `USERNAME_AND_PASSWORD`, `API_KEY`, `OAUTH2_AUTHORIZATION_CODE`, `OAUTH2_IMPLICIT`, `OAUTH2_CLIENT_CREDENTIALS`, `OAUTH2_RESOURCE_OWNER_CREDENTIALS`, `JWT`, `AUTH_TOKEN`, `SERVICE_ACCOUNT`, `CLIENT_CERTIFICATE_ONLY`, `OIDC_TOKEN`.
- **OAuth 2.0 redirect URI**: `https://console.cloud.google.com/integrations/callback/locations/AUTH_PROFILE_REGION`.
- **Portability**: Auth profiles are **not** included in downloaded integration files. Provision them separately in each project via REST or Terraform (`google_integrations_auth_config`).

## Test Cases (`versions.testCases`, Preview)

Test cases attach functional assertions and task mocks to a `DRAFT` version. They are not included when downloading an integration version and must be downloaded/uploaded separately.

| Method | HTTP & Path (under `.../versions/VERSION_ID`) | Notes |
| :--- | :--- | :--- |
| `create` | `POST /testCases?testCaseId=TEST_CASE_ID` | Cannot create test cases on an `ACTIVE` version (create a `DRAFT` first). |
| `get` / `list` | `GET /testCases/TEST_CASE_ID` / `GET /testCases` | Reads test case definitions (`triggerId`, `testInputParameters`, `testTaskConfigs`). |
| `patch` / `delete` | `PATCH /testCases/TEST_CASE_ID?updateMask=...` / `DELETE /testCases/TEST_CASE_ID` | Updates or removes a test case on a `DRAFT`. |
| `download` / `upload` | `GET /testCases/TEST_CASE_ID:download` / `POST /testCases:upload` | Exports or imports a test case (`fileFormat`: `JSON` or `YAML`). |
| `executeTest` | `POST /testCases/TEST_CASE_ID:executeTest` | Runs one test case (body `inputParameters`). Returns `executionId`, `testExecutionState`, `assertionResults[]`, `outputParameters`. Needs `integrations.testCases.invoke` (included in `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`). |
| `execute` | `POST /testCases:execute` | Runs all test cases on a version. Returns `executeTestCaseResponses[]` (each containing `executionId`, `testExecutionState`, `assertionResults[]`, `outputParameters`). Needs `integrations.testCases.invoke` (included in `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`). |
| `takeoverEditLock` | `POST /testCases/TEST_CASE_ID:takeoverEditLock` | Exists on `testCases` only (not on parent `versions`). |

## Templates (`projects.locations.templates`, Preview)

Templates package reusable integration patterns (Global read-only, Shared, or Project visibility).

| Method | HTTP & Path (under `.../locations/LOCATION`) | Notes |
| :--- | :--- | :--- |
| `create` / `patch` / `delete` | `POST /templates` / `PATCH /templates/TEMPLATE_ID?updateMask=...` / `DELETE /templates/TEMPLATE_ID` | Manages project or shared templates. |
| `get` / `list` / `search` | `GET /templates/TEMPLATE_ID` / `GET /templates` / `GET /templates:search` | Inspects available templates (`visibility`: `PRIVATE`, `SHARED`, `PUBLIC`). |
| `download` / `upload` | `GET /templates/TEMPLATE_ID:download?fileFormat=JSON` / `POST /templates:upload` | Exports (`fileFormat` required) or imports template content (body requires `content` and `fileFormat`). |
| `use` | `POST /templates/TEMPLATE_ID:use` | Creates a new integration from a template (body requires `integrationDetails` and `integrationRegion`; `subIntegrations` is optional). |
| `import` | `POST /templates/TEMPLATE_ID:import` | Imports a template into an existing integration (body requires `integration`; `subIntegrations` is optional). |
| `share` / `unshare` | `POST /templates/TEMPLATE_ID:share` / `POST /templates/TEMPLATE_ID:unshare` | Shares or revokes access across `resourceNames`. |

## Executions, Suspensions, and v2 Surface

| Method | HTTP & Path | Notes |
| :--- | :--- | :--- |
| `executions.list` | `GET /v1/.../integrations/INTEGRATION_NAME/executions` | Query with `filter`, `snapshotMetadataWithoutParams=true`, and `readMask` (do **not** use deprecated `truncateParams` [UI-only] or `filterParams.*` [internal-only]). Supported filter keys to use are `execution_id`, `state` (supports `=` and `!=` with unquoted `ExecutionDetails.state` values such as `filter=state=FAILED`, `filter=state!=SUCCEEDED`, `filter=state=CANCELLED`, or `filter=state=FAILED OR state=CANCELLED`, URL-encoded as needed; use `state`, not `eventExecutionState` [as shown on the REST reference page] or `event_execution_state` in the API reference's filter description), `update_time`, `workflow_name`, `trigger_id`, `CreateTimestamp`, and `parameter_type`; camelCase variants such as `executionId` are not supported even though some docs examples show them. Use `-` as `INTEGRATION_NAME` to query across integrations. |
| `executions:cancel` | `POST /v1/.../executions/EXECUTION_ID:cancel` | Body requires `cancelReason`. Only cancels `PENDING` (console "On hold"), `RETRY_ON_HOLD`, or `SUSPENDED` runs (cannot cancel `PROCESSING` [console "In process"], completed runs [`SUCCEEDED`, `FAILED`, `CANCELLED`], or Schedule-trigger runs). Requires `integrations.executions.cancel` (included in `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`—**not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`). |
| `executions:replay` | `POST /v1/.../executions/EXECUTION_ID:replay` | Preview; published integrations only. Body requires `replayReason`, optional `replayMode` (`REPLAY_MODE_FROM_BEGINNING` or `REPLAY_MODE_POINT_OF_FAILURE`), and optional `modifiedParameters` + `updateMask` (list every overridden key in `updateMask`; without `updateMask`, all original inputs are discarded and only `modifiedParameters` are used, and a key in `updateMask` missing from `modifiedParameters` is an error). Not for Schedule triggers. Preconditions returning `FAILED_PRECONDITION`: (a) test-case runs cannot be replayed in any mode (`"Test runs cannot be replayed."`); (b) `REPLAY_MODE_POINT_OF_FAILURE` is refused for executions that ran with database persistence (local logging / `databasePersistencePolicy: DATABASE_PERSISTENCE_DISABLED`) disabled because it needs execution snapshots—use `REPLAY_MODE_FROM_BEGINNING` in that case. Requires `integrations.executions.replay` (included in `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`—**not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`). |
| `suspensions.list` | `GET /v1/.../executions/EXECUTION_ID/suspensions` | Requires `integrations.suspensions.list` (included in `roles/integrations.suspensionResolver` and `roles/integrations.integrationAdmin`; `roles/integrations.suspensionResolver` alone cannot read execution records, so also grant `roles/integrations.integrationViewer` to inspect `taskExecutionDetails` or run `:troubleshoot`, or use the approval email link, which carries the execution and task IDs); visible only to principals with permission to resolve the relevant suspensions. |
| `suspensions:lift` | `POST /v1/.../integrations/INTEGRATION_NAME/executions/EXECUTION_ID/suspensions/SUSPENSION_ID:lift` | `Suspend`-task variant (confirm with user first). Body accepts optional `suspensionResult` (defaults to `Resolved`). `-` can replace `INTEGRATION_NAME` and either `EXECUTION_ID` or `SUSPENSION_ID` (at least one of `EXECUTION_ID` or `SUSPENSION_ID` must be concrete; omitting both returns an error). Requires `integrations.suspensions.lift` (included in `roles/integrations.suspensionResolver` and `roles/integrations.integrationAdmin`) plus `roles/iam.serviceAccountUser` on `runAsServiceAccount`. |
| `suspensions:resolve` | `POST /v1/.../executions/EXECUTION_ID/suspensions/SUSPENSION_ID:resolve` | Approves or rejects an `Approval` task (same call the console Approve/Reject buttons make; confirm with user first). Body: `{"suspension": {"eventExecutionInfoId": "EXECUTION_ID", "integration": "INTEGRATION_NAME", "taskId": "TASK_ID", "state": "LIFTED"}}` (or `"REJECTED"`). Requires `integrations.suspensions.resolve` (included in `roles/integrations.suspensionResolver` and `roles/integrations.integrationAdmin`) plus `roles/iam.serviceAccountUser` on `runAsServiceAccount`. |
| `generateOpenApiSpec` | `POST /v1/projects/PROJECT_ID/locations/LOCATION:generateOpenApiSpec` | Body requires `apiTriggerResources[]` (`integrationResource` + `triggerId[]`) and `fileFormat` (`JSON` or `YAML`). Generates an OpenAPI 3.0.1 spec for published API-trigger integrations in a single region. Requires `integrations.integrations.generateOpenApiSpec` (included in `roles/integrations.integrationViewer`, `roles/integrations.integrationEditor`, and `roles/integrations.integrationAdmin`, but **not** in `roles/integrations.integrationInvoker`). Used by ADK `ApplicationIntegrationToolset` in **integration mode** (`roles/integrations.integrationInvoker` + `roles/integrations.integrationViewer`); ADK **connection mode** does not call `:generateOpenApiSpec` and instead needs `roles/integrations.integrationInvoker` + `roles/connectors.viewer` (or a custom role with `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata`, which `roles/connectors.invoker` does not have, and `roles/integrations.integrationEditor` holds no `connectors.*` permissions). `roles/secretmanager.secretAccessor` is not needed for the toolset itself (the ADK client does not read Secret Manager). |
| `v2` `integrations:execute` / `:schedule` | `POST /v2/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME:execute` (or `:schedule`) | v2 execution endpoints. |
| `v2` `executions:troubleshoot` | `GET /v2/.../executions/EXECUTION_ID:troubleshoot` | Uses Gemini to return `executionId`, `displayMessage`, `errorMessage`, `rootCause`, and `detailedExplanation` for a failed execution (requires AI features enabled in the region and `integrations.executions.get`). |
| `v2` `taskExecutions.get` | `GET /v2/.../executions/EXECUTION_ID/taskExecutions/TASK_EXECUTION_ID` | Reads individual task execution details in v2. |

For detailed log queries, failure states, and troubleshooting workflows, use the `application-integration-troubleshooting` skill.
