# tm7-threat-model

Creates valid Microsoft Threat Modeling Tool (.tm7) files compatible with the Microsoft Threat Modeling Tool v7.3+. Use this skill whenever asked to create, generate, or modify a .tm7 threat model file, or when performing STRIDE threat modeling that should output a .tm7 file that opens cleanly in the Microsoft Threat Modeling Tool.

This plugin packages the [`tm7-threat-model`](skills/tm7-threat-model/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/tm7-threat-model) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/tm7-threat-model/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install tm7-threat-model@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtm7-threat-model),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `tm7-threat-model`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
