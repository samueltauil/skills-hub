# pathways-workload

Debugs failed, crashing or hung Pathways on Cloud workloads (JAX training or inference on Cloud TPU in GKE, run as a JobSet, PathwaysJob or LeaderWorkerSet). Reads Cloud Logging for every Pathways container (user workload, IFRT proxy, pathways-rm, pathways-worker, colocated Python sidecar), node kernel logs and GKE events, then reports the earliest real error, the root cause and a fix. Use when a Pathways workload fails to start, crashes, restarts or stops making progress, or shows errors such as IFRT proxy connection failures, DEADLINE_EXCEEDED lost connection to peer, host OOM kills, ImagePullBackOff, or JAX and Pathways version mismatches. Don't use for GKE workloads that don't use Pathways, or for creating clusters or deploying new Pathways workloads.

This plugin packages the [`pathways-workload`](skills/pathways-workload/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/pathways-workload) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pathways-workload/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pathways-workload@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpathways-workload),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pathways-workload`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
