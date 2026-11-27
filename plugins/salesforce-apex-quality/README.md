# salesforce-apex-quality

Apex code quality guardrails for Salesforce development. Enforces bulk-safety rules (no SOQL/DML in loops), sharing model requirements, CRUD/FLS security, SOQL injection prevention, PNB test coverage (Positive / Negative / Bulk), and modern Apex idioms. Use this skill when reviewing or generating Apex classes, trigger handlers, batch jobs, or test classes to catch governor limit risks, security gaps, and quality issues before deployment.

This plugin packages the [`salesforce-apex-quality`](skills/salesforce-apex-quality/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/salesforce-apex-quality) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/salesforce-apex-quality/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install salesforce-apex-quality@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsalesforce-apex-quality),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `salesforce-apex-quality`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
