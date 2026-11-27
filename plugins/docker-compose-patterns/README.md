# docker-compose-patterns

Use this skill when creating, modifying, or debugging Docker Compose configurations, even if the user just says they need to wire services together, add a database to their stack, or set up a local development environment with multiple containers. Covers service definitions, health checks, dependency ordering, volumes, networks, environment variables, and development overrides.

This plugin packages the [`docker-compose-patterns`](skills/docker-compose-patterns/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-compose-patterns) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-compose-patterns/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-compose-patterns@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-compose-patterns),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-compose-patterns`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
