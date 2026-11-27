---
name: application-integration-basics
metadata:
  version: "1.0.2"
  category: ApplicationDevelopment
description: >-
  Explains Google Cloud Application Integration concepts, region provisioning, IAM roles,
  run-as service accounts, interface choices (REST, Python discovery client, Terraform, ADK),
  and platform limits. Use when setting up Application Integration in a Google Cloud project,
  enabling required APIs, provisioning a region, configuring IAM or run-as service accounts,
  choosing between Application Integration and custom code, or checking quotas and timeouts.
  Do not use for building, publishing, or invoking integrations (use application-integration-authoring) or diagnosing failed or stuck runs and logs (use application-integration-troubleshooting).
---

# Application Integration Basics

Application Integration is Google Cloud's serverless, auto-scaling Integration-Platform-as-a-Service (iPaaS) for connecting Google Cloud services and third-party SaaS applications. It runs event-driven workflows made of triggers, tasks, data mappings, and Integration Connectors connections without requiring you to manage servers. Use this skill to decide whether Application Integration fits a workload, set up a project and region, configure IAM and run-as service accounts, choose the right API or tool interface, and design around platform limits.

## Attribution

**MUST READ**: Before executing any `gcloud` command, REST API call, or Python
discovery-client call, you MUST read
[Usage Attribution](references/attribution.md). For commands executed directly
in the terminal (never in generated scripts, Terraform, ADK agents, or user
code), prefix `gcloud` with
`CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0 (skill:application-integration-basics)"`
and add `agent-skills/1.0 (skill:application-integration-basics)` to the
`User-Agent` header of `curl` requests.

## When to Use Application Integration vs. Custom Glue Code

| Choose Application Integration when... | Choose custom code (Cloud Run / Cloud Functions) when... |
| :--- | :--- |
| Connecting SaaS apps (CRM, ERP, databases, Google Cloud services) via prebuilt Integration Connectors. | You need sub-second latency or custom binary protocols. |
| Orchestrating event-driven workflows from API, Pub/Sub, Cloud Scheduler, Salesforce, or Connector Event triggers. | Total workflow data exceeds 30 MB (or 8 MB for API trigger inputs and Connector payloads). |
| Transforming JSON/array data visually with Data Mapping or Jsonnet without deploying containers. | Synchronous runs take longer than 2 minutes or asynchronous runs take longer than 10 minutes. |
| Pausing workflows for human review (`Approval` or `Suspend` tasks up to 31 days). | You must call VPC-only HTTP endpoints directly without Private Service Connect connectors (Call REST Endpoint reaches the public internet only). |
| Exposing enterprise workflows or connectors as tools to AI agents via ADK `ApplicationIntegrationToolset`. | You need arbitrary language packages or heavy in-memory compute beyond JavaScript (V8) or Jsonnet tasks. |

## Safety and Confirmation Rules

- **Read-only checks run freely**: You may run `gcloud services list`, `gcloud projects get-iam-policy`, and HTTP `GET` calls to `https://integrations.googleapis.com/v1/...` or `https://connectors.googleapis.com/v1/...` without asking first.
- **Require explicit user confirmation before any state change**: Always show the exact command or request payload and wait for user approval before:
  - Enabling APIs (`gcloud services enable`).
  - Provisioning a region (`clients:provision` or `terraform apply` on `google_integrations_client`), especially with Customer-Managed Encryption Keys (CMEK), because **enabling CMEK for a region cannot be undone**.
  - Modifying IAM policies (`gcloud projects add-iam-policy-binding` or `gcloud iam service-accounts add-iam-policy-binding`).
  - Creating, uploading, publishing, unpublishing, executing, testing, or deleting any integration, version, auth profile, or connection.
- **Never bundle destructive scripts** that delete integrations, versions, auth profiles, or connections unattended.
- **Host changes require approval.** Before installing packages (`pip install`) or changing global gcloud or credential state (`gcloud config set ...` such as `auth/impersonate_service_account`, `gcloud auth application-default login` / `set-quota-project`), show the exact command and wait for the user's approval.

## Choosing the Interface

Application Integration has **no `gcloud integrations` command group** (and no `gcloud connectors` command group), and **no Google-managed remote MCP server**. The REST API is the primary control and execution interface.

| Interface | What it covers | Authentication |
| :--- | :--- | :--- |
| **REST API (`curl`)** | Full v1 surface: region provisioning, integrations, versions, download/upload, publish, execute, schedule, executions, suspensions, authConfigs, templates. | `Authorization: Bearer $(gcloud auth print-access-token)` |
| **Python discovery client** | Full v1 surface via `googleapiclient.discovery.build("integrations", "v1")` (and v2 via `build("integrations", "v2")`; no dedicated Cloud Client Library exists). Install with `pip install "google-api-python-client>=2.100.0,<3" "google-auth>=2.20.0,<3"` (changes host or credential state; get the user's approval first). | Application Default Credentials (`gcloud auth application-default login`) (changes host or credential state; get the user's approval first) |
| **Terraform (`hashicorp/google`)** | Infrastructure only: `google_integrations_client` (region setup), `google_integrations_auth_config`, and `google_integration_connectors_*`. Does **not** manage integration workflow versions. | ADC or Terraform provider credentials |
| **ADK (`ApplicationIntegrationToolset`)** | Exposes published API-trigger integrations or Integration Connectors actions/entities as tools for ADK agents (Python v0.1.0+, Java v0.3.0+). | ADC (`gcloud auth application-default login`) (changes host or credential state; get the user's approval first) or service account JSON |
| **Cloud console** | Visual drag-and-drop editor, Quick/Advanced region setup, Approval task resolution, OAuth 2.0 authorization code consent flow. | Browser Google Cloud sign-in |

- Use `gcloud` only for generic Google Cloud tasks: enabling APIs (`gcloud services enable`), printing access tokens (`gcloud auth print-access-token`), managing IAM, and reading Cloud Logging (`gcloud logging read`).
- Integration Connectors includes an outbound **MCP connector** (`MCP v1` and `v2`) that lets a workflow call an external MCP server as a connector target; this is an outbound connector, not a Google-managed MCP server for controlling Application Integration.
- Always use the global endpoint `https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/...` consistently for REST calls.
- **Note on draft testing (`integrations:test`)**: Although `POST .../integrations/INTEGRATION_NAME:test` exists in the v1 REST API, its required `TestIntegrationsRequest.clientId` value is not publicly documented, so do not invent one; test integrations by publishing to a non-production project and calling `:execute`.
- See [references/api-access.md](references/api-access.md) for authentication setup, `curl` commands, Python discovery client patterns, and ADK `ApplicationIntegrationToolset` configuration.

## Step-by-Step Region Setup Workflow

Application Integration is regional: confirm the target region is supported on [Application Integration locations](https://docs.cloud.google.com/application-integration/docs/locations.md.txt) and use `us-central1` as a well-supported default when the user has no preference. The region is the `LOCATION` in every REST path; no `gcloud` default-region setting applies to Application Integration. Provisioning is **per region**. Provisioning `us-central1` does not provision `europe-west1`; repeat region provisioning for every `LOCATION` you use in `PROJECT_ID`. Ensure an active billing account is attached to `PROJECT_ID` before setup—an active billing account is required even when usage stays within the monthly free tier (see the [Application Integration pricing page](https://cloud.google.com/application-integration/pricing)).

### 1. Check and enable required APIs

First check which APIs are already enabled (read-only):

```bash
gcloud services list --enabled --project=PROJECT_ID \
  --filter="config.name:(integrations.googleapis.com OR connectors.googleapis.com OR secretmanager.googleapis.com OR cloudkms.googleapis.com)"
```

After getting user confirmation, enable the required APIs (add `cloudkms.googleapis.com` only if configuring CMEK):

```bash
gcloud services enable \
  integrations.googleapis.com \
  connectors.googleapis.com \
  secretmanager.googleapis.com \
  --project=PROJECT_ID
```

### 2. Verify setup IAM roles on the caller

Setting up Application Integration requires `roles/integrations.integrationAdmin`, `roles/connectors.admin`, and `roles/editor` (plus `roles/cloudkms.admin` for CMEK). Check current bindings (read-only):

```bash
gcloud projects get-iam-policy PROJECT_ID --format=json
```

### 3. Provision the region (`LOCATION`)

Choose one of the three supported paths after getting user confirmation:

- **Option A: REST (`clients:provision`)**
  ```bash
  curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{}' \
    "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/clients:provision"
  ```
  The response is `{}` when provisioning succeeds (`clients:provision` does not apply `runAsServiceAccount`; set the run-as identity on each integration version via `IntegrationVersion.runAsServiceAccount`). `{}` is also returned when the region is already provisioned; the call does not change an existing region's settings. Change HTTP calls or encryption on an existing region from the console's Regions page (when the region is already `ACTIVE`, `cloudKmsConfig`, `enableHttpCall`, and `enableManagedAiFeatures` on `clients:provision` are not applied). If `PROJECT_ID` was already registered through Apigee Integration, provisioning fails.

- **Option B: Cloud console**
  Open `https://console.cloud.google.com/integrations`, select `LOCATION`, and click **Quick setup** (enables the APIs, creates the default service account, and uses Google-managed encryption) or **Advanced setup** (to configure CMEK, HTTP calls, AI features, governance, or variable masking). To add another region later, go to **Regions > Provision new region**.

- **Option C: Terraform (`google_integrations_client`)**
  Use the `google_integrations_client` resource in `hashicorp/google`. Do **not** set `run_as_service_account` on `google_integrations_client`—that argument was removed in provider v8.0.0 (August 26, 2026), and it mapped to the `clients:provision` `runAsServiceAccount` field, which is likewise not applied; set the run-as identity on each integration version (`IntegrationVersion.runAsServiceAccount`) instead.

### 4. Sanity-check region access

Run a read-only list call against the region; a successful `200 OK` response is a good sign that the API is reachable in `LOCATION`:

```bash
curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations"
```

See [references/provisioning-and-terraform.md](references/provisioning-and-terraform.md) for all `ProvisionClientRequest` fields, CMEK and governance options, and complete Terraform examples.

## Core Concepts at a Glance

- **Integrations and Triggers**: An integration is a workflow started by one or more triggers. Synchronous runs (`SYNC`) wait for completion and return output (`integrations.execute`, console test, sync `Call Integration`). Asynchronous runs (`ASYNC`) are fire-and-forget (`integrations.schedule`, Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce triggers, and runs resumed after a suspension or approval).
- **Tasks**: Units of work chained after a trigger (such as `Data Mapping`, `Call REST Endpoint`, `Connectors`, `JavaScript` on V8, `Cloud Function`, `Approval`, `Suspend`, `Timer`, loops, and `Call Integration`).
- **Versions and Edit Locks**: Only a `DRAFT` version can be edited (locked to its author for 15 minutes after the last update). Only an `ACTIVE` (published) version runs from triggers. Publishing a version automatically unpublishes the prior active version and cancels any suspended executions of that prior version. Unpublishing moves an active version to `SNAPSHOT` (`PREVIOUSLY_PUBLISHED`). Calling `versions.delete` soft-deletes a version into `ARCHIVED` (listed as `DELETED` on the Integration versions documentation page).
- **Variables**:
  - **Integration variables**: Explicit inputs (`IN`), outputs (`OUT`), `IN_OUT`, or internal variables with `IN_OUT_TYPE_UNSPECIFIED` (`$varName$`).
  - **Task variables**: Auto-generated task outputs named `` `Task_<taskId>_<variableName>` `` where `taskId` is the bare task number in `taskConfigs[].taskId` (for example, `taskId` `"1"` -> `` $`Task_1_responseBody`$ ``).
  - **System variables**: keys are backtick-wrapped (`` `ExecutionId` ``, `` `ExecutionMode` ``, `` `ErrorInfo` `` [`message`, `code`], `` `IntegrationName` ``, `` `Region` ``, `` `ProjectId` ``); reference them as `` $`ExecutionId`$ `` (a bare `$ExecutionId$` names a nonexistent integration variable and fails).
  - **Config variables** (Preview): Environment-specific values defined in `integrationConfigParameters` (with defaults in `parameter.defaultValue`; a top-level `value` on a draft is discarded) and supplied per environment in `configParameters` at publish time (named `` `CONFIG_<NAME>` ``; keys in `configParameters` must **exactly match** a key in `integrationConfigParameters`, backticks included, such as `` "`CONFIG_target_url`" ``, because unknown keys are silently ignored—publish returns 200 and the default stays). **Never store secrets in config variables**—they are exported in plain text. Use an authentication profile (`authConfigs`) or the Secret Manager task instead.
- **Suspensions**: `Suspend` tasks pause up to 31 days and are resumed via the Suspensions API (`suspensions:lift`, with an optional `suspensionResult`, requiring `integrations.suspensions.lift`). `Approval` tasks email approvers and can be approved or rejected in the Cloud console UI or via `suspensions:resolve` (`state`: `"LIFTED"` or `"REJECTED"`, requiring `integrations.suspensions.resolve`). Listing suspensions (`suspensions.list`) requires `integrations.suspensions.list`. All three permissions are included in `roles/integrations.suspensionResolver` (and `roles/integrations.integrationAdmin`), and resuming also requires `roles/iam.serviceAccountUser` on the integration's run-as service account; always confirm with the user before lifting or resolving. `Timer` tasks resume automatically.
- **Authentication Profiles (`authConfigs`)**: Reusable regional credential records (`projects/PROJECT_ID/locations/LOCATION/authConfigs/AUTH_CONFIG_ID`). They are not included when downloading an integration version.

See [references/core-concepts.md](references/core-concepts.md) for full details on version states, trigger types, task categories, variables, suspensions, and authentication profiles.

## IAM and the Run-As Service Account Requirement

### Key IAM roles and service agents

- **Developer & operator roles**: `roles/integrations.integrationAdmin` (full CRUD + delete auth profiles), `roles/integrations.integrationEditor` (create/upload/edit/test/invoke/cancel/replay/publish, including `integrations.integrationVersions.create` and `integrations.integrationVersions.deploy`), `roles/integrations.integrationDeployer` (publish/unpublish via `integrations.integrationVersions.deploy`; holds `list`/`get`/`deploy` but not `create`, so it can publish an existing version but cannot upload), `roles/integrations.integrationInvoker` (invoke/cancel/replay), `roles/integrations.integrationViewer` (view integrations and logs), and `roles/integrations.suspensionResolver` (list, lift, and resolve suspensions: `integrations.suspensions.list`, `integrations.suspensions.lift`, `integrations.suspensions.resolve`; `suspensionResolver` alone cannot read execution records, so also grant `roles/integrations.integrationViewer` to inspect `taskExecutionDetails` or run `:troubleshoot`, or use the approval email link, which carries the execution and task IDs).
- **Service agents**:
  - **Application Integration service agent**: `service-PROJECT_NUMBER@gcp-sa-integrations.iam.gserviceaccount.com` (granted `roles/integrations.serviceAgent`).
  - **Integration Connectors service agent**: `service-PROJECT_NUMBER@gcp-sa-connectors.iam.gserviceaccount.com` (granted `roles/connectors.serviceAgent`).

### Mandatory run-as service account rules (effective October 15, 2026)

1. **Explicit identity required**: For integrations created on or after October 15, 2026 (and for existing integrations at a later date), every run needs an explicit identity—either the triggering caller or a user-managed run-as service account set per integration version via `IntegrationVersion.runAsServiceAccount` (region provisioning via `clients:provision` does not apply `runAsServiceAccount`).
2. **Triggers other than API or Private require a run-as service account**: Integrations created on or after October 15, 2026 with any trigger other than an API or Private trigger (for example Schedule, Cloud Scheduler, Cloud Pub/Sub, Eventarc, Salesforce, or Connector Event) **cannot be tested or published unless `runAsServiceAccount` is set**. Private triggers are exempt like API triggers, so a sub-integration whose only trigger is Private can be published without `runAsServiceAccount`.
3. **Region governance**: If governance is enabled on the region, a run-as service account is mandatory for **every** new integration and version, including API-trigger integrations.
4. **Service Account User (`roles/iam.serviceAccountUser`)**: Whenever `runAsServiceAccount` is set on a version, the user (or principal) publishing or testing the version must hold `roles/iam.serviceAccountUser` on that service account (or its owning project). At runtime, the invoking caller or trigger service account—and anyone resolving or lifting a suspension—must also hold `roles/iam.serviceAccountUser` on it.
5. **Best practice**: Create one dedicated, minimally scoped user-managed service account per integration. When `runAsServiceAccount` is set and no task-level auth profile is set, it mints tokens for Connector, Call REST Endpoint, and Cloud Function tasks (an OAuth 2.0 or OIDC auth profile on a task takes precedence over `runAsServiceAccount`).

See [references/iam-and-service-accounts.md](references/iam-and-service-accounts.md) for the complete IAM role tables, service agent permissions, credential precedence rules, and `gcloud` IAM commands.

## Key Quotas and Limits to Design Around

| Limit | Value | Design impact |
| :--- | :--- | :--- |
| **SYNC execution timeout** | 2 minutes | Use async triggers or `integrations.schedule` for workflows exceeding 2 minutes; timed-out sync runs become `CANCELLED`. |
| **ASYNC execution timeout** | 10 minutes | Split heavy work into sub-integrations or external jobs if a single async run exceeds 10 minutes. |
| **Max execution lifetime** | 31 days | Includes time paused in `Approval` or `Suspend` tasks (max 44,640 minutes). |
| **Total integration data** | 30 MB | Shared across input/output variables and private-trigger sub-integrations. **Above 10 MB, local logging is disabled**, retries stop working, and monitoring skips the run. |
| **API trigger input size** | 8 MB | Cumulative size across all input variables; larger payloads fail before the workflow starts. |
| **Connectors data & timeout** | 8 MB in/out; 3 min timeout | Application Integration quotas cap cumulative data sent to/from connections at 8 MB and connector response at 20 MB (Integration Connectors quotas cap the Connectors task payload at 10 MB); custom queries cap at 180 seconds and 50,000 rows. |
| **Concurrent executions** | 50 per project per region; 10 per integration (defaults) | Both concurrency caps are adjustable; a burst on a single integration hits the 10-per-integration cap, not 50. The execution request rate quota is shown on the project's Cloud Quotas page and can be adjusted there. |
| **Integrations / tasks / versions** | 1,000 / 100 / 100 | Up to 1,000 integrations per project, 100 tasks per integration, and 100 versions per integration. |
| **Publish propagation** | Up to 10 minutes | Eventual consistency: an older version can keep running for up to 10 minutes after publishing a new version. |

See [references/limits.md](references/limits.md) for all task-specific payload caps, loop iteration limits, Integration Connectors node limits, and pricing details.

## Sibling Skills

- **application-integration-basics** (this skill): Concepts, API enablement, region provisioning, IAM roles and run-as service accounts, interface choices (REST, Python client, Terraform, ADK), and quotas/limits.
- **application-integration-authoring**: Building, uploading, versioning, config variables, publishing, executing, and testing integrations via the REST API; trigger IDs; task gotchas; and CI/CD promotion across projects with download/upload.
- **application-integration-troubleshooting**: Diagnosing failed or stuck executions, checking execution and task states and `ErrorInfo`, listing and filtering executions, Cloud Logging and Cloud Monitoring, suspensions and approvals, Integration Connectors connection health, and IAM / run-as / quota errors.

## Reference Files

- [references/attribution.md](references/attribution.md): Usage attribution for `gcloud` CLI commands, direct `curl` REST calls, and Python discovery-client snippets run in the terminal.
- [references/core-concepts.md](references/core-concepts.md): Triggers, execution modes, task types, version lifecycle, edit locks, variables, suspensions, and authentication profiles.
- [references/iam-and-service-accounts.md](references/iam-and-service-accounts.md): Predefined IAM roles for Application Integration and Integration Connectors, service agents, run-as service account rules, and IAM commands.
- [references/provisioning-and-terraform.md](references/provisioning-and-terraform.md): Per-region provisioning via REST `clients:provision`, Cloud console Quick/Advanced setup, CMEK caveats, and Terraform `google_integrations_*` / `google_integration_connectors_*` resources.
- [references/api-access.md](references/api-access.md): Endpoints, authentication, `curl` examples, Python `google-api-python-client` discovery patterns, ADK `ApplicationIntegrationToolset`, and MCP connector clarification.
- [references/limits.md](references/limits.md): Timeouts, payload caps, concurrency quotas, loop/task limits, Integration Connectors limits, and pricing tiers.
