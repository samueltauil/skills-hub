# loki

Grafana Loki log aggregation and LogQL query language. Covers LogQL syntax (log queries, metric queries, label matchers, line filters, parsers: json/logfmt/pattern/regexp/unpack, label filters, line_format), Loki architecture, log ingestion via Alloy/Promtail/Fluent Bit, structured metadata, and Logs Drilldown. Use when writing LogQL queries, configuring Loki, troubleshooting log pipelines, or analyzing logs.

This plugin packages the [`loki`](skills/loki/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-lgtm/loki) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/loki/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install loki@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dloki),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `loki`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
