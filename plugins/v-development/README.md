# v-development

Guide GitHub Copilot through V language development: installing the toolchain, project layout with v.mod, building, testing, formatting, and writing idiomatic V including Option/Result error handling. Use when the user works with V source files, v.mod projects, or asks about V syntax, tooling, and conventions.

This plugin packages the [`v-development`](skills/v-development/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/v-development) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/v-development/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install v-development@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dv-development),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `v-development`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
