# agent-platform-agent-registry

Manages Google Cloud Agent Registry (agentregistry.googleapis.com) resources using gcloud CLI and Kubernetes manifests, including agents, MCP servers, endpoints, services, bindings, AI applications, skills and skill revisions, resource-level IAM policies, Cloud Run and GKE automatic workload registration, Cloud Resource Manager management boundaries, 5-endpoint Quick Add for Agent Gateway, and Python ADK integration. Use when registering, discovering, searching, filtering, or governing agents, MCP servers, endpoints, skills, AI applications, or management boundaries in Google Cloud Agent Registry. Don't use for the preview AI Platform Skill Registry Python scripts (use agent-platform-skill-registry), deploying raw Vertex AI Agent Engine code (use agent-platform-deploy), or runtime trace debugging (use agent-platform-troubleshooting).

This plugin packages the [`agent-platform-agent-registry`](skills/agent-platform-agent-registry/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-agent-registry) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-agent-registry/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-agent-registry@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-agent-registry),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-agent-registry`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
