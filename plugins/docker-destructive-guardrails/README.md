# docker-destructive-guardrails

Use this skill before running, or recommending, any Docker command that deletes, wipes, resets, or otherwise irreversibly changes state — even if the user just says to "clean up", "clear the cache", "start fresh", "wipe everything", "nuke it", "reset", "force remove", or "tear down" Docker resources. Covers generic Docker CLI destructive operations not owned by a more specific skill — `docker rm`, `docker rm -f`, `docker container prune`, `docker kill`, `docker system prune`, `docker rmi`/`docker image rm`, `docker image prune -a`, `docker network rm`, `docker network prune`, `docker builder prune`, `docker buildx rm`, `docker context rm`, and standalone (non-Compose) `docker volume rm`/`docker volume prune`. Also indexes destructive commands owned by other Docker skills (Compose, sandbox, Desktop). Core rule — state exactly what will be lost and get explicit confirmation first, except narrow, low-friction Tier 1 container cleanup.

This plugin packages the [`docker-destructive-guardrails`](skills/docker-destructive-guardrails/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-destructive-guardrails) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-destructive-guardrails/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-destructive-guardrails@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-destructive-guardrails),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-destructive-guardrails`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
