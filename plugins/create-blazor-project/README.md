# create-blazor-project

Create a new ASP.NET Core web application or web site using Blazor. USE FOR: creating a new Blazor web app, scaffolding a new web project, starting a new web site, choosing render modes (Static SSR, Interactive Server, Interactive WebAssembly, Auto), running dotnet new blazor with the right options, setting up initial project structure. DO NOT USE FOR: adding features to existing projects, changing how an existing app renders, or component authoring (use author-component).

This plugin packages the [`create-blazor-project`](skills/create-blazor-project/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/create-blazor-project) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/create-blazor-project/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install create-blazor-project@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcreate-blazor-project),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `create-blazor-project`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
