# python-appservice-deploy

Deploy Python (Flask/Django/FastAPI) code to Azure App Service Linux. WHEN: "Flask App Service", "Django App Service", "FastAPI App Service", "deploy Python to App Service". DO NOT USE FOR: Container Apps, Functions, non-Python, Terraform/Bicep/IaC, full infra — use azure-prepare.

This plugin packages the [`python-appservice-deploy`](skills/python-appservice-deploy/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/python-appservice-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/python-appservice-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install python-appservice-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpython-appservice-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `python-appservice-deploy`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
