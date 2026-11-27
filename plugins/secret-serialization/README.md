# secret-serialization

Finds secrets, tokens, passwords, and API keys that can leak through generated serialization: Python dataclass repr and asdict, attrs, pydantic model_dump, NamedTuple, JavaScript JSON.stringify and util.inspect, structured logs, tracing spans, and error reports. Use when asked to "check for secret serialization", "credential in repr", "repr=False audit", "secret in spans", "token in logs", or when a change adds a credential field to a dataclass, model, or config object, or adds code that stringifies whole objects or every kwarg into telemetry.

This plugin packages the [`secret-serialization`](skills/secret-serialization/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/secret-serialization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/secret-serialization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install secret-serialization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecret-serialization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `secret-serialization`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
