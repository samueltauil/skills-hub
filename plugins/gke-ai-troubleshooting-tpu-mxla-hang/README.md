# gke-ai-troubleshooting-tpu-mxla-hang

Diagnose GKE Cloud TPU multi-slice training hangs (Megascale `HANG_DETECTED` logs and hang monitored events) using the ML Diagnostics `Megascale XLA (MXLA) Hang Analyzer` (`gcloud alpha mldiagnostics monitored-events`) and 1-minute Cloud Monitoring multi-slice latency metrics (`kubernetes.io/container/multislice/*`). Distinguishes XLA compiler/HLO launch divergence and host data-input stalls from TPU chip, SparseCore, ICI, or network fabric faults. Use when multi-slice TPU training jobs freeze without progressing steps, emit `HANG_DETECTED`, or stall in collective operations. Don't use for gradual step-time throughput drops without hangs (use gke-ai-troubleshooting-tpu-performance-degradation) or pod preemption/eviction restarts (use gke-ai-troubleshooting-jobset-interruption).

This plugin packages the [`gke-ai-troubleshooting-tpu-mxla-hang`](skills/gke-ai-troubleshooting-tpu-mxla-hang/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-mxla-hang) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-mxla-hang/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-mxla-hang@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-mxla-hang),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-mxla-hang`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
