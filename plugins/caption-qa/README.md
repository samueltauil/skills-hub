# caption-qa

Check SRT or WebVTT captions and subtitles against published standards (Netflix English, BBC subtitle guidelines, DCMP Captioning Key) for reading speed, line length, line count, time on screen, gaps and overlaps, then fix failures by retiming before rewording. Use when asked to QA, lint or validate captions, check whether subtitles read too fast, prepare captions for Netflix, broadcast or educational delivery, or add a caption check to CI.

This plugin packages the [`caption-qa`](skills/caption-qa/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/caption-qa) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/caption-qa/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install caption-qa@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcaption-qa),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `caption-qa`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
