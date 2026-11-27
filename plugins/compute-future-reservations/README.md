# compute-future-reservations

Evaluates future GPU and TPU reservation feasibility and calendar-mode booking options in Google Compute Engine (GCE). Use when planning future AI/ML training runs, checking reservation availability windows, verifying accelerator cluster topologies, or assessing future capacity lead times. Don't use for active on-demand reservations (use compute-on-demand-reservations), immediate Spot capacity queries (use compute-spot-capacity-advice), or Standard Future Reservations (--reservation-mode=DEFAULT).

This plugin packages the [`compute-future-reservations`](skills/compute-future-reservations/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/compute-future-reservations) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/compute-future-reservations/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install compute-future-reservations@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcompute-future-reservations),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `compute-future-reservations`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
