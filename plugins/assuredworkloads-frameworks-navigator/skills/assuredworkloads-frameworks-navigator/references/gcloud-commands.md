# Assured Workloads Frameworks Navigator - gcloud Commands Reference

This document provides the exact `gcloud` CLI syntax needed by the navigator skill (or by the user) to resolve context, prepare the environment, or query the Data Boundary catalog. 

> **Important**: Use the exact commands below to avoid trial-and-error (`--help`). The Cloud Security Compliance API requires specific flags that are enumerated here.

---

## 1. Environment & Project Setup

Use these commands to establish the correct execution context before invoking the backend scripts or listing resources.

```bash
# Verify gcloud installation
gcloud --version

# Set the target project context
gcloud config set project PROJECT_ID

# Authenticate the user session
gcloud auth login

# Enable the necessary API for the Cloud Security Compliance engine
gcloud services enable cloudsecuritycompliance.googleapis.com
```

---

## 2. Organization & Folder Resolution (Step 0)

To resolve the Organization ID (`ORGANIZATION_ID`) from a known Google Cloud Project or Folder.

```bash
# Given a Project ID, get its ancestors.
# The organization ID is the row where type="organization".
gcloud projects get-ancestors PROJECT_ID

# Given a Folder ID, describe it to discover its parent organization.
gcloud resource-manager folders describe FOLDER_ID
```

---

## 3. Catalog Fetching (Read-Only)

If the agent needs to manually list frameworks or controls, or recommend the raw commands to the user (the backend script `db_resources_loader.py` wraps these natively):

```bash
# List available Compliance Frameworks
gcloud compliance-manager frameworks list \
  --organization=ORGANIZATION_ID \
  --location=LOCATION \
  --page-size=1000 \
  --format=json

# List available Cloud Controls
gcloud compliance-manager cloud-controls list \
  --organization=ORGANIZATION_ID \
  --location=LOCATION \
  --page-size=1000 \
  --format=json
```

* `ORGANIZATION_ID`: The numeric ID of the Google Cloud organization.
* `LOCATION`: The target region (e.g., `australia-southeast1`) or `global`.
