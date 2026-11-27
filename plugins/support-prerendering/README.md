# support-prerendering

Make interactive Blazor components work correctly with prerendering. USE FOR fixing duplicate data loads, UI flicker during prerender-to-interactive handoff, null references during prerender, persisting state across prerender, disabling prerendering, excluding pages from interactive routing, or detecting whether a component is currently prerendering. DO NOT USE for choosing which render mode to use (see create-blazor-project) or general component authoring (see author-component).

This plugin packages the [`support-prerendering`](skills/support-prerendering/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/support-prerendering) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/support-prerendering/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install support-prerendering@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsupport-prerendering),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `support-prerendering`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
