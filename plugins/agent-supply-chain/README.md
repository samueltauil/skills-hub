# agent-supply-chain

Verify supply chain integrity for AI agent plugins, tools, and dependencies. Use this skill when: - Generating SHA-256 integrity manifests for agent plugins or tool packages - Verifying that installed plugins match their published manifests - Detecting tampered, modified, or untracked files in agent tool directories - Auditing dependency pinning and version policies for agent components - Building provenance chains for agent plugin promotion (dev → staging → production) - Any request like "verify plugin integrity", "generate manifest", "check supply chain", or "sign this plugin"

This plugin packages the [`agent-supply-chain`](skills/agent-supply-chain/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/agent-supply-chain) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-supply-chain/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-supply-chain@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-supply-chain),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-supply-chain`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
