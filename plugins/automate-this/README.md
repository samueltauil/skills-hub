# automate-this

Analyze a screen recording of a manual process and produce targeted, working automation scripts. Extracts frames and audio narration from video files, reconstructs the step-by-step workflow, and proposes automation at multiple complexity levels using tools already installed on the user machine.

This plugin packages the [`automate-this`](skills/automate-this/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/automate-this) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/automate-this/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install automate-this@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dautomate-this),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `automate-this`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
