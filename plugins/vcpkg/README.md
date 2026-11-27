# vcpkg

Guide for setting up vcpkg in C++ projects, managing dependency versions, and cross-compiling. Covers manifest initialization, CMake and Visual Studio integration, classic-to-manifest migration, version pinning, baselines, overrides, triplets, and cross-compilation. Use when a user is working with vcpkg project setup, installation, version management, or cross-platform builds. For specialized tasks, additional references cover custom registries and overlay ports (references/registries.md), CI/CD and binary caching (references/ci.md), and troubleshooting and dependency lifecycle (references/troubleshooting.md).

This plugin packages the [`vcpkg`](skills/vcpkg/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/vcpkg) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/vcpkg/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install vcpkg@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dvcpkg),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `vcpkg`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
