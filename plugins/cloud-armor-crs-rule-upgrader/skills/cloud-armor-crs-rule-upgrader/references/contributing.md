# Contributing and Invariants Guide: Cloud Armor OWASP Upgrade Skill

<!-- disableFinding(LINE_OVER_80) -->

This document defines the invariants, safety rules, and validation requirements
for maintaining and extending this skill.

--------------------------------------------------------------------------------

## 1. Domain Invariants

1.  **Opt-Out Parameter Semantic**:

    -   In legacy `evaluatePreconfiguredExpr(ruleset, [ids])`, the array is
        **strictly an opt-out list (disabled signatures)**.
    -   In CRS 4.22 `evaluatePreconfiguredWaf(ruleset, {'opt_out_rule_ids':
        [ids]})`, disabled signatures must remain disabled.
    -   An opt-out list must **never** be inverted or converted into an opt-in
        list during automatic migration.

2.  **Retired / Deprecated Signature Numbers**:

    -   All 15 retired CRS 3.0 / 3.3 signature numbers (`981172`, `981173`,
        `980130`, `949110`; SQLi: `942110`; RCE: `932100`, `932105`, `932106`,
        `932110`, `932115`, `932150`; Scanner Detection: `913101`, `913102`,
        `913110`, `913120`) do not exist in CRS 4.22.
    -   They must be filtered out of all upgraded opt-out lists and
        `preconfiguredWafConfig` `targetRuleIds`.
    -   Under no circumstances should non-existent signature IDs be retained in
        generated 4.22 rules.

3.  **Method Enforcement Safety (High Risk / Breaking Change)**:

    -   `methodenforcement-v422-stable` blocks HTTP `PUT`, `PATCH`, and
        `DELETE`.
    -   The agent must always warn the customer before enforcing method
        enforcement on policies protecting REST APIs.

4.  **Quota Limit (200 Rules)**:

    -   Google Cloud Armor enforces a hard limit of 200 rules per security
        policy.
    -   In Preview Mode, if the sum of original rules and generated preview
        rules exceeds 200, the upgrade must be halted and the user informed.

5.  **Fine-Tuning Preservation**:

    -   All `preconfiguredWafConfig.exclusions` field parameters
        (`requestHeadersToExclude`, `requestCookiesToExclude`,
        `requestQueryParamsToExclude`, `requestUrisToExclude`,
        `requestBodiesToExclude`) and match operators (`op`, `val`) must be
        carried over intact.
    -   If an exclusion entry's `targetRuleIds` list was originally non-empty
        and becomes empty (`[]`) after removing retired signature IDs, the
        entire exclusion entry must be dropped rather than left with
        `targetRuleIds: []`.

6.  **Preview Priority Ordering and Cutover Safety**:

    -   When generating preview rules, the preview priority for a rule at `prio`
        must be allocated strictly within `(previous_priority, prio)`, where
        `previous_priority` is the priority of the immediately preceding rule in
        the policy.
    -   A preview rule must **never** be placed at a priority `<=`
        `previous_priority`, as doing so would reorder evaluation ahead of
        intervening `allow` or custom rules and generate false-positive preview
        telemetry.
    -   If no free integer priority slot exists in `(previous_priority, prio)`,
        the script must raise a `ValueError` instructing the user to readjust
        adjacent rule priorities to leave at least one open priority slot or
        perform an in-place upgrade. The agent must never silently re-number
        existing customer rules without explicit confirmation and an IaC drift
        warning.
    -   Cutover from Preview Mode to full enforcement must update the original
        enforced rule priority in-place and delete the temporary preview rule,
        preserving original rule priorities and ordering.

--------------------------------------------------------------------------------

## 2. Code Invariants (scripts/upgrade_policy.py)

1.  **Dependencies and Runtime**:

    -   `scripts/upgrade_policy.py` uses only the Python standard library
        (`argparse`, `ast`, `copy`, `json`, `os`, `re`, `sys`, `typing`) so it
        can execute identically inside Cloud Shell, CI/CD, or standalone
        customer environments without third-party package installations.

2.  **Automated Testing**:

    -   Every modification to transformation logic or signature catalogs must be
        accompanied by unit tests in `_internal/upgrade_policy_test.py`.
    -   Run tests before committing:

        ```bash
        python3 -m unittest discover -s _internal -p "*_test.py"
        ```
