# issue-fields-migration

Bulk-migrate metadata to GitHub issue fields from two sources: repo labels (e.g. priority labels to a Priority field) and Project V2 fields. Use when users say "migrate my labels to issue fields", "migrate project fields to issue fields", "convert labels to issue fields", "copy project field values to issue fields", or ask about adopting issue fields. Issue fields are org-level typed metadata (single select, text, number, date) that replace label-based workarounds with structured, searchable, cross-repo fields.

This plugin packages the [`issue-fields-migration`](skills/issue-fields-migration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/issue-fields-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/issue-fields-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install issue-fields-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dissue-fields-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `issue-fields-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
