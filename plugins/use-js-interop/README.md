# use-js-interop

Add, review, or fix JavaScript interop in Blazor components. USE FOR: calling JavaScript from Blazor, calling .NET from JavaScript, collocated .razor.js modules, IJSRuntime, IJSObjectReference lifecycle, DotNetObjectReference, ElementReference, timing rules for when JS is available, IAsyncDisposable disposal of JS references, server-side JS interop safety. DO NOT USE FOR: general Blazor component authoring without JS interop needs (use author-component), forms (use collect-user-input).

This plugin packages the [`use-js-interop`](skills/use-js-interop/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/use-js-interop) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/use-js-interop/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install use-js-interop@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Duse-js-interop),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `use-js-interop`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
