# alerting-irm

Configure Grafana Alerting, Incident Response Management (IRM), and SLOs end-to-end — provisions Grafana-managed and data-source-managed alert rules, contact points (Slack/PagerDuty/email/webhook), notification policies with hierarchical matchers, silences, mute timings, on-call schedules and escalation chains, incident-management integrations, and SLOs with multi-window burn-rate alerts. Use when configuring alerts, debugging notification routing, setting up on-call rotations, declaring or managing incidents, defining SLOs, provisioning alerting via YAML or API, picking matchers for a notification policy, building a PagerDuty/Slack webhook receiver, or troubleshooting why an alert isn't firing — even when the user says "page me on errors", "alert me when X happens", "route this to the platform team", or "set up an SLO" without naming Alerting or IRM.

This plugin packages the [`alerting-irm`](skills/alerting-irm/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/alerting-irm) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/alerting-irm/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install alerting-irm@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dalerting-irm),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `alerting-irm`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
