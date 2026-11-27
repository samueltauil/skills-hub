# arize-prompt-optimization

Optimizes, improves, and debugs LLM prompts using production trace data, evaluations, and annotations. Extracts prompts from spans, gathers performance signal, and runs a data-driven optimization loop using the ax CLI. Use when the user mentions optimize prompt, improve prompt, make AI respond better, improve output quality, prompt engineering, prompt tuning, or system prompt improvement.

This plugin packages the [`arize-prompt-optimization`](skills/arize-prompt-optimization/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/arize-prompt-optimization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/arize-prompt-optimization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install arize-prompt-optimization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Darize-prompt-optimization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `arize-prompt-optimization`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
