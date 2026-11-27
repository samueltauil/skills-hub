# spring-observability

Add and review observability in Spring Boot 3/4 apps: Actuator exposure and health probes, Micrometer metrics, Observation API, OpenTelemetry tracing and OTLP/Prometheus export, structured logging with correlation ids, and safe use of heapdump/threaddump. Use when instrumenting, monitoring or troubleshooting a Spring Boot service.

This plugin packages the [`spring-observability`](skills/spring-observability/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/spring-observability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/spring-observability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install spring-observability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dspring-observability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `spring-observability`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
