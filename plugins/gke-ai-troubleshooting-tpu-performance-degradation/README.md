# gke-ai-troubleshooting-tpu-performance-degradation

Diagnose GKE Cloud TPU training throughput drops and step-time regressions (15%+ TPU duty-cycle drop) using ML Diagnostics Workload Monitoring (`gcloud alpha mldiagnostics monitored-events` / `hypercomputecluster.googleapis.com/v1alpha`) and 1-minute Cloud Monitoring system metrics (`kubernetes.io/node/accelerator/*`). Distinguishes hardware and network fabric throttling from workload resource bottlenecks (HBM capacity, host memory, or host CPU saturation). Use when TPU training throughput or duty cycle drops without crashing pods, when `PERFORMANCE_DEGRADATION` monitored events fire, or when triaging slow multi-slice training steps. Don't use for complete multi-slice XLA execution stalls with `HANG_DETECTED` logs (use gke-ai-troubleshooting-tpu-mxla-hang) or pod eviction/interruption restarts (use gke-ai-troubleshooting-jobset-interruption).

This plugin packages the [`gke-ai-troubleshooting-tpu-performance-degradation`](skills/gke-ai-troubleshooting-tpu-performance-degradation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-performance-degradation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-performance-degradation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-performance-degradation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-performance-degradation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-performance-degradation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
