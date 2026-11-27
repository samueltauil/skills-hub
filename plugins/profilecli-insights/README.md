# profilecli-insights

Query live Pyroscope profiles with profilecli, analyze them with pprof, and correlate hot functions with checked-out source code. Use when the user asks to investigate a service with a configured Pyroscope server, profilecli, and pprof.

This plugin packages the [`profilecli-insights`](skills/profilecli-insights/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-lgtm/profilecli-insights) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/profilecli-insights/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install profilecli-insights@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprofilecli-insights),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `profilecli-insights`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
