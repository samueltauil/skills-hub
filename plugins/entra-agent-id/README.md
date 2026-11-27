# entra-agent-id

Provision Microsoft Entra Agent Identity Blueprints, BlueprintPrincipals, and per-instance Agent Identities via Microsoft Graph, and configure OAuth 2.0 token exchange (fmi_path, OBO, cross-tenant) including the Microsoft Entra SDK for AgentID sidecar. USE FOR: Agent Identity Blueprint, BlueprintPrincipal, agent OAuth, fmi_path token exchange, agent OBO, Workload Identity Federation for agents, polyglot agent auth, Microsoft.Identity.Web.AgentIdentities. DO NOT USE FOR: standard Entra app registration (use entra-app-registration), Microsoft Foundry agent authoring (use microsoft-foundry).

This plugin packages the [`entra-agent-id`](skills/entra-agent-id/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/entra-agent-id) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/entra-agent-id/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install entra-agent-id@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dentra-agent-id),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `entra-agent-id`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
