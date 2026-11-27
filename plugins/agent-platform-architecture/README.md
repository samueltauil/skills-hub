# agent-platform-architecture

Designs, engineers, and validates enterprise Gemini platform architectures. Use when designing multi-project hierarchies (Host, Central Governance Hub, Runtime Spoke, Tool/MCP Spoke), configuring Agent Gateway, authoring Agent Connectivity Templates (ALL_TRAFFIC vs PRIVATE_RANGES_ONLY), deploying Secure Web Proxy (SWP) with Policy-Based Routing (PBR) or Cross-Cloud mTLS Egress Hubs, configuring Private CA TrustConfig with Internal ALB + Serverless NEG, implementing Unified Access Policies (UAP Policy V2 CEL) and Semantic Governance (SGP), configuring 3P IdP Token Exchange (EntraID/Ping/Okta via ext_proc + STS) or Agent Identity Auth Manager (SPIFFE), enforcing Model Armor Floor Settings and Fail-Closed guardrails, deploying Cross-Project Registry sync, binding ADK agents on Agent Runtime, or executing Day-2 lifecycle operations. Don't use for read-only live log triage or incident diagnosis, or generic Google Cloud Identity and Access Management (IAM) debugging.

This plugin packages the [`agent-platform-architecture`](skills/agent-platform-architecture/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-architecture) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-architecture/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-architecture@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-architecture),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-architecture`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
