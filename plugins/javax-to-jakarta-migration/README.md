# javax-to-jakarta-migration

Migrate Java code from javax.* to jakarta.* namespace. Use only when the user explicitly asks for a javax to jakarta namespace or framework migration (for example to Tomcat 10+/11 or Jakarta EE), or when java-upgrade or spring-boot-4-migration delegates it. Finding javax imports alone does not authorize a migration.

This plugin packages the [`javax-to-jakarta-migration`](skills/javax-to-jakarta-migration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/javax-to-jakarta-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/javax-to-jakarta-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install javax-to-jakarta-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Djavax-to-jakarta-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `javax-to-jakarta-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
