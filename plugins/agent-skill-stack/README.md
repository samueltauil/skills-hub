# agent-skill-stack

Find, evaluate, and assemble the smallest compatible set of AI Agent Skills for an end-to-end natural-language goal. Use when a user wants Skills for a multi-step workflow, asks which Skills fit a project, needs an installed-Skill audit or conflict check, has low Skill recall, wants indirect helpers such as humanizers or compliance checks, or wants a project-specific Skill Stack with controlled installation. Search local Skills, registries, GitHub, and OpenCLI; compare adoption, verified fit, safety, and overlap. Do not use for locating one known or common Skill; use the generic find-skills workflow.

This plugin packages the [`agent-skill-stack`](skills/agent-skill-stack/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/agent-skill-stack) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-skill-stack/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-skill-stack@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-skill-stack),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-skill-stack`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
