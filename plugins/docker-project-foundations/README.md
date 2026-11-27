# docker-project-foundations

Use this skill when setting up, initializing, or Dockerizing a project, even if the user doesn't explicitly mention Docker but describes a need for containerized local development, adding a database or cache dependency, or running services without host-level installs. Covers Dockerfile, compose.yaml, and .dockerignore creation with Docker best practices.

This plugin packages the [`docker-project-foundations`](skills/docker-project-foundations/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-project-foundations) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-project-foundations/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-project-foundations@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-project-foundations),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-project-foundations`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
