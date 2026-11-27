# lsp-setup

Enable code intelligence (go-to-definition, find-references, hover, type info) for any programming language by installing and configuring an LSP server for Copilot CLI. Detects the OS, installs the right server, and generates the JSON configuration (user-level or repo-level). Use when you need deeper code understanding and no LSP server is configured, or when the user asks to set up, install, or configure an LSP server.

This plugin packages the [`lsp-setup`](skills/lsp-setup/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/lsp-setup) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/lsp-setup/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install lsp-setup@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dlsp-setup),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `lsp-setup`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
