# send-data

Sending telemetry data to Grafana Cloud — metrics via Prometheus remote write or OTLP, logs via Loki push or Alloy, traces via OTLP to Tempo, profiles via Pyroscope. Covers Alloy-based pipelines, direct SDK/agent integrations, cloud integrations catalog, and credentials management. Use when connecting an application or infrastructure to Grafana Cloud, setting up data ingestion, configuring remote write, or choosing between ingestion methods.

This plugin packages the [`send-data`](skills/send-data/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/send-data) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/send-data/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install send-data@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsend-data),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `send-data`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
