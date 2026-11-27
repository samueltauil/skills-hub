# code-testing-extensions

Provides file paths to language-specific extension files for the code-testing pipeline. Read this reference-only catalog for extension guidance files (e.g., dotnet.md for .NET, cpp.md for C++). Agents and skills read its bundled files directly; do not invoke this catalog through the model's skill tool.

This plugin packages the [`code-testing-extensions`](skills/code-testing-extensions/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/code-testing-extensions) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/code-testing-extensions/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install code-testing-extensions@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcode-testing-extensions),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `code-testing-extensions`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
