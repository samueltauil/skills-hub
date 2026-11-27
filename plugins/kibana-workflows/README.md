# kibana-workflows

Author, validate, test, run, and inspect Elastic Workflow YAML definitions. Use when the user wants to turn natural language into a Kibana workflow, fix workflow YAML, understand triggers or steps, or run a quick test loop against a real Kibana.

This plugin packages the [`kibana-workflows`](skills/kibana-workflows/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-workflows) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/kibana-workflows/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install kibana-workflows@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dkibana-workflows),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `kibana-workflows`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
