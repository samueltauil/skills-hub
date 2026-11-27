# doc-and-modernize

Two related workflows for a locally-cloned codebase, in one skill. Documentation mode produces a single, comprehensive, verifiable architecture document primarily by reading files on disk (local-first) — use it whenever the user wants to understand, map, document, research, or onboard onto a codebase ("research this repo", "write up the architecture", "do an architecture deep dive", "document how this codebase works", "map the system design", "create an onboarding doc"). Modernization mode generates a phased plan to modernize, migrate, upgrade, or rewrite a legacy system ("modernize this", "plan the migration", "how would we rewrite this", "how do we get off this legacy stack"); if no architecture document exists yet it first runs Documentation mode, then continues straight through to the plan. It assumes the legacy stack may be dead, runs a time-boxed feasibility spike, and picks the highest achievable rung on a safety ladder instead of demanding a fully-green legacy CI gate up front.

This plugin packages the [`doc-and-modernize`](skills/doc-and-modernize/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/doc-and-modernize) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/doc-and-modernize/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install doc-and-modernize@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddoc-and-modernize),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `doc-and-modernize`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
