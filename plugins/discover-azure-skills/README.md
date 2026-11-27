# discover-azure-skills

Searches the Azure skills catalog and recommends installable agent skills by matching an Azure task to skill metadata and plugin installation guidance. WHEN: before starting any task that involves an Azure or Microsoft-cloud service, product, or data source, when no currently loaded skill or tool already covers it.

This plugin packages the [`discover-azure-skills`](skills/discover-azure-skills/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/discover-azure-skills) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/discover-azure-skills/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install discover-azure-skills@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddiscover-azure-skills),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `discover-azure-skills`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
