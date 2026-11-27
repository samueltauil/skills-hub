# sap-cloud-integration

SAP Cloud Integration (CPI, part of SAP Integration Suite) runtime-specific guidance for building and troubleshooting iFlows. Use when writing or reviewing CPI Groovy scripts, choosing headers vs. exchange properties, designing exception subprocesses, JMS retry, idempotency or data store patterns, or diagnosing adapter errors (SFTP, HTTP/OAuth, SOAP, IDoc, OData, AS2, Cloud Connector) from Message Processing Log (MPL) text. Not for SAP PI/PO, ABAP development, or generic Java/Groovy outside CPI.

This plugin packages the [`sap-cloud-integration`](skills/sap-cloud-integration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/sap-cloud-integration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sap-cloud-integration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sap-cloud-integration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsap-cloud-integration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sap-cloud-integration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
