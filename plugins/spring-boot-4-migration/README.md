# spring-boot-4-migration

Migrate a Spring Boot 3.x application to Spring Boot 4.0 (Spring Framework 7, Jackson 3, modular starters, JSpecify). Use only for an explicit Boot 3.x to 4 migration, or to fix build or test failures caused by it, or to review one. Not for 3.x patch bumps or 4.0 to 4.1 upgrades; follow the target Boot version release notes and upgrade guide for those. Covers Maven and Gradle (Kotlin DSL, version catalogs).

This plugin packages the [`spring-boot-4-migration`](skills/spring-boot-4-migration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/spring-boot-4-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/spring-boot-4-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install spring-boot-4-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dspring-boot-4-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `spring-boot-4-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
