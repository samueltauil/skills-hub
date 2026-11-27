# configure-auth

Add authentication and authorization to a Blazor Web App, accounting for the app's render mode. USE WHEN the user needs [Authorize] on pages, AuthorizeView, role or policy-based access, login/logout Identity pages, or AuthenticationStateProvider. Also USE WHEN auth state is null after WebAssembly loads, SignInManager throws in an interactive component, NotAuthorized content never renders in static SSR, or HttpContext.User is null in an interactive component. DO NOT USE for general component authoring (see author-component), for prerendering concerns unrelated to auth (see support-prerendering), or for managing non-auth cascading state (see coordinate-components).

This plugin packages the [`configure-auth`](skills/configure-auth/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/configure-auth) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/configure-auth/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install configure-auth@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dconfigure-auth),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `configure-auth`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
