# gha-security-review

GitHub Actions security review for workflow exploitation vulnerabilities. Use when asked to "review GitHub Actions", "audit workflows", "check CI security", "GHA security", "workflow security review", or review .github/workflows/ for pwn requests, expression injection, credential theft, and supply chain attacks. Exploitation-focused with concrete PoC scenarios.

This plugin packages the [`gha-security-review`](skills/gha-security-review/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/gha-security-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gha-security-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gha-security-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgha-security-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gha-security-review`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
