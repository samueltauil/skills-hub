# fetch-and-send-data

Call APIs, load data into components, and handle the async lifecycle in Blazor. USE FOR fetching data from a backend, submitting data to an API, displaying loading/error states, registering HttpClient, building service abstractions for Auto/WebAssembly render modes. DO NOT USE for form validation (see collect-user-input), prerendering persistence (see support-prerendering), or project scaffolding (see create-blazor-project).

This plugin packages the [`fetch-and-send-data`](skills/fetch-and-send-data/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/fetch-and-send-data) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/fetch-and-send-data/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install fetch-and-send-data@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfetch-and-send-data),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `fetch-and-send-data`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
