# Integration Connectors Health and Schema Troubleshooting

Use this reference when a Connectors task or Connector Event trigger fails. It separates broken connections (`ERROR`, `AUTHORIZATION_REQUIRED`, `INACTIVE`, schema failures, node throttling) from caller IAM failures (a Connectors role such as `roles/connectors.invoker` or `roles/connectors.admin`).

- [Diagnostic Decision Flow: Connection vs Caller IAM](#diagnostic-decision-flow-connection-vs-caller-iam): Lines 12-21
- [Step 1: Check Connection State (`connections.get`)](#step-1-check-connection-state-connectionsget): Lines 22-39
- [Step 2: Check Eventing State (Connector Event Triggers)](#step-2-check-eventing-state-connector-event-triggers): Lines 40-59
- [Step 3: Check Schema Metadata and Runtime Readiness](#step-3-check-schema-metadata-and-runtime-readiness): Lines 60-96
- [Step 4: Separate Connection Auth from Caller IAM](#step-4-separate-connection-auth-from-caller-iam): Lines 97-109
- [Step 5: Check Throttling (HTTP 429) and Connectors Limits](#step-5-check-throttling-http-429-and-connectors-limits): Lines 110-131

## Diagnostic Decision Flow: Connection vs Caller IAM

1. **Fetch the connection resource** with `view=FULL` (`connections.get`).
2. **Check `status.state`:**
   - If `ERROR`, `AUTHORIZATION_REQUIRED`, `INACTIVE`, `CREATING`, `UPDATING`, or `DELETING`, the connection itself is not ready. Fix the connection first.
   - If `ACTIVE`, the connection is up and ready for requests.
3. **If `ACTIVE` and using a Connector Event trigger,** check `eventingStatus.state` (`ACTIVE` vs `ERROR` or `INGRESS_ENDPOINT_REQUIRED`).
4. **If `ACTIVE` and an entity or action fails,** check `connectionSchemaMetadata` (`state` and `errorMessage`) and runtime v2 `checkStatus` / `checkReadiness`.
5. **If the connection and schema are healthy,** check caller IAM (a Connectors role such as `roles/connectors.invoker` or `roles/connectors.admin` on the integration's run-as service account) and task payload/timeout limits.

## Step 1: Check Connection State (`connections.get`)

`GET https://connectors.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME` returns `ConnectionStatus` under `status`. Pass `view=FULL` (default is `BASIC`) to inspect full configuration and status details.

```bash
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://connectors.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME?view=FULL"
```

| `ConnectionStatus.state` | Meaning | Next step |
|---|---|---|
| `ACTIVE` | Running and ready for requests. | Proceed to Step 2 (schema/eventing) or Step 4 (caller IAM). |
| `ERROR` | Not running due to an error. | Read `status.status` for the detailed error message. Check target host reachability, Endpoint Attachment / Managed Zone (for private backends), and Secret Manager credentials. |
| `AUTHORIZATION_REQUIRED` | Authorization configuration is incomplete. | Complete OAuth authorization or credential setup in `https://console.cloud.google.com/connectors/connections`. |
| `INACTIVE` | Connection is stopped / suspended. | Resume the connection in the Cloud console, or set `suspended: false` via `connections.patch` with `updateMask=suspended` (requires user confirmation). |
| `CREATING` / `UPDATING` | Provisioning or update in progress. | Wait for `ACTIVE` before running tasks. |
| `DELETING` | Being deleted. | Update the integration to point to an active connection. |

## Step 2: Check Eventing State (Connector Event Triggers)

For integrations started by a Connector Event trigger, inspect `eventingStatus.state` on the connection response:

| `EventingStatus.state` | Meaning |
|---|---|
| `ACTIVE` | Event subscriptions are active. |
| `ERROR` | Eventing failed. You can attempt repair via `:repairEventing` (after user confirmation). |
| `INGRESS_ENDPOINT_REQUIRED` | Ingress endpoint configuration is missing for event delivery. |

To repair event subscriptions (state-changing; show command and get user confirmation first):

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "https://connectors.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME:repairEventing"
```

## Step 3: Check Schema Metadata and Runtime Readiness

If `ConnectionStatus.state` is `ACTIVE` but the Connectors task cannot find or run an entity or action, inspect `connectionSchemaMetadata` (for `state` and `errorMessage`) and list available actions or entity types via the runtime v2 API.

```bash
# Primary probe for schema state and errorMessage on CONNECTION_NAME (read-only, no filter)
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://connectors.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME/connectionSchemaMetadata"

# List discovered actions via runtime v2 actions.list (read-only)
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://connectors.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME/actions"

# List discovered entity types via runtime v2 entityTypes.list (read-only)
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://connectors.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME/entityTypes"
```

- **Why use `GET .../connectionSchemaMetadata` and runtime v2 `actions.list` / `entityTypes.list`:** `GET https://connectors.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME/connectionSchemaMetadata` (no filter) is the primary probe for `state` and `errorMessage`. For listing actions and entity types, use runtime v2 `actions.list` (`GET https://connectors.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME/actions`) and `entityTypes.list` (`GET https://connectors.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME/entityTypes`)—the v1 `connectionSchemaMetadata:listActions` and `connectionSchemaMetadata:listEntityTypes` methods **require** a `filter` query parameter (calls without a filter are rejected, and wildcards are not supported).
- **Schema states (`ConnectionSchemaMetadata.state`):** `STATE_UNSPECIFIED`, `REFRESHING`, `UPDATED`, `REFRESHING_SCHEMA_METADATA`, `UPDATED_SCHEMA_METADATA`, `REFRESH_SCHEMA_METADATA_FAILED` (check `errorMessage`), `REFRESHING_FULL_SCHEMA`, `UPDATED_FULL_SCHEMA`.
- **Additional read methods:** `:getEntityType` and `:getAction`.
- **Refresh schema (state-changing; ask user confirmation first):**
  ```bash
  curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{}' \
    "https://connectors.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME/connectionSchemaMetadata:refresh"
  ```

### Runtime v2 Health Probes

The Integration Connectors v2 data-plane API (`https://connectors.googleapis.com/v2/...`) exposes direct runtime checks on a connection:
- `GET .../v2/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME:checkStatus`
- `GET .../v2/projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_NAME:checkReadiness`
- It also exposes `actions.list`, `actions.get`, `entityTypes.list`, `entityTypes.get`, entity CRUD (`entities.list`/`get`/`create`/`patch`/`delete`), `connections:executeSqlQuery`, and `connections/CONNECTION_NAME/actions/ACTION_NAME:execute` (ask user confirmation before running write actions or SQL queries).

## Step 4: Separate Connection Auth from Caller IAM

A connection has two independent authentication hops:

| Hop | Principal | Where credentials / roles live | Symptom when broken |
|---|---|---|---|
| **1. Caller -> Connection** | Integration's `runAsServiceAccount` (or default `service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com` if none set) | IAM in the connection's Google Cloud project (a Connectors role such as `roles/connectors.invoker` or `roles/connectors.admin`). | Connection `status.state` is `ACTIVE`, but the Connectors task fails with HTTP 403 `PERMISSION_DENIED`. |
| **2. Connection -> Target backend** | Connection's own configured auth (Secret Manager secret, OAuth token, or connection service account) | Connection config in Integration Connectors + target SaaS/DB. | `ConnectionStatus.state` is `ERROR` or `AUTHORIZATION_REQUIRED`, or v2 `checkStatus` fails. |

### Cross-Project Service Account on a Connection

If a connection itself is configured to act as a service account from **another** Google Cloud project, the Integration Connectors service agent (`service-PROJECT_NUMBER@gcp-sa-connectors.iam.gserviceaccount.com`) must hold `roles/iam.serviceAccountTokenCreator` on that service account in the other project.

## Step 5: Check Throttling (HTTP 429) and Connectors Limits

### Node Throttling (HTTP 429)

- Each connection scales between its configured minimum and maximum nodes (up to 100 nodes per connection; up to 50 connections per region and 20 unique regions).
- When traffic exceeds the connection's active node capacity, requests fail with **HTTP 429**.
- **Remediation:**
  1. Check `connectors.googleapis.com/connection/nodes` and `connection/response_count` (filtered by `code="429"`) in Cloud Monitoring.
  2. Raise the minimum or maximum node count on the connection. Note that an active billing account must be attached to the project even when usage stays within the monthly free tier, and additional nodes beyond the free tier incur charges; check the [Application Integration pricing page](https://cloud.google.com/application-integration/pricing) and the Google Cloud Pricing Calculator before scaling nodes.
  3. Configure a task retry strategy (such as `EXPONENTIAL_BACKOFF`) on the Connectors task in the integration.

### Connectors Task Limits

| Limit | Value |
|---|---|
| **Connectors task timeout** | 3 minutes |
| **Data sent to / from a connection** | 8 MB max (Application Integration quota) |
| **Maximum Connectors task payload** | 10 MB (Integration Connectors quota) |
| **Maximum connector response** | 20 MB |
| **Execute Custom Query timeout / rows** | 180 seconds / 50,000 rows max |
| **List entities pagination** | Default page size 25, max 50,000 pages |
| **Cross-region support** | An integration and the connection it calls can be in different regions (except ADK `ApplicationIntegrationToolset` connection mode, which requires the same region). |
