# terraform-azurerm-set-diff-analyzer

Analyze Terraform plan JSON output for AzureRM Provider to distinguish between false-positive diffs (order-only changes in Set-type attributes) and actual resource changes. Use when reviewing terraform plan output for Azure resources like Application Gateway, Load Balancer, Firewall, Front Door, NSG, and other resources with Set-type attributes that cause spurious diffs due to internal ordering changes.

This plugin packages the [`terraform-azurerm-set-diff-analyzer`](skills/terraform-azurerm-set-diff-analyzer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/terraform-azurerm-set-diff-analyzer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/terraform-azurerm-set-diff-analyzer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install terraform-azurerm-set-diff-analyzer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dterraform-azurerm-set-diff-analyzer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `terraform-azurerm-set-diff-analyzer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
