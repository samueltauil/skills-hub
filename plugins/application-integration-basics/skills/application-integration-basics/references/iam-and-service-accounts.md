# IAM and Service Accounts

This reference covers predefined IAM roles for Application Integration and Integration Connectors, service agents, the October 15, 2026 run-as service account rules, and `gcloud` IAM commands.

- [Safety Rule](#safety-rule): Lines 14-17
- [Roles for Initial Product Setup](#roles-for-initial-product-setup): Lines 18-25
- [Application Integration Predefined Roles](#application-integration-predefined-roles): Lines 26-42
- [Integration Connectors Predefined Roles](#integration-connectors-predefined-roles): Lines 43-55
- [Task-to-Role Quick Map](#task-to-role-quick-map): Lines 56-71
- [Service Agents](#service-agents): Lines 72-82
- [Run-As Service Account and October 15, 2026 Rules](#run-as-service-account-and-october-15-2026-rules): Lines 83-102
- [gcloud IAM Commands](#gcloud-iam-commands): Lines 103-140

## Safety Rule

Read-only IAM policy inspections (`gcloud projects get-iam-policy`, `gcloud iam service-accounts get-iam-policy`) run freely. Always show the exact command and obtain explicit user confirmation before adding or removing any IAM policy binding.

## Roles for Initial Product Setup

To set up Application Integration and provision a region in `PROJECT_ID`, the administrator needs:
- `roles/integrations.integrationAdmin`
- `roles/connectors.admin`
- `roles/editor`
- `roles/cloudkms.admin` (required only when configuring Customer-Managed Encryption Keys)

## Application Integration Predefined Roles

| Role | Title | What it grants |
| :--- | :--- | :--- |
| `roles/integrations.integrationAdmin` | Application Integration Admin | Full CRUD access to all integrations, versions, executions, suspensions, and authentication profiles (required to delete auth profiles). |
| `roles/integrations.integrationEditor` | Application Integration Editor | List, create, and update integrations; create and edit auth profiles; invoke, cancel, replay, and publish/unpublish integrations (`integrations.integrationVersions.deploy`). Holds no `connectors.*` permissions. |
| `roles/integrations.integrationDeployer` | Application Integration Deployer | Deploy (publish) and undeploy (unpublish) integration versions to the runtime (`integrations.integrationVersions.list`, `get`, `deploy`; does not include `integrations.integrationVersions.create`, so `integrationDeployer` alone can publish an existing version but cannot upload via `versions:upload`). |
| `roles/integrations.integrationInvoker` | Application Integration Invoker | Invoke published integrations (`integrations.integrations.invoke`), run test cases (`integrations.testCases.invoke`), cancel executions (`integrations.executions.cancel`), and replay executions (`integrations.executions.replay`). |
| `roles/integrations.integrationViewer` | Application Integration Viewer | Read-only access to list and view integrations, versions, and execution logs, and generate OpenAPI specs (`integrations.integrations.generateOpenApiSpec`). |
| `roles/integrations.suspensionResolver` | Application Integration Approver | List, lift, and resolve suspended executions and Approval tasks (`integrations.suspensions.list`, `integrations.suspensions.lift`, `integrations.suspensions.resolve`; does not grant `integrations.executions.list`, `integrations.executions.get`, `integrations.executions.cancel`, or `integrations.executions.replay`, so `suspensionResolver` alone cannot read execution records or run `:troubleshoot`). |
| `roles/integrations.serviceAgent` | Application Integration Service Agent | Service agent role granting access to execute integrations (also listed for testing or publishing on the project). |
| `roles/integrations.certificateViewer` | Certificate Viewer | View certificates used by integrations. |
| `roles/integrations.sfdcInstanceAdmin` | Application Integration SFDC Instance Admin | Full CRUD access to all SFDC instances (`sfdcInstanceEditor` and `sfdcInstanceViewer` also exist). |
| `roles/integrations.admin` | Integrations Admin | Broad `integrations.*` access (`roles/integrations.viewer` is the read-only counterpart). |

Apigee Integration roles also exist in IAM (`roles/integrations.apigeeIntegrationAdminRole`, `apigeeIntegrationDeployerRole`, `apigeeIntegrationEditorRole`, `apigeeIntegrationInvokerRole`, `apigeeIntegrationsViewer`, `apigeeSuspensionResolver`, and Beta `roles/integrations.securityIntegrationAdmin`).

## Integration Connectors Predefined Roles

| Role | Title | What it grants |
| :--- | :--- | :--- |
| `roles/connectors.admin` | Connector Admin | Full access to all Integration Connectors resources. |
| `roles/connectors.editor` | Connectors Editor | Create and update Integration Connectors resources. |
| `roles/connectors.viewer` | Connectors Viewer | Read-only access to Integration Connectors resources (includes `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata`). |
| `roles/connectors.invoker` | Connector Invoker | Invoke all entity and action operations on connections (does **not** include `connectors.connections.get` or `connectors.connections.getConnectionSchemaMetadata`). |
| `roles/connectors.listener` | Connector Event Listener | Listen to Connector Event subscriptions. |
| `roles/connectors.serviceAgent` | Connectors Platform Service Agent | Service agent role for the Integration Connectors service agent. |

Additional scoped roles exist for sub-resources: `roles/connectors.customConnectorAdmin` / `customConnectorViewer`, `roles/connectors.endpointAttachmentAdmin` / `endpointAttachmentViewer`, `roles/connectors.eventSubscriptionAdmin` / `eventSubscriptionViewer`, and `roles/connectors.managedZoneAdmin` / `managedZoneViewer`.

## Task-to-Role Quick Map

| Action | Minimum predefined role |
| :--- | :--- |
| View integrations | `roles/integrations.integrationViewer` |
| View execution logs | `roles/integrations.integrationViewer` or `roles/integrations.integrationInvoker` |
| Run / invoke (`:execute` / `:schedule`) | `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, or `roles/integrations.integrationAdmin` (`integrations.integrations.invoke`) |
| Replay execution (`:replay`) | `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, or `roles/integrations.integrationAdmin` (`integrations.executions.replay`; **not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`) |
| Cancel execution (`:cancel`) | `roles/integrations.integrationInvoker`, `roles/integrations.integrationEditor`, or `roles/integrations.integrationAdmin` (`integrations.executions.cancel`; **not** in `roles/integrations.suspensionResolver` or `roles/integrations.integrationViewer`, so approvers with only `roles/integrations.suspensionResolver` cannot cancel a stuck `SUSPENDED` run) |
| Create, upload (`versions:upload`), edit, or test draft versions, or create/edit auth profiles | `roles/integrations.integrationEditor` (covers `versions:upload` and `versions:publish`; plus `roles/iam.serviceAccountUser` on `runAsServiceAccount` for the user testing or publishing the version whenever `runAsServiceAccount` is set) |
| Delete auth profiles | `roles/integrations.integrationAdmin` |
| Publish or unpublish versions | `roles/integrations.integrationDeployer` or `roles/integrations.integrationEditor` (`integrations.integrationVersions.deploy`, plus `roles/iam.serviceAccountUser` on `runAsServiceAccount` for the user publishing the version whenever `runAsServiceAccount` is set; `roles/integrations.integrationDeployer` alone can publish but cannot upload via `versions:upload`, which requires `integrations.integrationVersions.create`) |
| List, approve (`:resolve`), or lift (`:lift`) a suspended execution | `roles/integrations.suspensionResolver` or `roles/integrations.integrationAdmin` (`integrations.suspensions.list` for `suspensions.list`, `integrations.suspensions.resolve` for `:resolve` [Approval], `integrations.suspensions.lift` for `:lift` [Suspend]) **plus** `roles/iam.serviceAccountUser` on the run-as service account. `roles/integrations.suspensionResolver` alone cannot read execution records (no `integrations.executions.list` or `integrations.executions.get`, returning HTTP 403 on `executions.list` and v2 `:troubleshoot`); to inspect `taskExecutionDetails` (or run `:troubleshoot`), also grant `roles/integrations.integrationViewer` (or use the approval email link, which carries the execution and task IDs). |
| Call a sub-integration (`Call Integration` task) | Caller service account needs `roles/integrations.integrationInvoker` |
| Run ADK `ApplicationIntegrationToolset` | **Depends on mode**: **Integration mode** needs `roles/integrations.integrationInvoker` + `roles/integrations.integrationViewer` (`integrationViewer` supplies `integrations.integrations.generateOpenApiSpec` for `POST .../locations/LOCATION:generateOpenApiSpec`, which `integrationInvoker` does **not** have, so `integrationInvoker` alone fails with 403 wherever the agent runs; `roles/integrations.integrationEditor` is only a broad alternative because it also grants version create/update/delete/publish and holds no `connectors.*` permissions). **Connection mode** needs `roles/integrations.integrationInvoker` (to `:execute` the `ExecuteConnection` integration) + `roles/connectors.viewer` (or a custom role with `connectors.connections.get` and `connectors.connections.getConnectionSchemaMetadata`, which the toolset needs when constructed using the agent's credentials to call `GET .../connections/CONNECTION?view=BASIC`, `connectionSchemaMetadata:getEntityType`, and `connectionSchemaMetadata:getAction`; `roles/connectors.invoker` does **not** have those permissions). Connection mode does **not** call `:generateOpenApiSpec` (`integrationViewer` is only needed in integration mode). `roles/secretmanager.secretAccessor` is not needed for the toolset itself (the ADK client does not read Secret Manager). |

## Service Agents

Two Google-managed service agents are used in `PROJECT_ID`:

| Service | Service agent email | Default role |
| :--- | :--- | :--- |
| Application Integration (`integrations.googleapis.com`) | `service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com` | `roles/integrations.serviceAgent` |
| Integration Connectors (`connectors.googleapis.com`) | `service-PROJECT_NUMBER@gcp-sa-connectors.iam.gserviceaccount.com` | `roles/connectors.serviceAgent` |

- **Cross-project connection service account**: If an Integration Connectors connection uses a user-managed service account from a different Google Cloud project, grant `service-PROJECT_NUMBER@gcp-sa-connectors.iam.gserviceaccount.com` the `roles/iam.serviceAccountTokenCreator` role in that other project.

## Run-As Service Account and October 15, 2026 Rules

A user-managed **run-as service account** is set per integration version via `IntegrationVersion.runAsServiceAccount` (or **Integration settings > Service account** in the Cloud console, followed by **Publish**). Region provisioning (`clients:provision` and Terraform `google_integrations_client`) does **not** apply `runAsServiceAccount`.

### Credential precedence for tasks

When a task calls an external service (`Connectors`, `Call REST Endpoint`, or `Cloud Function`):
1. **Task-level auth profile wins**: If an OAuth 2.0 profile (or OIDC profile on a `Cloud Function` task) and a user-managed `runAsServiceAccount` are both configured, the auth profile is used by default.
2. **Run-as service account**: If `runAsServiceAccount` is set on the version and no auth profile is attached to the task, `runAsServiceAccount` mints the outbound token.
3. **Default service agent**: If neither an auth profile nor `runAsServiceAccount` is set, tasks fall back to `service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com`.

### Mandatory identity rules (effective October 15, 2026)

- **Every run needs an explicit identity**: For integrations created on or after October 15, 2026 (and for existing integrations at a later date), every run requires either the triggering caller's identity or an attached run-as service account.
- **Triggers other than API or Private require `runAsServiceAccount`**: Integrations created on or after October 15, 2026 with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Eventarc, Salesforce, or Connector Event) **cannot be tested or published unless `runAsServiceAccount` is set**. Private triggers are exempt like API triggers, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount`.
- **Region governance**: If governance is enabled on the region, a run-as service account is required for **all** new integrations and versions, regardless of trigger type.
- **Service Account User (`roles/iam.serviceAccountUser`)**: Whenever `runAsServiceAccount` is set on a version, the user (or principal) publishing or testing the version needs `roles/iam.serviceAccountUser` on that service account (or on the project that owns the service account). At runtime (to invoke, resume a suspension on, or call the integration), the invoking principal—the caller, or for Pub/Sub, Cloud Scheduler, Eventarc, and Connector Event triggers, the trigger's service account—must hold `roles/iam.serviceAccountUser` on `runAsServiceAccount`.
- **Two independent IAM checks**: A 403 `PERMISSION_DENIED` error can come from either the caller lacking an Application Integration IAM role or missing `roles/iam.serviceAccountUser` / resource permissions on the run-as service account. Both checks apply independently, so fixing one does not bypass the other.
- **Least-privilege recommendation**: Create one dedicated, minimally scoped user-managed service account per integration.

## gcloud IAM Commands

### Read-only: check project number and existing bindings

```bash
# Look up PROJECT_NUMBER to identify service agent emails
gcloud projects describe PROJECT_ID --format="value(projectNumber)"

# Inspect project IAM policy
gcloud projects get-iam-policy PROJECT_ID --format=json

# Inspect IAM policy on a run-as service account
gcloud iam service-accounts get-iam-policy SA_EMAIL --project=PROJECT_ID --format=json
```

### State-changing: create a dedicated run-as service account and grant roles

Show these commands and obtain user confirmation before running them:

```bash
# 1. Create a dedicated run-as service account for an integration
gcloud iam service-accounts create SA_NAME \
  --display-name="Run-as SA for INTEGRATION_NAME" \
  --project=PROJECT_ID

# 2. Grant the publisher / developer Service Account User on that service account
gcloud iam service-accounts add-iam-policy-binding \
  SA_NAME@PROJECT_ID.iam.gserviceaccount.com \
  --member="user:USER_EMAIL" \
  --role="roles/iam.serviceAccountUser" \
  --project=PROJECT_ID

# 3. Grant the run-as service account only the downstream roles the workflow needs
#    (for example, Connector Invoker if it calls Integration Connectors)
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_NAME@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/connectors.invoker"
```
