# arize-trace

Downloads, exports, and inspects existing Arize traces and spans to understand what an LLM app is doing or debug runtime issues. Covers exporting traces by ID, spans by ID, sessions by ID, and root-cause investigation using the ax CLI. Use when the user wants to look at existing trace data, see what their LLM app is doing, export traces, download spans, investigate errors, or analyze behavior regressions.

This plugin packages the [`arize-trace`](skills/arize-trace/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/arize-trace) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/arize-trace/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install arize-trace@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Darize-trace),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `arize-trace`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
