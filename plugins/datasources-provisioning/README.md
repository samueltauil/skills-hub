# datasources-provisioning

Generate a copy-paste Grafana data source provisioning file (YAML or Terraform) for any plugin from its standardized settings schema on the plugins CDN. Use when the user wants to provision or configure a data source as code — e.g. "provision infinity", "datasource yaml for clickhouse", "terraform for the github datasource" — even when they only name the plugin and not the word "provisioning".

This plugin packages the [`datasources-provisioning`](skills/datasources-provisioning/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-datasources/datasources-provisioning) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/datasources-provisioning/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install datasources-provisioning@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddatasources-provisioning),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `datasources-provisioning`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
