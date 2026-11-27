# docker-build-strategies

Use this skill when writing, reviewing, or optimizing Dockerfiles, even if the user just says their image is too large, their build is slow, or they need to harden a container for production. Covers multi-stage builds, layer caching, .dockerignore, non-root users, and image size optimization.

This plugin packages the [`docker-build-strategies`](skills/docker-build-strategies/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-build-strategies) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-build-strategies/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-build-strategies@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-build-strategies),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-build-strategies`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
