# cloud-logging-finops

Audits Cloud Logging costs for a Google Cloud project: the charges for log entries written to log buckets, the services, log streams and severities that drive them, and the log sinks that route them. Reconciles Cloud Billing export costs with Cloud Monitoring volume metrics, and generates a FinOps report with charts and copy-paste exclusion filters. Use when auditing Cloud Logging spend, finding logging waste, identifying top logging contributors, generating log cost reduction reports, or creating log sink exclusion filters. Don't use for querying log entries (use cloud-logging-query-generation), configuring Cloud Monitoring alerts, or querying metrics/traces.

This plugin packages the [`cloud-logging-finops`](skills/cloud-logging-finops/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-logging-finops) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-logging-finops/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-logging-finops@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-logging-finops),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-logging-finops`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
