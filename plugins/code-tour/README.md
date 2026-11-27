# code-tour

Use this skill to create CodeTour .tour files — persona-targeted, step-by-step walkthroughs that link to real files and line numbers. Trigger for: "create a tour", "make a code tour", "generate a tour", "onboarding tour", "tour for this PR", "tour for this bug", "RCA tour", "architecture tour", "explain how X works", "vibe check", "PR review tour", "contributor guide", "help someone ramp up", or any request for a structured walkthrough through code. Supports 20 developer personas (new joiner, bug fixer, architect, PR reviewer, vibecoder, security reviewer, and more), all CodeTour step types (file/line, selection, pattern, uri, commands, view), and tour-level fields (ref, isPrimary, nextTour). Works with any repository in any language.

This plugin packages the [`code-tour`](skills/code-tour/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/code-tour) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/code-tour/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install code-tour@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcode-tour),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `code-tour`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
