# developer-device-platform-device-run

Runs automated, non-interactive jobs on remote Android devices with Developer Device Platform (DDP) Device Run using `gcloud beta device-run sessions`: native Android executables or shell scripts (for example CLI tools, custom runners, test harnesses or benchmarks) and Android instrumentation tests, on one or many devices, then waits for completion and collects per-device outputs and logs. Use when running a binary or test suite on remote devices without an interactive connection. Don't use it for interactive device reservations, adb tunnels or screen streaming (use developer-device-platform-basics), or for local devices.

This plugin packages the [`developer-device-platform-device-run`](skills/developer-device-platform-device-run/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/developer-device-platform-device-run) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/developer-device-platform-device-run/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install developer-device-platform-device-run@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddeveloper-device-platform-device-run),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `developer-device-platform-device-run`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
