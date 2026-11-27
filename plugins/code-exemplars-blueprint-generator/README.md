# code-exemplars-blueprint-generator

Technology-agnostic prompt generator that creates customizable AI prompts for scanning codebases and identifying high-quality code exemplars. Supports multiple programming languages (.NET, Java, JavaScript, TypeScript, React, Angular, Python) with configurable analysis depth, categorization methods, and documentation formats to establish coding standards and maintain consistency across development teams.

This plugin packages the [`code-exemplars-blueprint-generator`](skills/code-exemplars-blueprint-generator/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/code-exemplars-blueprint-generator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/code-exemplars-blueprint-generator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install code-exemplars-blueprint-generator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcode-exemplars-blueprint-generator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `code-exemplars-blueprint-generator`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
