# coordinate-components

Share state between components that don't have a direct parent-child parameter relationship, using cascading values, scoped services with change events, or CascadingValueSource via DI. USE WHEN the user needs a CascadingParameter or CascadingValue that works across render mode boundaries, a shopping cart or notification count accessible from multiple pages, a theme or user preference cascaded app-wide, or when components in different parts of the tree must react when shared data changes. Also USE WHEN cascading values aren't reaching interactive children in per-page interactivity mode, or when the user needs to understand scoped vs singleton service lifetime for state on Blazor Server. DO NOT USE for direct parent-child parameter passing or EventCallback (see author-component), for persisting state across prerender-to-interactive transitions (see support-prerendering), or for service abstractions for data fetching in Auto/WebAssembly (see fetch-and-send-data).

This plugin packages the [`coordinate-components`](skills/coordinate-components/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/coordinate-components) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/coordinate-components/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install coordinate-components@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcoordinate-components),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `coordinate-components`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
