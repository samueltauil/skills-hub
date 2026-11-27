# openai-pdf

Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction.

This plugin packages the [`pdf`](skills/pdf/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/pdf) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/openai-pdf/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install openai-pdf@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dopenai-pdf),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `openai-pdf`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
