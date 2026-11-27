# csp-investigation

Investigate cloud-provider (CSP) service issues — AWS today (the reasoning applies to any AWS service; schema and failure signatures are deepest for RDS, Lambda, SQS, ALB, EC2), and in future GCP and Azure — using OTel-schema cloud metrics in Elastic. Use when diagnosing cloud-resource problems, whether alert-triggered or ad hoc: database connection/CPU/memory pressure, function error rates and throttling, queue backlog and consumer lag, load-balancer 5xx, instance saturation. Correlates the resource under investigation against its own baseline, classifies the failure mode, and rules out co-occurring but unrelated conditions.

This plugin packages the [`observability-csp-investigation`](skills/observability-csp-investigation/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/observability/csp-investigation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/csp-investigation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install csp-investigation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcsp-investigation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `csp-investigation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
