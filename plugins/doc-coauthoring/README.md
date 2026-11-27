# doc-coauthoring

Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.

This plugin packages the [`doc-coauthoring`](skills/doc-coauthoring/SKILL.md) skill from
[anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/doc-coauthoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install doc-coauthoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddoc-coauthoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `doc-coauthoring`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[anthropics/skills](https://github.com/anthropics/skills).
