# IntegrationVersion JSON Reference

This guide details the `IntegrationVersion` JSON schema used by `versions.create`, `versions.patch`, `versions:upload`, and `versions:download` in the v1 REST API.

- [Top-Level `IntegrationVersion` Fields](#top-level-integrationversion-fields): Lines 12-37
- [Trigger Configuration (`TriggerConfig`)](#trigger-configuration-triggerconfig): Lines 38-55
- [Task Configuration (`TaskConfig`)](#task-configuration-taskconfig): Lines 56-74
- [Variables and `ValueType` (`IntegrationParameter`)](#variables-and-valuetype-integrationparameter): Lines 75-108
- [Config Variables (`IntegrationConfigParameter`)](#config-variables-integrationconfigparameter): Lines 109-118
- [Minimal `IntegrationVersion` JSON Template](#minimal-integrationversion-json-template): Lines 119-196

## Top-Level `IntegrationVersion` Fields

| Field | Mode | Description |
| :--- | :--- | :--- |
| `name` | Output only | Resource path: `projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/versions/VERSION_ID`. |
| `description` | Optional | Human-readable version description. |
| `userLabel` | Optional | User-assigned version label. |
| `state` | Output only | `INTEGRATION_STATE_UNSPECIFIED`, `DRAFT`, `ACTIVE`, `ARCHIVED`, or `SNAPSHOT`. |
| `snapshotNumber` | Output only | Monotonically increasing version snapshot number. |
| `lockHolder` | Optional | Email of the author currently holding the 15-minute `DRAFT` edit lock (`versions:publish` and `versions.delete` fail on a `DRAFT` if the caller is not `lockHolder`). |
| `lastModifierEmail` | Optional | Email of the last user who modified this version. |
| `createTime` / `updateTime` | Output only | RFC 3339 creation and last-modified timestamps. |
| `runAsServiceAccount` | Optional | Dedicated service account email. When set and no authentication profile (`authConfig`) is configured on the task, it is used to generate the auth token for Connector (`Connectors`), REST (`Call REST Endpoint`), and Cloud Function tasks; an authentication profile configured on the task takes precedence over `runAsServiceAccount`. Integrations created on or after October 15, 2026 with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce, or Connector Event) cannot be tested or published unless `runAsServiceAccount` is set (Private triggers are exempt like API triggers, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount`); whenever `runAsServiceAccount` is set, the user publishing or testing the version needs `roles/iam.serviceAccountUser` on it. |
| `triggerConfigs` | Repeated | Trigger definitions (`TriggerConfig[]`) that start the workflow. |
| `taskConfigs` | Repeated | Task definitions (`TaskConfig[]`) that execute work. |
| `integrationParameters` | Repeated | Input, output, and transient workflow variables (`IntegrationParameter[]`). |
| `integrationConfigParameters` | Repeated | Environment-specific config variables (`IntegrationConfigParameter[]`). |
| `errorCatcherConfigs` | Repeated | Error catcher flows triggered when tasks or triggers fail. |
| `cloudLoggingDetails` | Optional | Controls Cloud Logging (`enableCloudLogging` boolean, `cloudLoggingSeverity` of `INFO`, `ERROR`, or `WARNING`). |
| `databasePersistencePolicy` | Optional | Controls database persistence (local logging) for execution data: `DATABASE_PERSISTENCE_POLICY_UNSPECIFIED` = `Enable (sync)` (the API default—a version built over REST without `databasePersistencePolicy` persists synchronously), `DATABASE_PERSISTENCE_ASYNC` = `Enable (async)` (the console default), or `DATABASE_PERSISTENCE_DISABLED` = `Disable`. |
| `enableVariableMasking` | Optional | Masks variable values in logs (Preview). Does **not** redact downloaded version files. |
| `cloudKmsKey` | Optional | CMEK key reference when regional CMEK is enabled. |
| `teardown` | Optional (deprecated) | Teardown configuration for the integration (marked deprecated in the v1 discovery document). |

- **Deprecated fields**: Never populate `taskConfigsInternal`, `triggerConfigsInternal`, or `integrationParametersInternal`. They are deprecated in favor of `taskConfigs`, `triggerConfigs`, and `integrationParameters`.

## Trigger Configuration (`TriggerConfig`)

Each trigger in `triggerConfigs[]` defines an entry point and the initial `startTasks` to invoke.

| Field | Required | Description |
| :--- | :--- | :--- |
| `triggerNumber` | Yes | Unique string identifier for this trigger within the version (for example, `"1"`). |
| `triggerType` | No | `API`, `CRON`, `CLOUD_PUBSUB_EXTERNAL`, `CLOUD_SCHEDULER`, `SFDC_CHANNEL`, `SFDC_CDC_CHANNEL`, `INTEGRATION_CONNECTOR_TRIGGER`, `PRIVATE_TRIGGER`, or `EVENTARC_TRIGGER`. |
| `triggerId` | No | Auto-generated invocation identifier (optional in payload; derived from `properties`). For API triggers: `api_trigger/TRIGGER_NAME`. For private triggers: `private_trigger/TRIGGER_NAME`. |
| `label` | No | Display label in the editor (for example, `"API Trigger"`). |
| `properties` | No | Trigger-specific key-value properties (for example, `{"Trigger name": "TRIGGER_NAME"}` for API triggers). |
| `startTasks` | No | Array of `{ "taskId": "1" }` objects naming the first task(s) to run. |
| `nextTasksExecutionPolicy` | No | Controls how multiple `startTasks` are evaluated (`RUN_ALL_MATCH` or `RUN_FIRST_MATCH`). |
| `errorCatcherId` | No | Attaches an error catcher flow to this trigger (at most one per trigger). |
| `inputVariables` / `outputVariables` | No | Trigger-scoped input and output variable names. |
| `cloudSchedulerConfig` | No | Configuration block when `triggerType` is `CLOUD_SCHEDULER`. |
| `alertConfig` | No | Alert thresholds attached to the trigger. |

## Task Configuration (`TaskConfig`)

Each task in `taskConfigs[]` represents one step in the DAG. An integration can contain at most 100 tasks.

| Field | Required | Description |
| :--- | :--- | :--- |
| `taskId` | Yes | Unique string identifier within the integration (for example, `"1"`, `"2"`). |
| `task` | No | Task type identifier (for example, `EmailTask` in the public upload guide, or `FieldMappingTask` in the API discovery document). |
| `displayName` | No | Human-readable label shown in the editor and execution logs. |
| `parameters` | No | Map of parameter key to `EventParameter` (`{"key": "...", "value": {ValueType}}`). |
| `nextTasks` | No | Outgoing edges: array of `{"taskId": "2", "condition": "$amount$ > 0"}`. |
| `nextTasksExecutionPolicy` | No | `RUN_ALL_MATCH` (runs all downstream tasks whose edge condition matches) or `RUN_FIRST_MATCH`. |
| `taskExecutionStrategy` | No | Join behavior when multiple upstream tasks point here: `WHEN_ALL_SUCCEED`, `WHEN_ANY_SUCCEED`, or `WHEN_ALL_TASKS_AND_CONDITIONS_SUCCEED`. |
| `failurePolicy` | No | Retry strategy on temporary errors: `retryStrategy` (`FATAL`, `IGNORE`, `NONE`, `RESTART_INTEGRATION_WITH_BACKOFF`, `EXPONENTIAL_BACKOFF`, `FIXED_INTERVAL`, `LINEAR_BACKOFF`), `maxRetries`, `intervalTime`, `condition`. |
| `synchronousCallFailurePolicy` | No | Retry policy used specifically during synchronous execution. |
| `conditionalFailurePolicies` | No | Conditional retry configuration (`failurePolicies[]` evaluated in order, plus `defaultFailurePolicy` when none match). |
| `errorCatcherId` | No | ID of the error catcher flow to run after retry policies are exhausted (at most one per task). |
| `jsonValidationOption` | No | Controls JSON schema validation for task inputs/outputs. |

## Variables and `ValueType` (`IntegrationParameter`)

Variables in `integrationParameters[]` define the integration's typed inputs, outputs, and working state.

### `IntegrationParameter` Fields

| Field | Description |
| :--- | :--- |
| `key` | Variable name (for example, `orderId`). Referenced in expressions as `$orderId$`. |
| `dataType` | `STRING_VALUE`, `INT_VALUE`, `DOUBLE_VALUE`, `BOOLEAN_VALUE`, `STRING_ARRAY`, `INT_ARRAY`, `DOUBLE_ARRAY`, `BOOLEAN_ARRAY`, or `JSON_VALUE`. |
| `inputOutputType` | `IN` (input only), `OUT` (output only), `IN_OUT` (both), or `IN_OUT_TYPE_UNSPECIFIED` (default, for internal variables). |
| `defaultValue` | `ValueType` object used when the trigger does not supply a dynamic value. A dynamic trigger input always overrides `defaultValue`. |
| `isTransient` | Boolean; indicates whether this parameter is a transient parameter. |
| `masked` | Boolean; masks the variable value in execution logs. |
| `searchable` | Boolean; indexes the variable for execution log filtering. |
| `containsLargeData` | Boolean hint for large payloads. |
| `jsonSchema` | Optional JSON Schema string when `dataType` is `JSON_VALUE`. |

### `ValueType` Oneof Encoding

Every `ValueType` object (used in `defaultValue` on `IntegrationParameter` and `integrationConfigParameters[].parameter.defaultValue`, and in `inputParameters` on `:execute`/`:schedule`) contains **exactly one** of these fields:

| `dataType` | `ValueType` Field | JSON Encoding Note |
| :--- | :--- | :--- |
| `STRING_VALUE` | `{"stringValue": "hello"}` | UTF-8 string (max 20 MB in Data Mapping). |
| `INT_VALUE` | `{"intValue": "42"}` | **String-encoded** 64-bit integer (not a raw JSON number). |
| `DOUBLE_VALUE` | `{"doubleValue": 3.14}` | JSON number. |
| `BOOLEAN_VALUE` | `{"booleanValue": true}` | JSON boolean. |
| `JSON_VALUE` | `{"jsonValue": "{\"id\":1}"}` | **String-encoded** JSON document (not an inline JSON object). |
| `STRING_ARRAY` | `{"stringArray": {"stringValues": ["a", "b"]}}` | Object wrapping `stringValues[]`. |
| `INT_ARRAY` | `{"intArray": {"intValues": ["1", "2"]}}` | Object wrapping string-encoded `intValues[]`. |
| `DOUBLE_ARRAY` | `{"doubleArray": {"doubleValues": [1.5, 2.5]}}` | Object wrapping `doubleValues[]`. |
| `BOOLEAN_ARRAY` | `{"booleanArray": {"booleanValues": [true, false]}}` | Object wrapping `booleanValues[]`. |

## Config Variables (`IntegrationConfigParameter`)

Config variables (Preview) separate environment-specific configuration from workflow logic so the same version JSON can be promoted across projects without editing tasks.

- **Naming rule**: In the REST API, config variable keys must use the `CONFIG_` prefix wrapped in backticks: `` `CONFIG_<NAME>` `` (the Cloud console adds `CONFIG_` automatically). Reference them in expressions as `` $`CONFIG_<NAME>`$ ``.
- **Schema in `integrationConfigParameters[]`**: Config variable defaults belong in `parameter.defaultValue` inside `integrationConfigParameters[]`—for example, `{"parameter": {"key": "`CONFIG_backend_url`", "dataType": "STRING_VALUE", "displayName": "Backend URL", "defaultValue": {"stringValue": "https://api.example.com"}}}`. A top-level `value` in uploaded or created draft JSON is discarded, so per-environment values go in `configParameters` at publish.
- **Supplying values at publish**: Pass `{"configParameters": {"`CONFIG_<NAME>`": "target-value"}}` in the `POST .../versions/VERSION_ID:publish` body (`configParameters` is a `google.protobuf.Struct`, so values are plain JSON primitives/objects rather than `ValueType` wrappers). **Gotcha**: Keys in `configParameters` must **exactly match** a key in `integrationConfigParameters`, backticks included (for example, `` "`CONFIG_target_url`" ``); unknown keys are **silently ignored**, not rejected (`versions:publish` returns 200 and the default stays).
- **Security limitation**: Config variables are **not** a secret store. Their values are stored and exported in plain text when downloading a version (`versions:download`) or sharing a template, even if variable masking is enabled. Never store API keys, passwords, or tokens in config variables; use `projects.locations.authConfigs` or the Secret Manager access task.
- **Connector limitation**: Config variables cannot be used to parameterize Integration Connectors entity operations or actions.

## Minimal `IntegrationVersion` JSON Template

Save this runnable template to a file (for example, `version.json`). Pass it to `versions:upload` wrapped in `{"content": "<escaped-json>", "fileFormat": "JSON"}`—`versions:upload` creates the integration automatically if it does not exist yet, or adds a new `DRAFT` version if it does (the uploaded `DRAFT` still requires `versions:publish`). Alternatively, pass the JSON directly to `POST .../versions?newIntegration=true` only when you want the call to fail with `ALREADY_EXISTS` if `INTEGRATION_NAME` already exists. The template sets `runAsServiceAccount` (`RUN_AS_SA`, such as `order-workflow-sa@PROJECT_ID.iam.gserviceaccount.com`) because projects with governance require a run-as service account to publish, and the caller needs `roles/iam.serviceAccountUser` on it. The `EmailTask` uses the customer-visible parameter keys `"To"` (`stringArray`), `"Subject"` (`stringValue`), `"BodyFormat"` (`stringValue`, such as `"PLAIN_TEXT"`), and `"TextBody"` (`stringValue`). Running this workflow sends a real email, so always confirm `RECIPIENT_EMAIL` and each state-changing call (upload/create, publish, and execute) with the user first.

```json
{
  "description": "API-triggered order notification integration",
  "runAsServiceAccount": "order-workflow-sa@PROJECT_ID.iam.gserviceaccount.com",
  "cloudLoggingDetails": {
    "enableCloudLogging": true,
    "cloudLoggingSeverity": "INFO"
  },
  "triggerConfigs": [
    {
      "label": "API Trigger",
      "triggerType": "API",
      "triggerNumber": "1",
      "triggerId": "api_trigger/TRIGGER_NAME",
      "properties": {
        "Trigger name": "TRIGGER_NAME"
      },
      "startTasks": [
        {
          "taskId": "1"
        }
      ]
    }
  ],
  "taskConfigs": [
    {
      "task": "EmailTask",
      "taskId": "1",
      "displayName": "Send Email",
      "taskExecutionStrategy": "WHEN_ALL_SUCCEED",
      "parameters": {
        "To": {
          "key": "To",
          "value": {
            "stringArray": {
              "stringValues": [
                "RECIPIENT_EMAIL"
              ]
            }
          }
        },
        "Subject": {
          "key": "Subject",
          "value": {
            "stringValue": "Order notification for $orderId$"
          }
        },
        "BodyFormat": {
          "key": "BodyFormat",
          "value": {
            "stringValue": "PLAIN_TEXT"
          }
        },
        "TextBody": {
          "key": "TextBody",
          "value": {
            "stringValue": "Processing order $orderId$."
          }
        }
      }
    }
  ],
  "integrationParameters": [
    {
      "key": "orderId",
      "dataType": "STRING_VALUE",
      "inputOutputType": "IN_OUT",
      "defaultValue": {
        "stringValue": "ORD-0000"
      }
    }
  ]
}
```
