# java-add-graalvm-native-image-support

GraalVM Native Image skill for Spring Boot, Micronaut and plain Java: detects the build tool and framework, adds native image support, builds the executable, analyzes errors, and iterates until the native build succeeds and the binary runs correctly. For Quarkus projects it only dispatches to the quarkus-native-and-container skill.

This plugin packages the [`java-add-graalvm-native-image-support`](skills/java-add-graalvm-native-image-support/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/java-add-graalvm-native-image-support) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/java-add-graalvm-native-image-support/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install java-add-graalvm-native-image-support@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Djava-add-graalvm-native-image-support),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `java-add-graalvm-native-image-support`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
