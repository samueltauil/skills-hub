# arize-link

Generates deep links to the Arize UI for traces, spans, sessions, datasets, labeling queues, evaluators, and annotation configs. Produces clickable URLs for sharing Arize resources with team members. Use when the user wants to link to or open a trace, span, session, dataset, evaluator, or annotation config in the Arize UI.

This plugin packages the [`arize-link`](skills/arize-link/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/arize-link) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/arize-link/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install arize-link@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Darize-link),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `arize-link`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
