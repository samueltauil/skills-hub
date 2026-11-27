# daily-focus-board

Spin up a personal, motivating daily focus board that renders in a browser canvas and that the user drives by talking to their AI partner. Tasks track status (to-do → in progress → done) with timestamped progress notes and roll up into a "today's momentum" feed; numeric-goal tasks (pages, pomodoros, reps) render as progress-bar counters. Executive-function / neurodivergent-friendly by design: Focus mode, kind "not today" carryover (no overdue-shaming), a brain-dump box, reduced-motion, and gentle deadline countdowns. Add, reorder, and relabel tasks live, assign Eisenhower priority (Do first / Schedule / Delegate / Later), open with an above/below-the-line check-in and a daily mantra, and save an end-of-day recap. Use when someone wants to plan their day, stay focused, kick off a work session, or track progress. Progress persists in the browser (localStorage).

This plugin packages the [`daily-focus-board`](skills/daily-focus-board/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/daily-focus-board) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/daily-focus-board/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install daily-focus-board@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddaily-focus-board),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `daily-focus-board`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
