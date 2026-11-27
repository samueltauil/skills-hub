# transcribe

Transcribe audio files to text with optional diarization and known-speaker hints. Use when a user asks to transcribe speech from audio/video, extract text from recordings, or label speakers in interviews or meetings.

This plugin packages the [`transcribe`](skills/transcribe/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/transcribe) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/transcribe/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install transcribe@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtranscribe),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `transcribe`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
