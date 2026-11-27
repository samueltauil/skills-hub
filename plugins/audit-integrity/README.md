# audit-integrity

Enforce output quality, evidence verification, and quality gates across security audits. Use this skill when you perform SAST, SCA, threat modeling, or security code reviews. Use this skill to verify code locations and taint traces for all findings. Use this skill to prevent the suppression of valid security findings. Use this skill to evaluate reports against quality thresholds (score ≥ 8/10) before delivery.

This plugin packages the [`audit-integrity`](skills/audit-integrity/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/audit-integrity) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/audit-integrity/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install audit-integrity@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Daudit-integrity),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `audit-integrity`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
