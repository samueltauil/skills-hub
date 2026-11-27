# lean-comments

Audits, writes, and refines maintained first-party source-code comments and declaration-level documentation across languages. Use when adding, editing, reviewing, cleaning up, or auditing comments, doc comments, docstrings, TODO, FIXME, NOTE, suppressions, or other source commentary, including while modifying code and deciding whether a comment is warranted at all. Defaults to no comment unless it preserves meaningful, non-obvious information that cannot reasonably be recovered from the code or nearby repository context.

This plugin packages the [`lean-comments`](skills/lean-comments/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/lean-comments) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/lean-comments/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install lean-comments@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dlean-comments),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `lean-comments`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
