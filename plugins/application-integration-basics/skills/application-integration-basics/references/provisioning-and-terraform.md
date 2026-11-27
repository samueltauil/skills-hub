# Provisioning and Terraform

This reference covers per-region provisioning for Application Integration via REST (`clients:provision`), the Cloud console, and Terraform (`hashicorp/google`).

- [Per-Region Provisioning Model](#per-region-provisioning-model): Lines 11-18
- [Enabling Required APIs](#enabling-required-apis): Lines 19-41
- [Provisioning via REST (`clients:provision`)](#provisioning-via-rest-clientsprovision): Lines 42-95
- [Provisioning via Cloud Console](#provisioning-via-cloud-console): Lines 96-104
- [Provisioning via Terraform (`hashicorp/google`)](#provisioning-via-terraform-hashicorpgoogle): Lines 105-158

## Per-Region Provisioning Model

Application Integration is provisioned **one region at a time** within `PROJECT_ID`. Provisioning `us-central1` does not enable `us-east1` or `europe-west1`; you must provision each `LOCATION` where you plan to create integrations.

- **Supported regions**: Regional locations across the Americas, Europe, Asia-Pacific, and the Middle East (for example, `us-central1`, `us-east1`, `europe-west1`, `asia-southeast1`, `me-central1`).
- **Apigee Integration conflict**: If `PROJECT_ID` was already registered through Apigee Integration, provisioning fails.
- **CMEK is permanent**: Enabling Customer-Managed Encryption Keys (CMEK) for a region **cannot be undone**. Always confirm with the user before enabling CMEK.

## Enabling Required APIs

Check enabled APIs first (read-only):

```bash
gcloud services list --enabled --project=PROJECT_ID \
  --filter="config.name:(integrations.googleapis.com OR connectors.googleapis.com OR secretmanager.googleapis.com OR cloudkms.googleapis.com)"
```

After getting user confirmation, enable the required APIs:

```bash
# Standard setup
gcloud services enable \
  integrations.googleapis.com \
  connectors.googleapis.com \
  secretmanager.googleapis.com \
  --project=PROJECT_ID

# Add Cloud KMS only when configuring CMEK
gcloud services enable cloudkms.googleapis.com --project=PROJECT_ID
```

## Provisioning via REST (`clients:provision`)

- **Method and URL**: `POST https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/clients:provision`
- **Success response**: Empty JSON object `{}`. `{}` is also returned when the region is already provisioned; the call does not change an existing region's settings. Change HTTP calls or encryption on an existing region from the console's Regions page (when the region is already `ACTIVE`, `cloudKmsConfig`, `enableHttpCall`, and `enableManagedAiFeatures` on `clients:provision` are not applied).

### `ProvisionClientRequest` body fields

All fields in the request body are optional:

| Field | Type | Description |
| :--- | :--- | :--- |
| `cloudKmsConfig` | object | CMEK settings: `kmsLocation` (required), `kmsRing` (required), `key` (required), `keyVersion` (optional), `kmsProjectId` (optional). Google-managed encryption (GMEK) applies when omitted. |
| `runAsServiceAccount` | string | Not applied by `clients:provision` (the field is accepted but ignored); set `runAsServiceAccount` on each integration version (`IntegrationVersion.runAsServiceAccount`). |
| `createSampleWorkflows` | boolean | When `true`, seeds sample workflows in the region. |
| `enableHttpCall` | boolean | Enables HTTP calls for the region (HTTP is off by default). |
| `enableManagedAiFeatures` | boolean | Enables managed AI features (such as Gemini error troubleshooting) in the region. |
| `skipCpProvision` | boolean | Undocumented field; do not set. |
| `provisionGmek` | boolean | **Deprecated**. Omit this field; GMEK is used automatically when `cloudKmsConfig` is absent. |

### REST example (standard GMEK setup)

Show the exact command and obtain user confirmation before running it. An empty body `{}` provisions the region with defaults (Google-managed encryption and HTTP calls disabled); add `"enableHttpCall": true` or `"enableManagedAiFeatures": true` only if the user explicitly opts in:

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/clients:provision"
```

### REST example (CMEK setup)

Confirm with the user first that CMEK is irreversible for `LOCATION`:

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "cloudKmsConfig": {
      "kmsLocation": "LOCATION",
      "kmsRing": "KMS_RING_NAME",
      "key": "KMS_KEY_NAME",
      "kmsProjectId": "KMS_PROJECT_ID"
    }
  }' \
  "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/clients:provision"
```

### Other `clients` methods in the v1 discovery document

The v1 discovery document also lists `changeConfig`, `deprovision`, `provisionClientPostProcessor`, `replace`, `switch`, `switchVariableMasking`, and `toggleHttp` on `projects.locations.clients`, but only `provision` appears in the public REST reference navigation—do not rely on the unreferenced methods.

## Provisioning via Cloud Console

Open `https://console.cloud.google.com/integrations` and select `LOCATION` (or go to **Regions > Provision new region** for an additional region).

| Setup mode | What it configures |
| :--- | :--- |
| **Quick setup** | Enables `integrations.googleapis.com`, `connectors.googleapis.com`, and `secretmanager.googleapis.com`, creates the default service account, and uses Google-managed encryption. |
| **Advanced setup** | Lets you choose CMEK (and optionally a separate CMEK for Integration Connectors), **Enable HTTP** (off by default), **Enable AI features**, **Enable governance** (makes a run-as service account mandatory on every new integration and version), and **Variable masking in logs** (Preview). |

## Provisioning via Terraform (`hashicorp/google`)

Terraform manages regional setup, authentication profiles, and Integration Connectors resources. **Terraform does not have a resource for integration workflows or versions** (there is no `google_integrations_integration` resource; manage integration JSON via the REST API).

| Resource | Purpose |
| :--- | :--- |
| `google_integrations_client` | Provisions Application Integration in a region (`projects/{{project}}/locations/{{location}}/clients`). |
| `google_integrations_auth_config` | Creates an authentication profile (`authConfigs`). Must set `depends_on` on `google_integrations_client`. |
| `google_integration_connectors_connection` | Creates an Integration Connectors connection (`name`, `location`, `connector_version` required). |
| `google_integration_connectors_endpoint_attachment` | Creates a regional Private Service Connect (PSC) endpoint attachment for a service attachment. |
| `google_integration_connectors_managed_zone` | Creates a global Cloud DNS peering zone for Integration Connectors. |

### Critical Terraform gotcha (`hashicorp/google` v8.0.0+)

The `run_as_service_account` argument was **removed** from `google_integrations_client` in `hashicorp/google` v8.0.0 (August 26, 2026). It mapped to the `clients:provision` `runAsServiceAccount` field and is likewise not applied. Do not include `run_as_service_account` in `google_integrations_client` blocks, even though older examples on the Manage regions documentation page still show it; set the run-as identity on each integration version (`IntegrationVersion.runAsServiceAccount`) instead.

### Terraform example: region provisioning and auth profile

```hcl
variable "external_api_token" {
  type      = string
  sensitive = true
}

resource "google_integrations_client" "regional_client" {
  project                    = "PROJECT_ID"
  location                   = "LOCATION"
  create_sample_integrations = false
  deletion_policy            = "PREVENT"

  # Optional: uncomment only if using CMEK (cannot be undone for the region)
  # cloud_kms_config {
  #   kms_location   = "LOCATION"
  #   kms_ring       = "KMS_RING_NAME"
  #   key            = "KMS_KEY_NAME"
  #   kms_project_id = "KMS_PROJECT_ID"
  # }
}

resource "google_integrations_auth_config" "token_profile" {
  project      = "PROJECT_ID"
  location     = "LOCATION"
  display_name = "example-auth-token"
  depends_on   = [google_integrations_client.regional_client]

  decrypted_credential {
    credential_type = "AUTH_TOKEN"
    auth_token {
      type  = "Bearer"
      token = var.external_api_token
    }
  }
}
```
