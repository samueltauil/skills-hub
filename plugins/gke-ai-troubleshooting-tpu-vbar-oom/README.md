# gke-ai-troubleshooting-tpu-vbar-oom

Diagnoses and prevents vbar_control_agent segfaults, out-of-memory (OOM) errors, and TPU device initialization failures on TPU v6e nodes in GKE caused by race conditions during TPU device resets or high-frequency metrics polling. Use when troubleshooting vbar_control_agent crashes, memory cgroup OOMs in serial console logs, tpu-device-plugin metrics checksum corruption errors, or custom TPU metrics collection conflicts on GKE TPU v6e nodes. Don't use for general non-TPU container OOM troubleshooting or standard GKE node lifecycle operations.

This plugin packages the [`gke-ai-troubleshooting-tpu-vbar-oom`](skills/gke-ai-troubleshooting-tpu-vbar-oom/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-vbar-oom) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-vbar-oom/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-vbar-oom@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-vbar-oom),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-vbar-oom`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
