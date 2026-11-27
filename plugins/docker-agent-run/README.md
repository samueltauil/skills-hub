# docker-agent-run

Use this skill when running a Docker Agent with `docker agent run`, choosing a safety/approval mode, using the `--sandbox` isolation flag, setting up aliases, or troubleshooting a run (missing credentials, worktrees). Even if the user just says they want to "run my agent", "make my agent auto-approve tool calls", "run this agent safely", or "why can't my agent see my API key", this skill applies. Covers `--safety` (strict/balanced/restricted/autonomous), `--yolo`, `--sandbox` and its network allowlist, `--worktree`, `docker agent alias`, and `docker agent doctor`.

This plugin packages the [`docker-agent-run`](skills/docker-agent-run/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-agent-run) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-agent-run/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-agent-run@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-agent-run),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-agent-run`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
