# system-text-json-net11

Imperative guidance for the System.Text.Json APIs added in .NET 11: the built-in `JsonNamingPolicy.PascalCase` naming policy, and the strongly-typed generic `JsonSerializerOptions.GetTypeInfo` and `JsonSerializerOptions.TryGetTypeInfo` metadata accessors (generic overloads that return a typed `JsonTypeInfo`). USE ONLY when the user is targeting net11.0 or later and needs PascalCase JSON property or dictionary-key names without writing a custom naming policy, a strongly-typed generic `JsonTypeInfo` instead of the non-generic `JsonTypeInfo`, or a no-throw way to probe whether a type's serialization metadata is resolved. DO NOT USE when the target is earlier than net11.0, the requested behavior uses an established pre-net11 naming policy, or the user explicitly selected another JSON library.

This plugin packages the [`system-text-json-net11`](skills/system-text-json-net11/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet11/skills/system-text-json-net11) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/system-text-json-net11/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install system-text-json-net11@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsystem-text-json-net11),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `system-text-json-net11`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
