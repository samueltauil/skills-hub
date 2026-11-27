# security-best-practices

Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests security best practices guidance, a security review/report, or secure-by-default coding help. Trigger only for supported languages (python, javascript/typescript, go). Do not trigger for general code review, debugging, or non-security tasks.

This plugin packages the [`security-best-practices`](skills/security-best-practices/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/security-best-practices/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install security-best-practices@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecurity-best-practices),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `security-best-practices`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
