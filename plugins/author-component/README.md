# author-component

Create or review Blazor components (.razor files) with correct architecture. USE FOR: writing new Blazor components that do NOT involve JavaScript interop, implementing parameters and EventCallback, RenderFragment slots, component lifecycle (OnInitializedAsync, OnParametersSet), async patterns, IAsyncDisposable, CancellationToken, CSS isolation, code-behind. DO NOT USE FOR: creating new projects (use create-blazor-project), JavaScript interop or calling browser APIs from Blazor (use use-js-interop), forms and validation (use collect-user-input), prerendering issues (use support-prerendering), HTTP data fetching patterns (use fetch-and-send-data), coordinating state between unrelated components (use coordinate-components).

This plugin packages the [`author-component`](skills/author-component/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/author-component) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/author-component/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install author-component@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dauthor-component),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `author-component`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
