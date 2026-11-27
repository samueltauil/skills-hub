# vectorization

Design, implement, optimize, and review SIMD code in .NET. USE FOR: vectorizing scalar loops with TensorPrimitives, Vector64/128/256/512, or platform hardware intrinsics; reviewing existing SIMD code, including the generic Vector type, for contract equivalence, tail handling, memory safety, portability, fallbacks, and measured performance. DO NOT USE FOR: performance work unrelated to SIMD or vectorization.

This plugin packages the [`vectorization`](skills/vectorization/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-advanced/skills/vectorization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/vectorization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install vectorization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dvectorization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `vectorization`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
