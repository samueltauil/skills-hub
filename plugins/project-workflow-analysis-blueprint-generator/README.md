# project-workflow-analysis-blueprint-generator

Comprehensive technology-agnostic prompt generator for documenting end-to-end application workflows. Automatically detects project architecture patterns, technology stacks, and data flow patterns to generate detailed implementation blueprints covering entry points, service layers, data access, error handling, and testing approaches across multiple technologies including .NET, Java/Spring, React, and microservices architectures.

This plugin packages the [`project-workflow-analysis-blueprint-generator`](skills/project-workflow-analysis-blueprint-generator/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/project-workflow-analysis-blueprint-generator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/project-workflow-analysis-blueprint-generator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install project-workflow-analysis-blueprint-generator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dproject-workflow-analysis-blueprint-generator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `project-workflow-analysis-blueprint-generator`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
