# secops-detection-engineering

Author, validate, test, and deploy YARA-L 2.0 detection rules and evaluate end-to-end detection coverage gaps in Google SecOps. Use when writing new detection rules, tuning existing rules, validating syntax, testing logic against historical telemetry, or evaluating detection coverage against threat intelligence blogs, CVE disclosures, and Threat Detection Opportunities (TDOs) using synthetic UDM events and long-running coverage analysis. Don't use for alert triage (use secops-triage), deep forensic event reconstruction on infected hosts (use secops-investigate), or case management operations (use secops-cases).

This plugin packages the [`secops-detection-engineering`](skills/secops-detection-engineering/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/secops-detection-engineering) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/secops-detection-engineering/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install secops-detection-engineering@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecops-detection-engineering),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `secops-detection-engineering`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
