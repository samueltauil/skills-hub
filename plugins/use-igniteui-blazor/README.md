# use-igniteui-blazor

Add, configure, or review Ignite UI for Blazor Lite component support in Blazor applications. USE FOR: installing IgniteUI.Blazor.Lite or IgniteUI.Blazor.GridLite, registering AddIgniteUIBlazor() in Blazor Server, WASM, Hybrid, or split Blazor Web App projects, adding @using IgniteUI.Blazor.Controls, wiring the theme stylesheet, picking the right host page, locating the GridLite stylesheet path, explaining single-project vs split Server/Client Web App setup differences, and checking where an interactive render mode is needed for Ignite UI components to work. DO NOT USE FOR: general Blazor component authoring without Ignite UI, choosing app architecture or render mode from scratch (see create-blazor-project), JavaScript interop (see use-js-interop), authentication (see configure-auth), prerendering (see support-prerendering), or layout/component design questions that need no Ignite UI setup.

This plugin packages the [`use-igniteui-blazor`](skills/use-igniteui-blazor/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/use-igniteui-blazor) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/use-igniteui-blazor/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install use-igniteui-blazor@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Duse-igniteui-blazor),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `use-igniteui-blazor`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
