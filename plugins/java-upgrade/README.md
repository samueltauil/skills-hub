# java-upgrade

Upgrade a Java project to a newer JDK (11 to 17, 17 to 21, 21 to 25) and adopt the new language and library features. Detects the current Java version from the build files, then loads only the matching per-version guide. Use when the user asks to upgrade Java, modernize Java code, or adopt records, sealed classes, pattern matching, virtual threads or other new Java features. For automated end-to-end upgrades see the modernize-java plugin.

This plugin packages the [`java-upgrade`](skills/java-upgrade/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/java-upgrade) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/java-upgrade/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install java-upgrade@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Djava-upgrade),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `java-upgrade`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
