# cloud-monitoring-notification-channels-configuration

Generates Terraform HCL configurations for Cloud Monitoring notification channels (`google_monitoring_notification_channel`) and adds notification channels to alerting policies (`google_monitoring_alert_policy`) in Google Cloud projects. Use when creating or configuring email, SMS, Slack, PagerDuty, Pub/Sub, or webhook notification channels, verifying Pub/Sub topic compatibility (including cross-project topics, message storage policies, and in-transit enforcement) and publishing permissions for the Cloud Monitoring Service Agent, or adding notification channels to existing alert policies. Don't use for authoring or editing alerting policy conditions, selecting metric descriptors, or writing PromQL or Monitoring Filter queries.

This plugin packages the [`cloud-monitoring-notification-channels-configuration`](skills/cloud-monitoring-notification-channels-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-monitoring-notification-channels-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-monitoring-notification-channels-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-monitoring-notification-channels-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-monitoring-notification-channels-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-monitoring-notification-channels-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
