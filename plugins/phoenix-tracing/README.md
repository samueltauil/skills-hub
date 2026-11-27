# phoenix-tracing

OpenInference semantic conventions and instrumentation for Phoenix AI observability. Use when implementing LLM tracing, creating custom spans, or deploying to production.

This plugin packages the [`phoenix-tracing`](skills/phoenix-tracing/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/phoenix-tracing) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/phoenix-tracing/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install phoenix-tracing@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dphoenix-tracing),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `phoenix-tracing`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
