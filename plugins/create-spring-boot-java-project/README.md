# create-spring-boot-java-project

Create a new Spring Boot Java project (Maven or Gradle) from start.spring.io with sensible defaults for configuration, PostgreSQL, logging, security, testing and Docker. Use when asked to scaffold, bootstrap or generate a Spring Boot application. Detects existing project versions and never upgrades implicitly.

This plugin packages the [`create-spring-boot-java-project`](skills/create-spring-boot-java-project/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/create-spring-boot-java-project) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/create-spring-boot-java-project/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install create-spring-boot-java-project@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcreate-spring-boot-java-project),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `create-spring-boot-java-project`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
