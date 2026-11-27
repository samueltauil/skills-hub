# acreadiness-generate-instructions

Generate tailored AI agent instruction files via AgentRC instructions command. Produces .github/copilot-instructions.md (default, recommended for Copilot in VS Code) plus optional per-area .instructions.md files with applyTo globs for monorepos. Use after running /acreadiness-assess to close gaps in the AI Tooling pillar.

This plugin packages the [`acreadiness-generate-instructions`](skills/acreadiness-generate-instructions/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/acreadiness-generate-instructions) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/acreadiness-generate-instructions/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install acreadiness-generate-instructions@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dacreadiness-generate-instructions),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `acreadiness-generate-instructions`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
