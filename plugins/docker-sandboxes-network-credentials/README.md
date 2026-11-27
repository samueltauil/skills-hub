# docker-sandboxes-network-credentials

Use this skill when configuring what a Docker Sandboxes (`sbx`) sandbox can reach on the network or which credentials it authenticates with, even if the user just says they want to "let the agent call an internal API", "block all network access", "give the agent a GitHub token", or "use a private registry image for a sandbox". Covers `sbx policy init/allow/deny/ls/inspect/log/check/rm network` (global and per-sandbox egress rules, deny-over-allow precedence) and `sbx secret set/set-custom/ls/rm/import` (service secrets, dynamic secrets via --ref/--command, and registry pull credentials with their host-pulls-only-by-default injection scope).

This plugin packages the [`docker-sandboxes-network-credentials`](skills/docker-sandboxes-network-credentials/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-sandboxes-network-credentials) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-sandboxes-network-credentials/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-sandboxes-network-credentials@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-sandboxes-network-credentials),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-sandboxes-network-credentials`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
