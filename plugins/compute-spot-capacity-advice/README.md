# compute-spot-capacity-advice

Evaluates Google Compute Engine (GCE) Spot VM capacity obtainability, placement likelihood, and machine family or regional flexibility. Use when planning batch workloads, finding available Spot CPU or GPU capacity, assessing stockout risks, or optimizing instance distribution across zones. Don't use for TPU availability, on-demand reservation capacity (use compute-on-demand-reservations), or future GPU/TPU calendar bookings (use compute-future-reservations).

This plugin packages the [`compute-spot-capacity-advice`](skills/compute-spot-capacity-advice/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/compute-spot-capacity-advice) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/compute-spot-capacity-advice/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install compute-spot-capacity-advice@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcompute-spot-capacity-advice),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `compute-spot-capacity-advice`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
