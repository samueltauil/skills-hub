# API Access, Python Client, and ADK

This reference covers supported Application Integration interfaces, REST endpoints, authentication, `curl` and Python discovery client usage, and ADK `ApplicationIntegrationToolset` configuration.

- [Supported Interfaces and What Does Not Exist](#supported-interfaces-and-what-does-not-exist): Lines 12-18
- [Endpoints, Versions, and OAuth Scope](#endpoints-versions-and-oauth-scope): Lines 19-33
- [Authentication](#authentication): Lines 34-51
- [REST API (`curl`) Examples](#rest-api-curl-examples): Lines 52-87
- [Python Discovery Client (`google-api-python-client`)](#python-discovery-client-google-api-python-client): Lines 88-131
- [ADK `ApplicationIntegrationToolset`](#adk-applicationintegrationtoolset): Lines 132-164

## Supported Interfaces and What Does Not Exist

- **No `gcloud` command group**: Neither `gcloud integrations` nor `gcloud connectors` exists. Use `gcloud` only for generic tasks (`gcloud services enable`, `gcloud auth`, `gcloud projects`, `gcloud iam`, `gcloud logging read`).
- **No dedicated Cloud Client Library**: `https://docs.cloud.google.com/application-integration/docs/libraries` returns 404. For Python, use the discovery-based `google-api-python-client` (`pip install "google-api-python-client>=2.100.0,<3" "google-auth>=2.20.0,<3"`) (changes host or credential state; get the user's approval first).
- **No Google-managed remote MCP server**: Neither Application Integration (`integrations.googleapis.com`) nor Integration Connectors (`connectors.googleapis.com`) appears on Google Cloud's remote MCP servers list.
- **Outbound MCP connector vs. MCP server**: Integration Connectors provides an outbound **MCP connector** (`MCP v1` and `v2`) that lets an integration connect out to an external MCP server and expose its tools as connector entities and actions. It does not expose Application Integration itself as a managed MCP server.

## Endpoints, Versions, and OAuth Scope

| Service | Base endpoint | Discovery document |
| :--- | :--- | :--- |
| Application Integration (v1) | `https://integrations.googleapis.com/v1` | `https://integrations.googleapis.com/$discovery/rest?version=v1` |
| Application Integration (v2) | `https://integrations.googleapis.com/v2` | `https://integrations.googleapis.com/$discovery/rest?version=v2` |
| Integration Connectors (v1) | `https://connectors.googleapis.com/v1` | `https://connectors.googleapis.com/$discovery/rest?version=v1` |
| Integration Connectors (v2 runtime) | `https://connectors.googleapis.com/v2` | `https://connectors.googleapis.com/$discovery/rest?version=v2` |

- **OAuth scope**: All documented methods require `https://www.googleapis.com/auth/cloud-platform`.
- **Global vs. regional host**: Use `https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/...` consistently. Some API trigger pages also show `https://LOCATION-integrations.googleapis.com/v1/...`; if you ever encounter a regional host, the host region and `/locations/LOCATION/` path **must** match (the worked example in the API trigger documentation has a mismatched region bug).
- **v1 vs. v2 surface**:
  - `v1` exposes the full authoring, provisioning, versioning, execution, suspension, auth config, and template surface.
  - `v2` exposes `integrations.execute`, `integrations.schedule`, `executions.list`, `executions.troubleshoot` (LLM root-cause explanation of a failed execution), and `executions.taskExecutions.get`.

## Authentication

- **For `curl` (REST)**: Pass a bearer token from the gcloud CLI:
  ```bash
  -H "Authorization: Bearer $(gcloud auth print-access-token)"
  ```
- **For Python and ADK**: Configure Application Default Credentials (ADC) and set the quota project (changes host or credential state; get the user's approval first):
  ```bash
  gcloud auth application-default login
  gcloud auth application-default set-quota-project PROJECT_ID
  ```
- **Service account impersonation**: When testing as a service account (`SA_EMAIL`), the caller needs `roles/iam.serviceAccountTokenCreator` on `SA_EMAIL` (changes host or credential state; get the user's approval first):
  ```bash
  gcloud config set auth/impersonate_service_account SA_EMAIL
  # Unset when finished:
  gcloud config unset auth/impersonate_service_account
  ```

## REST API (`curl`) Examples

### Read-only: list integrations and versions

```bash
# List integrations in LOCATION
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations?pageSize=50"

# List versions of INTEGRATION_NAME
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME/versions"
```

### State-changing: execute a published integration synchronously

Show the exact command and obtain user confirmation before executing an integration. Only an `ACTIVE` (published) integration can be invoked by `:execute`.

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Server-Timeout: 120" \
  -d '{
    "triggerId": "api_trigger/TRIGGER_NAME",
    "inputParameters": {
      "customerId": {"stringValue": "123"}
    }
  }' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME:execute"
```

- **Field names**: Use `"triggerId"` (the REST reference field name) and `"inputParameters"` (a map of variable name to `ValueType` oneof: `stringValue`, `intValue` as string-encoded int64, `doubleValue`, `booleanValue`, `stringArray`, `intArray`, `doubleArray`, `booleanArray`, or `jsonValue`).
- **Integration name `-`**: Passing `-` instead of `INTEGRATION_NAME` executes **all** integrations in `LOCATION` that have the matching `triggerId`; prefer naming `INTEGRATION_NAME` explicitly so only one integration runs.
- **Error check**: An HTTP 200 response alone does not prove every task succeeded. Inspect `outputParameters` and verify the execution record (`ExecutionDetails.state`, per-task `taskExecutionState`, and `ErrorInfo`) via `executions.list?filter=execution_id="EXECUTION_ID"`.

## Python Discovery Client (`google-api-python-client`)

Install dependencies first with `pip install "google-api-python-client>=2.100.0,<3" "google-auth>=2.20.0,<3"` (changes host or credential state; get the user's approval first), then build the v1 service from the discovery document (`integrations` v1 or `connectors` v1).

```python
import google.auth
from googleapiclient.discovery import build

credentials, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
service = build("integrations", "v1", credentials=credentials)

# Read-only: list integrations in a region
parent = "projects/PROJECT_ID/locations/LOCATION"
response = (
    service.projects()
    .locations()
    .integrations()
    .list(parent=parent, pageSize=50)
    .execute()
)
for integration in response.get("integrations", []):
    print(integration["name"], integration.get("active", False))

# State-changing (confirm with user first): execute via API trigger
exec_response = (
    service.projects()
    .locations()
    .integrations()
    .execute(
        name="projects/PROJECT_ID/locations/LOCATION/integrations/INTEGRATION_NAME",
        body={
            "triggerId": "api_trigger/TRIGGER_NAME",
            "inputParameters": {
                "customerId": {"stringValue": "123"},
            },
        },
    )
    .execute()
)
print(exec_response.get("executionId"), exec_response.get("outputParameters"))
```

## ADK `ApplicationIntegrationToolset`

ADK (Python v0.1.0+ and Java v0.3.0+) provides `ApplicationIntegrationToolset` to expose Application Integration workflows or Integration Connectors connections as agent tools.

### Integration mode vs. Connection mode

| Mode | Constructor arguments (Python) | How it works and caveats |
| :--- | :--- | :--- |
| **Integration mode** | Required: `project`, `location`, `integration`, `triggers` (list of trigger IDs such as `["api_trigger/TRIGGER_NAME"]`; pass `[]` to expose all API triggers in the integration—omitting `triggers` fails because ADK Python's `IntegrationClient` requires `triggers` not to be `None`). | Generates agent tools from the published integration's OpenAPI spec (`:generateOpenApiSpec`). `tool_name_prefix` and `tool_instructions` are accepted but **silently ignored** in integration mode. |
| **Connection mode** | Required: `project`, `location`, `connection`, plus at least one of `entity_operations` (dict of entity -> list of ops; `[]` means all ops) or `actions`. | Calls an integration named `ExecuteConnection` (from the Connection Tool template, usually auto-created on region provisioning, or overridden via `connection_template_override` in Python SDK v1.21.0+). Application Integration **must** be provisioned in the same region as the connection. |

### ADK Python example (Integration mode)

```python
from google.adk.tools.application_integration_tool.application_integration_toolset import (
    ApplicationIntegrationToolset,
)

integration_tools = ApplicationIntegrationToolset(
    project="PROJECT_ID",
    location="LOCATION",
    integration="INTEGRATION_NAME",
    triggers=["api_trigger/TRIGGER_NAME"],
)
```

### ADK IAM and authentication gotchas

- **IAM roles depend on mode**:
  - **Integration mode**: Grant `roles/integrations.integrationInvoker` + `roles/integrations.integrationViewer`. In integration mode, `ApplicationIntegrationToolset` fetches the tool schema via `POST .../locations/LOCATION:generateOpenApiSpec`, which requires `integrations.integrations.generateOpenApiSpec`. `roles/integrations.integrationInvoker` does **not** contain `integrations.integrations.generateOpenApiSpec` (`roles/integrations.integrationViewer` and `roles/integrations.integrationEditor` do), so granting `roles/integrations.integrationInvoker` alone fails with 403 wherever the agent runs (not only on Agent Runtime). Use `roles/integrations.integrationEditor` only as a broad alternative for integration mode (it also grants version create, update, delete, and publish permissions, and holds no `connectors.*` permissions).
  - **Connection mode**: Grant `roles/integrations.integrationInvoker` (to `:execute` the `ExecuteConnection` integration) + `roles/connectors.viewer` (or a custom role with `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata`). When constructed using the agent's own credentials, the toolset calls `GET .../connections/CONNECTION?view=BASIC`, `connectionSchemaMetadata:getEntityType`, and `connectionSchemaMetadata:getAction`, which require `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata` (`roles/connectors.viewer` includes both; `roles/connectors.invoker` does **not**, and `roles/integrations.integrationEditor` holds no `connectors.*` permissions). Connection mode does **not** call `:generateOpenApiSpec`, so `roles/integrations.integrationViewer` is needed only in integration mode. `roles/secretmanager.secretAccessor` is not needed for the toolset itself (the ADK client does not read Secret Manager).
- **Dynamic OAuth2 (`auth_scheme` / `auth_credential`)**: Only takes effect in Python connection mode when the connection has `authOverrideEnabled`; otherwise the dynamic credential is ignored with a warning.
- **Java positional constructor**: Java uses positional arguments `(project, location, integration, triggers, connection, entityOperations, actions, serviceAccountJson, toolNamePrefix, toolInstructions)` and does not support `auth_scheme`, `auth_credential`, or `connection_template_override`.
