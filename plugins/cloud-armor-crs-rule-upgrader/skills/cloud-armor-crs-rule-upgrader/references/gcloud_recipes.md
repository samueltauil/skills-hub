# Google Cloud Armor gcloud CLI Recipes Reference

<!-- disableFinding(LINE_OVER_80) -->

This document provides exact, copy-pasteable `gcloud` CLI workflows for
auditing, upgrading, and monitoring Google Cloud Armor security policies during
an OWASP CRS 4.22 migration.

## Table of Contents

-   [1. Policy Audit and Inspection](#1-policy-audit-and-inspection): Lines 19-40
-   [2. In-Place Upgrade Recipes](#2-in-place-upgrade-recipes): Lines 43-90
-   [3. Preview Mode Recipes](#3-preview-mode-recipes): Lines 93-173
-   [4. Monitoring and Telemetry in Cloud Logging](#4-monitoring-and-telemetry-in-cloud-logging): Lines 176-205
-   [5. Cutover: Transitioning from Preview Mode to Full Enforcement](#5-cutover-transitioning-from-preview-mode-to-full-enforcement): Lines 208-255

--------------------------------------------------------------------------------

## 1. Policy Audit and Inspection

### Describe an Existing Policy

Retrieve full JSON configuration of the policy:

```bash
gcloud compute security-policies describe POLICY_NAME \
  --project=PROJECT_ID \
  --format="json" > /tmp/POLICY_NAME_original.json
```

### List All Policies in Project

Quickly identify security policies:

```bash
gcloud compute security-policies list \
  --project=PROJECT_ID \
  --format="table(name, description, type)"
```

--------------------------------------------------------------------------------

## 2. In-Place Upgrade Recipes

In-place upgrades replace the rule expression and WAF configuration directly on
existing priorities.

### Option A: Updating Individual Rules via CLI

For rules without structured `preconfiguredWafConfig`:

```bash
gcloud compute security-policies rules update PRIORITY \
  --security-policy="POLICY_NAME" \
  --project=PROJECT_ID \
  --expression="UPGRADED_EXPRESSION"
```

**Example (SQLi with opt-out)**:

```bash
gcloud compute security-policies rules update 1000 \
  --security-policy="my-prod-waf" \
  --expression="evaluatePreconfiguredWaf('sqli-v422-stable', {'opt_out_rule_ids': ['owasp-crs-v042200-id942120-sqli']})"
```

### Option B: Atomic Policy Import (Recommended for Complex Policies)

When rules include `preconfiguredWafConfig` fine-tuning or multiple rules, use
atomic export/import:

```bash
# 1. Export current policy
gcloud compute security-policies export POLICY_NAME \
  --project=PROJECT_ID \
  --file-name=/tmp/POLICY_NAME.json \
  --file-format=json

# 2. Upgrade using helper script
python3 scripts/upgrade_policy.py /tmp/POLICY_NAME.json \
  --mode=in-place \
  --format=json > /tmp/POLICY_NAME_upgraded.json

# 3. Import upgraded policy atomically
gcloud compute security-policies import POLICY_NAME \
  --project=PROJECT_ID \
  --file-name=/tmp/POLICY_NAME_upgraded.json \
  --file-format=json
```

--------------------------------------------------------------------------------

## 3. Preview Mode Recipes

Preview mode leaves existing rules actively enforcing while creating 4.22
preview rules evaluated *before* the enforced rules (`preview = true`).

### Creating a Preview Rule

Place the preview rule at a lower numeric priority (for example, `PRIORITY - 5`
or `PRIORITY - 1`), ensuring the priority sits strictly **between the
immediately preceding rule and `ENFORCED_PRIORITY`** so that it never crosses an
intervening `allow` or `deny` rule:

> **Note**: Using `rules create --expression` alone is only for rules without
> `preconfiguredWafConfig` field exclusions. For rules with
> `preconfiguredWafConfig` exclusions, use the JSON export/import workflow below
> or `add-preconfig-waf-exclusion` / `remove-preconfig-waf-exclusion`.

```bash
gcloud compute security-policies rules create PREVIEW_PRIORITY \
  --security-policy="POLICY_NAME" \
  --project=PROJECT_ID \
  --expression="UPGRADED_EXPRESSION" \
  --action="ACTION" \
  --preview \
  --description="PREVIEW: Upgraded CRS 4.22 Rule for Priority ENFORCED_PRIORITY"
```

**Example (RCE in Preview Mode)**:

```bash
# Original enforcing rule sits at priority 1200
# Preview rule placed at priority 1195
gcloud compute security-policies rules create 1195 \
  --security-policy="my-prod-waf" \
  --expression="evaluatePreconfiguredWaf('rce-v422-stable')" \
  --action="deny(403)" \
  --preview \
  --description="PREVIEW: Upgraded CRS 4.22 RCE Rule for Priority 1200"
```

### Batch Preview Mode Deployment

Depending on whether you are adding preview rules to an existing policy or
creating a completely separate standalone preview policy:

#### Option A: Adding Preview Rules to Existing Policy (via Import)

```bash
# 1. Export current policy
gcloud compute security-policies export POLICY_NAME \
  --project=PROJECT_ID \
  --file-name=/tmp/POLICY_NAME.json \
  --file-format=json

# 2. Generate Preview Configuration
python3 scripts/upgrade_policy.py /tmp/POLICY_NAME.json \
  --mode=preview \
  --format=json > /tmp/POLICY_NAME_preview.json

# 3. Import (updates existing policy atomically)
gcloud compute security-policies import POLICY_NAME \
  --project=PROJECT_ID \
  --file-name=/tmp/POLICY_NAME_preview.json \
  --file-format=json
```

#### Option B: Creating a Separate Standalone Preview Policy (via Create)

```bash
# 1. Generate upgraded policy JSON
python3 scripts/upgrade_policy.py /tmp/POLICY_NAME.json \
  --mode=preview \
  --format=json > /tmp/NEW_POLICY_NAME.json

# 2. Create the new security policy from the file
gcloud compute security-policies create NEW_POLICY_NAME \
  --project=PROJECT_ID \
  --file-name=/tmp/NEW_POLICY_NAME.json \
  --file-format=json
```

--------------------------------------------------------------------------------

## 4. Monitoring and Telemetry in Cloud Logging

After deploying rules in Preview Mode, monitor Cloud Logging before full
enforcement to ensure no false positives occur.

### Filter for Preview Rule Matches

Query logs where preview rules triggered:

```bash
gcloud logging read '
  resource.type="http_load_balancer" AND
  jsonPayload.enforcedSecurityPolicy.name="POLICY_NAME" AND
  jsonPayload.previewSecurityPolicy.matchedRulePriority:*
' --project=PROJECT_ID --limit=20 --format="table(timestamp, httpRequest.requestUrl, jsonPayload.previewSecurityPolicy.matchedRulePriority, jsonPayload.previewSecurityPolicy.action)"
```

### Check for Preview False Positives

Query requests that were allowed by live rules but would be blocked by 4.22
preview rules:

```bash
gcloud logging read '
  resource.type="http_load_balancer" AND
  jsonPayload.enforcedSecurityPolicy.outcome="ACCEPT" AND
  jsonPayload.previewSecurityPolicy.action="DENY"
' --project=PROJECT_ID --limit=25
```

--------------------------------------------------------------------------------

## 5. Cutover: Transitioning from Preview Mode to Full Enforcement

Once testing confirms no false positives, cut over to CRS 4.22 by **updating the
original rule priorities in-place** and **deleting the temporary preview
rules**. This preserves your exact original priority numbers, evaluation order,
Infrastructure-as-Code (Terraform) state, and SIEM monitoring filters.

### Option A: Per-Rule CLI Cutover (Recommended for Simple Rules)

> **Note**: Using `rules update --expression` alone is only for rules without
> `preconfiguredWafConfig` field exclusions. For rules with
> `preconfiguredWafConfig` exclusions, use Option B (JSON export/import
> workflow) or `add-preconfig-waf-exclusion` / `remove-preconfig-waf-exclusion`.

1.  **Update the original enforced rule in-place to CRS 4.22**:

```bash
gcloud compute security-policies rules update LEGACY_PRIORITY \
  --security-policy="POLICY_NAME" \
  --project=PROJECT_ID \
  --expression="UPGRADED_EXPRESSION"
```

2.  **Delete the temporary preview rule**:

```bash
gcloud compute security-policies rules delete PREVIEW_PRIORITY \
  --security-policy="POLICY_NAME" \
  --project=PROJECT_ID \
  --quiet
```

### Option B: Atomic Batch Cutover via Import (Recommended for Structured Exclusions)

Run `upgrade_policy.py` in `--mode=in-place` against your original pre-preview
policy backup and import it atomically (which upgrades all original priorities
to CRS 4.22 and removes the temporary preview rules in one step):

```bash
python3 scripts/upgrade_policy.py /tmp/POLICY_NAME.json \
  --mode=in-place \
  --format=json > /tmp/POLICY_NAME_enforced_v422.json

gcloud compute security-policies import POLICY_NAME \
  --project=PROJECT_ID \
  --file-name=/tmp/POLICY_NAME_enforced_v422.json \
  --file-format=json
```
