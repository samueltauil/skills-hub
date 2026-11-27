# arize-annotation

Creates and manages annotation configs (categorical, continuous, freeform label schemas) and annotation queues (human review workflows) on Arize. Applies human annotations to project spans via the Python SDK. Use when the user mentions annotation config, annotation queue, label schema, human feedback, bulk annotate spans, update_annotations, labeling queue, annotate record, or human review.

This plugin packages the [`arize-annotation`](skills/arize-annotation/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/arize-annotation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/arize-annotation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install arize-annotation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Darize-annotation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `arize-annotation`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
