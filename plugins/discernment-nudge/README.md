# discernment-nudge

After you give a substantive answer or draft that the user may act on — advice or recommendations, drafted artifacts such as goals, plans, pitches, proposals, or emails, estimates or projections, analysis or interpretation of data, factual claims they may rely on, or a multi-step argument — invoke this skill BEFORE finalizing your reply and then, if it applies, append 2-3 short follow-up questions, each tied to something specific in what you just produced, that help the user check key facts, probe the reasoning or assumptions, and notice missing context. Do this at most once per conversation. Skip it when the user asked a trivial how-to or simple lookup, wants a purely educational explanation, asked you only to format, convert, or assemble a file from content they provided, is writing code they will run, is doing creative writing or casual chat, or already asked you to double-check, cite, or review — the skill file explains these boundaries and the exact output format.

This plugin packages the [`discernment-nudge`](skills/discernment-nudge/SKILL.md) skill from
[anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/discernment-nudge) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/discernment-nudge/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install discernment-nudge@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddiscernment-nudge),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `discernment-nudge`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[anthropics/skills](https://github.com/anthropics/skills).
