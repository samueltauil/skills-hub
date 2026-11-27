# check-npm

Audit a JavaScript/TypeScript repo's npm, yarn, or pnpm configuration for supply-chain hardening: tool version, lifecycle scripts, unsafe dependency protocols, and minimum release age ≥3 days. Use when the user invokes /check-npm or asks to audit package manager security, lifecycle scripts, git dependencies, ignore-scripts, min-release-age, allow-git, approvedGitRepositories, strictDepBuilds, or blockExoticSubdeps in a Grafana plugin or JS/TS project.

This plugin packages the [`check-npm`](skills/check-npm/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-plugins/check-npm) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/check-npm/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install check-npm@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcheck-npm),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `check-npm`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
