# k6-docs

Write or review k6 documentation across the three k6 repositories - k6-DefinitelyTyped (TypeScript types), k6-docs (user documentation), and k6 (release notes / changelog). Applies k6 doc style conventions, generates TypeScript type definitions, drafts release notes, and validates examples by running them against k6@master. Use when working on k6 documentation, the k6 changelog, the k6 release notes, k6 API reference, k6 TypeScript types, load testing docs, or when the user asks to write, edit, or review anything in the k6, k6-docs, or k6-DefinitelyTyped repos - even if they don't explicitly say "documentation".

This plugin packages the [`k6-docs`](skills/k6-docs/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6-docs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6-docs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6-docs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6-docs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6-docs`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
