# agent-platform-alert-configuration

Configures best-practice alerting policies for AI agents using OpenTelemetry (OTel) metrics, generating output as Terraform (.tf) configuration files. Use when analyzing, writing, or deploying alerting policies to monitor agent latency, error rates, token usage, and quality metrics. Don't use for standard infrastructure monitoring unrelated to AI agents, or when the agent is not instrumented with OpenTelemetry (for Reliability, Cost, Safety, Security alerts). NOTE: Reliability, Cost, Safety, and Security alerts use generic OTel metrics and work across runtimes (such as Cloud Run, Vertex AI). Quality alerts rely on Vertex AI Online Monitors and are strictly bound to Vertex AI deployments.

This plugin packages the [`agent-platform-alert-configuration`](skills/agent-platform-alert-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-alert-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-alert-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-alert-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-alert-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-alert-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
