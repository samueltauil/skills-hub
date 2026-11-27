# Fine-Tuning and CEL Expression Syntax Reference

<!-- disableFinding(LINE_OVER_80) -->

This reference documents Common Expression Language (CEL) syntax, opt-in/opt-out
rules, structured `preconfiguredWafConfig` exclusions, and method enforcement
mitigations when migrating to OWASP CRS 4.22.

## Table of Contents

-   [1. CEL Syntax Evolution](#1-cel-syntax-evolution): Lines 17-61
-   [2. Structured Fine-Tuning (`preconfiguredWafConfig`)](#2-structured-fine-tuning-preconfiguredwafconfig): Lines 64-145
-   [3. Method Enforcement Breaking Change and Remediation](#3-method-enforcement-breaking-change-and-remediation): Lines 148-188

--------------------------------------------------------------------------------

## 1. CEL Syntax Evolution

### Legacy Syntax (CRS 3.0 / 3.3)

In legacy policies, rulesets were evaluated using either
`evaluatePreconfiguredWaf` or `evaluatePreconfiguredExpr`:

```cel
// No exclusions:
evaluatePreconfiguredWaf('sqli-stable')

// Signature opt-outs (DISABLED signatures):
evaluatePreconfiguredExpr('sqli-stable', ['owasp-crs-v030001-id942120-sqli'])
```

> **CRITICAL DOMAIN FACT**: In `evaluatePreconfiguredExpr(ruleset, ['id1',
> 'id2'])`, the array parameter is **strictly an OPT-OUT list**. It means:
> evaluate all signatures in the ruleset *except* `id1` and `id2` (which are
> disabled). It was NEVER an opt-in list.

### Native CRS 4.22 Syntax

CRS 4.22 unifies all preconfigured evaluations under `evaluatePreconfiguredWaf`
using dictionary parameters:

```cel
// Basic evaluation:
evaluatePreconfiguredWaf('sqli-v422-stable')

// Opt-out specific signatures (preserves legacy disabled list):
evaluatePreconfiguredWaf('sqli-v422-stable', {'opt_out_rule_ids': ['owasp-crs-v042200-id942120-sqli']})

// Opt-in specific signatures (evaluates ONLY specified signatures):
evaluatePreconfiguredWaf('sqli-v422-stable', {'opt_in_rule_ids': ['owasp-crs-v042200-id942120-sqli']})

// Custom sensitivity level:
evaluatePreconfiguredWaf('sqli-v422-stable', {'sensitivity': 2})

// Standalone CVE evaluation (preserves original signature IDs):
evaluatePreconfiguredWaf('cve-canary', {'opt_out_rule_ids': ['owasp-crs-v030001-id244228-cve', 'owasp-crs-v030001-id344228-cve']})

// CVE Canary with custom sensitivity:
evaluatePreconfiguredWaf('cve-canary', {'sensitivity': 1})
```

--------------------------------------------------------------------------------

## 2. Structured Fine-Tuning (`preconfiguredWafConfig`)

Cloud Armor rules can configure fine-grained exclusions using the structured
`preconfiguredWafConfig` object on the rule.

> **Note**: In legacy policies, rules using the `evaluatePreconfiguredExpr` CEL
> syntax did NOT support the Google Cloud console's "fine-tune" feature. Rules
> using standard `evaluatePreconfiguredWaf` with `preconfiguredWafConfig` did
> support it. In CRS 4.22, both options are available.

### Exclusion Object Structure

Each exclusion entry in `preconfiguredWafConfig.exclusions[]` contains:

-   `targetRuleSet`: The ruleset being exempted (for example,
    `sqli-v422-stable`).
-   `targetRuleIds` (optional): List of specific signature IDs to exempt. If
    omitted, applies to the entire ruleset.
-   Request attribute exclusions:
    -   `requestHeadersToExclude`: Exclude specific request header names.
    -   `requestCookiesToExclude`: Exclude specific cookie names.
    -   `requestQueryParamsToExclude`: Exclude specific query parameter names.
    -   `requestUrisToExclude`: Exclude specific request URI paths.
    -   `requestBodiesToExclude`: Exclude specific request body fields.

### Field Parameter Structure

Each field exclusion
(`SecurityPolicyRulePreconfiguredWafConfigExclusionFieldParams`) contains:

-   `op`: Match operator (`EQUALS`, `STARTS_WITH`, `ENDS_WITH`, `CONTAINS`,
    `EQUALS_ANY`).
-   `val`: Target parameter, header, cookie, URI, or body field value (for
    example, `User-Agent`, `session_token`, `/api/upload`). Must be omitted when
    `op` is `EQUALS_ANY`.

### Migration Transformation Rules

When upgrading a policy with `preconfiguredWafConfig`:

1.  **Target Ruleset**: Update `targetRuleSet` to the CRS 4.22 equivalent (for
    example, `sqli-stable` to `sqli-v422-stable`, `lfi-v33-stable` to
    `lfi-v422-stable`).
2.  **Signature IDs**: Update `targetRuleIds` from `owasp-crs-v030001-...` or
    `owasp-crs-v030301-...` to `owasp-crs-v042200-...`.
3.  **Deprecated IDs**: Remove all 15 retired CRS 3.0/3.3 signature IDs
    (`981172`, `981173`, `980130`, `949110`; SQLi: `942110`; RCE: `932100`,
    `932105`, `932106`, `932110`, `932115`, `932150`; Scanner Detection:
    `913101`, `913102`, `913110`, `913120`) from `targetRuleIds`. If an
    exclusion's `targetRuleIds` list becomes empty (`[]`) after removing retired
    IDs, the entire exclusion entry must be removed rather than left with
    `targetRuleIds: []` (which would exempt the entire ruleset).
4.  **Field Conditions**: Preserve all header, cookie, query parameter, URI, and
    body exclusions without modification.

### Example: Upgraded `preconfiguredWafConfig`

```json
"preconfiguredWafConfig": {
  "exclusions": [
    {
      "targetRuleSet": "lfi-v422-stable",
      "targetRuleIds": [
        "owasp-crs-v042200-id930100-lfi"
      ],
      "requestHeadersToExclude": [
        {
          "op": "EQUALS",
          "val": "X-Custom-Token"
        }
      ],
      "requestUrisToExclude": [
        {
          "op": "STARTS_WITH",
          "val": "/api/v2/reports"
        }
      ]
    }
  ]
}
```

--------------------------------------------------------------------------------

## 3. Method Enforcement Breaking Change and Remediation

### The Risk

In CRS 4.22, `methodenforcement-v422-stable` only permits HTTP methods:

-   `GET`
-   `HEAD`
-   `POST`
-   `OPTIONS`

Any HTTP request using **`PUT`**, **`PATCH`**, or **`DELETE`** (common in
RESTful APIs and modern web applications) will be matched and blocked by Cloud
Armor with HTTP 403 Forbidden!

### Remediation Strategies

#### Strategy A: Opt out of Method Enforcement Signature (Recommended for Full REST APIs)

Opt out of signature `id911100` within the CEL expression:

```cel
evaluatePreconfiguredWaf('methodenforcement-v422-stable', {'opt_out_rule_ids': ['owasp-crs-v042200-id911100-methodenforcement']})
```

#### Strategy B: Scope Method Enforcement to Non-API Traffic

Use CEL boolean logic to only evaluate Method Enforcement on paths that do not
handle REST API mutations:

```cel
evaluatePreconfiguredWaf('methodenforcement-v422-stable') && !request.path.startsWith('/api/')
```

#### Strategy C: Allow Specific HTTP Methods via CEL

Only enforce on disallowed methods:

```cel
evaluatePreconfiguredWaf('methodenforcement-v422-stable') && !(request.method in ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'])
```
