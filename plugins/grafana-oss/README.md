# grafana-oss

Configure Grafana OSS — provisions dashboards from YAML, sets up data sources (Prometheus / Loki / Tempo / Pyroscope), writes dashboard JSON with template variables, builds panel queries, assigns built-in roles (Viewer / Editor / Admin / GrafanaAdmin), mints service-account tokens, edits grafana.ini server config, creates annotations, installs plugins via provisioning, and validates each step with a health-check curl. Use when building dashboards, configuring data sources, setting up provisioning YAML, picking a panel type, writing template variables, managing users and roles, configuring SMTP/OAuth in grafana.ini, creating annotations via API, troubleshooting why a provisioned dashboard isn't showing up, or running Grafana OSS locally — even when the user says "set up a Prometheus data source", "provision dashboards from git", "make a service account", or "configure SSO in OSS" without saying "Grafana OSS".

This plugin packages the [`grafana-oss`](skills/grafana-oss/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/grafana-oss) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/grafana-oss/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install grafana-oss@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgrafana-oss),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `grafana-oss`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
