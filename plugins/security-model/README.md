# security-model

Define, review, or update SECURITY_MODEL.md files that tell security review tools a repository's threat model, trust boundaries, invariants, reportable finding classes, and exclusions. Use when asked to "write a security model", "threat model this repo for scanners", "define security review scope", "what counts as a vulnerability here", "update SECURITY_MODEL.md", "why did the scanner flag or miss this", or to check whether existing security guidance still matches the code. Not for running a security review or editing the SECURITY.md disclosure policy.

This plugin packages the [`security-model`](skills/security-model/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/security-model) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/security-model/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install security-model@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecurity-model),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `security-model`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
