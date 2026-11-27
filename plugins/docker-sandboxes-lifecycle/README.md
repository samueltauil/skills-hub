# docker-sandboxes-lifecycle

Use this skill when creating, running, reattaching to, listing, stopping, or removing Docker Sandboxes (the standalone `sbx` CLI that runs AI coding agents in isolated microVMs), even if the user just says they want to "run claude in a sandbox", "isolate an agent from my repo", "give an agent its own git clone", or "clean up old sandboxes". Covers `sbx run`/`sbx create` (including the built-in agents claude, codex, cursor, devin, docker-agent, gemini, opencode, shell), workspace bind-mount vs `--clone` isolation, additional read-only workspaces, reattaching by `--name`, `sbx ls`/`stop`/`rm`/`prune`, `sbx exec`, `sbx cp`, and `sbx ports`.

This plugin packages the [`docker-sandboxes-lifecycle`](skills/docker-sandboxes-lifecycle/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-sandboxes-lifecycle) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-sandboxes-lifecycle/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-sandboxes-lifecycle@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-sandboxes-lifecycle),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-sandboxes-lifecycle`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
