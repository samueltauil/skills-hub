# generate-testability-wrappers

DO NOT USE when the target already consumes an injected interface or built-in abstraction such as IFileSystem or TimeProvider, even if the request says "generate a wrapper"; no new wrapper is needed. Use only when C# source calls an ambient/static dependency and no injectable seam exists: first-time TimeProvider, IHttpClientFactory, or System.IO.Abstractions adoption; minimal Environment/Console/Process wrappers; IProcessRunner; DI registration; or an ambient seam that preserves a static API. Exclude static detection (detect-static-dependencies), migration to an existing/registered abstraction (migrate-static-to-wrapper), one blocked behavior plus deterministic tests (testability-obstacle), and general interface design.

This plugin packages the [`generate-testability-wrappers`](skills/generate-testability-wrappers/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/generate-testability-wrappers) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/generate-testability-wrappers/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install generate-testability-wrappers@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgenerate-testability-wrappers),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `generate-testability-wrappers`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
