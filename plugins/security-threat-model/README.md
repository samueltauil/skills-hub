# security-threat-model

Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concise Markdown threat model. Trigger only when the user explicitly asks to threat model a codebase or path, enumerate threats/abuse paths, or perform AppSec threat modeling. Do not trigger for general architecture summaries, code review, or non-security design work.

This plugin packages the [`security-threat-model`](skills/security-threat-model/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/security-threat-model/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install security-threat-model@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecurity-threat-model),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `security-threat-model`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
