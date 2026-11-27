# apigee-agent-gateway-governance

Stands up an Apigee API proxy that a Google Cloud Agent Gateway calls as an ext-proc (Service Extension) callout on an agent's LLM traffic, to meter token usage per model, extract caller identity, and apply Model Armor prompt screening or a semantic cache. Use when wiring Apigee in as an AI gateway behind an Agent Gateway, when an agent's model egress needs governing, or when a callout proxy returns no verdict and you need to find out why. The distinguishing question is whether Apigee forwards the traffic or only inspects it: this skill is inspect-only, and builds the proxy itself. Don't use it when Apigee is meant to receive a request and route it onward to a backend — including hosting an MCP server behind Apigee — which needs a proxy with a target instead. Don't use for governing the agent's calls to tools or MCP servers. Don't use for choosing or switching which model a request goes to. Don't use for creating the Agent Gateway itself, nor for Apigee hybrid.

This plugin packages the [`apigee-agent-gateway-governance`](skills/apigee-agent-gateway-governance/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/apigee-agent-gateway-governance) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/apigee-agent-gateway-governance/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install apigee-agent-gateway-governance@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapigee-agent-gateway-governance),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `apigee-agent-gateway-governance`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
