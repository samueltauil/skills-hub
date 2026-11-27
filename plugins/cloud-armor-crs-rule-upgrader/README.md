# cloud-armor-crs-rule-upgrader

Upgrades Google Cloud Armor security policies from OWASP CRS 3.0 and 3.3 to OWASP CRS 4.22. Preserves signature opt-in and opt-out lists, translates evaluatePreconfiguredExpr to native evaluatePreconfiguredWaf dictionary parameters, remaps signature IDs to v042200, drops retired signature IDs, and updates structured preconfiguredWafConfig fine-tuning exclusions. Evaluates operational risk (High Breaking Change, Medium Attention Required, Low Clean Upgrade) including Method Enforcement breaking changes (PUT/PATCH/DELETE blocking) and sensitivity coverage expansions. Supports both in-place rule upgrades and smooth preview mode deployments with priority spacing and a 200-rule quota guardrail. Use when a user or agent needs to audit, upgrade, or transition Cloud Armor WAF rules to CRS 4.22. Don't use for non-WAF Cloud Armor rules (IP rate-limiting, geo-blocking, reCAPTCHA) or AWS/Azure WAF migrations.

This plugin packages the [`cloud-armor-crs-rule-upgrader`](skills/cloud-armor-crs-rule-upgrader/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-armor-crs-rule-upgrader) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-armor-crs-rule-upgrader/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-armor-crs-rule-upgrader@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-armor-crs-rule-upgrader),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-armor-crs-rule-upgrader`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
