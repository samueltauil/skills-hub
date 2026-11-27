# dashboarding

Build, modify, and ship Grafana dashboards as JSON via the HTTP API — panel types (timeseries / stat / gauge / table / heatmap / logs / traces / node-graph), `gridPos` 24-column layout, units, thresholds, template + datasource + chained variables, transformations (`organize` / `calculateField` / `filterByValue`), panel + dashboard links with `${__field.labels.x}` / `${__from}`, and Loki/Prometheus annotations. Use when scripting dashboard creation, writing the dashboard JSON for a new service, adding a `$job` dropdown variable, computing an "Error %" column with a transformation, overlaying deploys as annotations, or pushing a dashboard via `POST /api/dashboards/db` — even when the user says "create a dashboard for this metric", "add a service dropdown", "show errors as percentage", "overlay our deploys", or "export the dashboard JSON" without naming the API or schema. After every API push, verify with the returned `version` plus a GET on the dashboard UID.

This plugin packages the [`dashboarding`](skills/dashboarding/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/dashboarding) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dashboarding/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dashboarding@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddashboarding),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dashboarding`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
