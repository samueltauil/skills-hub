# compute-on-demand-reservations

Inspects, verifies, and manages Google Compute Engine (GCE) On-Demand reservations and analyzes consumed versus available reserved capacity. Use when checking active reservation capacity, determining whether reserved VMs are available or exhausted, verifying reservation targeting (automatic versus specific reservation), or sharing reservations across projects. Don't use for Spot capacity advice (use gcloud compute advice capacity --provisioning-model=SPOT) or future calendar bookings (use compute-future-reservations).

This plugin packages the [`compute-on-demand-reservations`](skills/compute-on-demand-reservations/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/compute-on-demand-reservations) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/compute-on-demand-reservations/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install compute-on-demand-reservations@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcompute-on-demand-reservations),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `compute-on-demand-reservations`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
