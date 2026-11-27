# oncall-irm

Route alerts, run on-call rotations, and drive incidents in Grafana IRM / OnCall — integrations (Alertmanager / Grafana Alerting / generic webhook / PagerDuty), Jinja2 routing + grouping templates, escalation chains (wait → notify schedule → notify team → webhook → auto-resolve), schedules (web + iCal + Terraform `grafana_oncall_schedule`), Slack chatops with Acknowledge/Resolve/Silence, and the P1-P4 incident lifecycle. Use when wiring Alertmanager to OnCall, deciding which team gets paged, building rotations from a Google Calendar / iCal, hooking up Slack notifications, or declaring an incident from an alert — even when the user says "page the platform team on critical alerts", "send Prometheus alerts to Slack", "set up our on-call rota", "escalation policy", or "auto-resolve when the alert clears" without naming OnCall / IRM. Heads up — OnCall OSS is in maintenance mode (archived March 2026); Grafana Cloud users should use IRM.

This plugin packages the [`oncall-irm`](skills/oncall-irm/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/oncall-irm) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/oncall-irm/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install oncall-irm@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Doncall-irm),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `oncall-irm`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
