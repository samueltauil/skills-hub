# elastic-onboarding

Onboard an application into Elastic Observability with the Elastic Distribution of OpenTelemetry (EDOT): route on language and runtime, detect and replace a classic Elastic APM agent, apply the required OTLP configuration, and then verify with ES|QL that traces, metrics, and logs actually arrive under the expected service name. Use when adding observability to a service, migrating off the classic Elastic APM agent, or debugging why an instrumented service is not showing up in Elastic.

This plugin packages the [`observability-onboarding`](skills/observability-onboarding/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/observability/onboarding) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elastic-onboarding/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elastic-onboarding@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delastic-onboarding),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elastic-onboarding`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
