# on-device-delegate

Saves cloud-model context by briefing one bounded, read-heavy sub-task (more than about 25 KB of prose, or many files that no single command can answer) to the local-coding plugin's on-device worker, which runs on the local MAI Code 1.1 Flash model. Use for log and test triage, summarizing many files, or extracting facts from large inputs. When the user names this skill, call the skill tool in the same response as your first other tool call, never as a separate step.

This plugin packages the [`on-device-delegate`](skills/on-device-delegate/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/on-device-delegate) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/on-device-delegate/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install on-device-delegate@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Don-device-delegate),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `on-device-delegate`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
