# fleet-management

Manage a fleet of Grafana Alloy collectors with Fleet Management — author Alloy pipelines once, target them via attribute matchers (`env="production"`, regex `region=~"us-.*"`), push remotely via OpAMP without restarting collectors. Covers pipeline create / update / matcher RPCs, collector attribute API, `remotecfg` bootstrap block (standalone + Helm), pre-deploy `alloy fmt` validation, the local Alloy UI at port 12345 for component health, and post-deploy `REMOTE_CONFIG_STATUS_APPLIED` verification. Use when standing up a Cloud Alloy fleet, pushing a config change to 200 collectors, hunting why one collector shows `REMOTE_CONFIG_STATUS_FAILED`, validating River syntax before saving, or wiring `discovery.kubernetes` → `prometheus.remote_write` — even when the user says "configure Alloy", "remote config the collectors", "push pipeline", "OpAMP", "collector is unhealthy", or "manage agent config centrally" without naming Fleet Management.

This plugin packages the [`fleet-management`](skills/fleet-management/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/fleet-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/fleet-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install fleet-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfleet-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `fleet-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
