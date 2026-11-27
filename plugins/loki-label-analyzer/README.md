# loki-label-analyzer

Expert evaluator for Grafana Loki label strategy. Audits, designs, and improves label schemas using cardinality scoring, access-pattern alignment, static vs. dynamic label rules, and consistency checks. Use when the user asks to evaluate, audit, design, or improve a Loki label strategy — or asks why their Loki queries are slow.

This plugin packages the [`loki-label-analyzer`](skills/loki-label-analyzer/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/loki-label-analyzer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/loki-label-analyzer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install loki-label-analyzer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dloki-label-analyzer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `loki-label-analyzer`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
