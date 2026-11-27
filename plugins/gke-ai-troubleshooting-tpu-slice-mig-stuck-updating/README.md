# gke-ai-troubleshooting-tpu-slice-mig-stuck-updating

Diagnose and resolve GKE TPU Dynamic Slice creation and JobSet scheduling failures blocked by underlying Compute Engine managed instance groups (MIGs) stuck in an updating or unstable state (isStable=False). Use when TPU slice creation fails with a SliceCreationFailed status reason, when JobSets remain stuck in pending, or when MIG status reflects isStable=False or versionTarget.isReached=False during TPU slice formation. Don't use for SliceCreationFailed causes unrelated to MIG stability (use gke-ai-troubleshooting-tpu-dynamic-slices-monitoring) or general pod scheduling failures unrelated to TPU slices.

This plugin packages the [`gke-ai-troubleshooting-tpu-slice-mig-stuck-updating`](skills/gke-ai-troubleshooting-tpu-slice-mig-stuck-updating/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-slice-mig-stuck-updating) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-slice-mig-stuck-updating/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-slice-mig-stuck-updating@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-slice-mig-stuck-updating),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-slice-mig-stuck-updating`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
