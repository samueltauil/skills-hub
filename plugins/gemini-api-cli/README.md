# gemini-api-cli

Call the Gemini API from the shell with gemini-api. Use for media generation (images, TTS, music, video), file and YouTube analysis, audio/video transcription, Deep Research, and sandboxed agents.

This plugin packages the [`gemini-api-cli`](skills/gemini-api-cli/SKILL.md) skill from
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-api-cli) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-api-cli/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-api-cli@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-api-cli),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-api-cli`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills).
