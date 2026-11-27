# brag-sheet

Turn vague "what did I do?" into evidence-backed impact statements for performance reviews, self-reviews, promotion packets, and weekly updates. Uniquely mines Copilot CLI session logs to reconstruct forgotten work, plus git commits and GitHub PRs. Enforces a 3-part impact contract (action → result → evidence). Works standalone with zero dependencies. Trigger for: "brag", "log work", "what did I do", "backfill my work history", "performance review", "self-review", "self assessment", "write impact statement", "review prep", "promo packet", "promotion case", "weekly update", "status report", "accomplishments", "what did I ship", "I forgot to log my work", "summarize my work", "track my wins", "what should I highlight", "end of half", "career growth", "work journal", or any request to document, summarize, or organize work accomplishments.

This plugin packages the [`brag-sheet`](skills/brag-sheet/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/brag-sheet) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/brag-sheet/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install brag-sheet@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbrag-sheet),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `brag-sheet`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
