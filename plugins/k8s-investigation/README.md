# k8s-investigation

Investigate Kubernetes workload, node, and control-plane issues using OTel telemetry (EDOT). Use when diagnosing pod failures (CrashLoopBackOff, OOMKilled, Error), node pressure, resource exhaustion, image pull failures, admission rejections, autoscaling anomalies, or correlating K8s state with application signals. OTel ingest path only — the legacy ECS Kubernetes integration shape is out of scope.

This plugin packages the [`observability-k8s-investigation`](skills/observability-k8s-investigation/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/observability/k8s-investigation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k8s-investigation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k8s-investigation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk8s-investigation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k8s-investigation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
