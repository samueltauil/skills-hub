# quarkus-native-and-container

Build Quarkus native executables (Mandrel/GraalVM), fix native failures with reflection registration, test the native binary, and produce container images and Kubernetes/OpenShift manifests. Use for native, Docker, Jib or Kubernetes work in a Quarkus project.

This plugin packages the [`quarkus-native-and-container`](skills/quarkus-native-and-container/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/quarkus-native-and-container) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/quarkus-native-and-container/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install quarkus-native-and-container@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dquarkus-native-and-container),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `quarkus-native-and-container`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
