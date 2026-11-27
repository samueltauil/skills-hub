# gemini-omni-flash-api

Use this skill for generative video editing, text-to-video, image- and video-referenced video generation, first-frame-to-video, first-and-last-frame transitions, and video extensions using Gemini Omni 1.2 Flash (gemini-omni-1.2-flash) via the official google-genai SDK. Includes workflows for pre-processing/optimizing high-resolution or long source videos with ffmpeg, stripping audio for full sound regeneration, and handling turn-by-turn video editing and parallel execution.

This plugin packages the [`gemini-omni-flash-api`](skills/gemini-omni-flash-api/SKILL.md) skill from
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-omni-flash-api) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-omni-flash-api/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-omni-flash-api@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-omni-flash-api),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-omni-flash-api`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills).
