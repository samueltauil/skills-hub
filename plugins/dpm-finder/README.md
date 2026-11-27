# dpm-finder

Find the Prometheus metrics that drive your Grafana Cloud bill. `dpm-finder` is a Grafana Professional Services CLI that ranks metrics by Data Points per Minute (DPM) with per-label-set breakdown, optional `--cost-per-1000-series` pricing, and a Prometheus-exporter mode. Use when investigating high Grafana Cloud spend, hunting noisy / high-cardinality metrics, comparing pre/post recording-rule cardinality, or feeding cost data into dashboards — even when the user says "why is my Mimir bill so high?", "find the biggest metrics", "cardinality offenders", or "optimize Prometheus cost" without naming dpm-finder.

This plugin packages the [`dpm-finder`](skills/dpm-finder/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/dpm-finder) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dpm-finder/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dpm-finder@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddpm-finder),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dpm-finder`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
