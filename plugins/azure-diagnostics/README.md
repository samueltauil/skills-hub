# azure-diagnostics

Debug Azure production issues using AppLens, Azure Monitor, resource health, and safe triage, including evidence-only diagnosis without live access. WHEN: debug production issues, troubleshoot app service, app service high CPU, app service deployment failure, troubleshoot container apps, container app 503 or target port mismatch, troubleshoot functions, function telemetry missing or stopped after a config/connection-string change, troubleshoot AKS, VM RDP, Linux SSH, VM black screen, can't connect to VM, reset VM password, NSG or firewall blocking, kubectl cannot connect, kube-system/CoreDNS failures, pod pending, crashloop, node not ready, upgrade failures, analyze logs, KQL, insights, image pull failures, cold start issues, health probe failures, resource health, root cause of errors, troubleshoot event hubs, troubleshoot service bus, messaging SDK error, AMQP connection failure, message lock lost, lock renewal during long-running processing, service bus dead letter.

This plugin packages the [`azure-diagnostics`](skills/azure-diagnostics/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-diagnostics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-diagnostics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-diagnostics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-diagnostics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-diagnostics`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
