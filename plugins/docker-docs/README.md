# docker-docs

Use this skill to answer questions about any Docker product from current official Docker documentation instead of memory, even if the user just asks "how do I…", "does Docker support…", "what's the flag for…", or "is this still the right way" about Docker. Covers Docker Desktop, Engine, Build/Buildx/Build Cloud, Compose, Hub, Scout, Docker Hardened Images (DHI), Offload, Testcontainers, Docker Sandboxes (`sbx`, local and cloud sandboxes, Sandboxes API/SDK), Docker Agentic Platform, Docker Agent, MCP Catalog/Toolkit/Gateway, Model Runner, Gordon, and account, admin, security, and billing docs. Searches with the `search_docker_docs` MCP tool when available and otherwise falls back to `docs.docker.com/llms.txt` and per-page Markdown.

This plugin packages the [`docker-docs`](skills/docker-docs/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-docs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-docs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-docs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-docs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-docs`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
