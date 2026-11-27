# metronome

Guides Metronome usage-based billing integration decisions — event ingestion (single and batch, idempotency, billable metrics), contract design (rate cards, overrides, dimensional pricing, products), invoicing lifecycle (grace periods, finalization, Stripe sync), credit and commit management (prepaid, postpaid, thresholds, auto-recharge), and Stripe integration (arrears invoicing, tax providers, line item limits). Use when building, modifying, or reviewing any Metronome integration — including ingesting usage events, creating customers, contracts, or rate cards, designing billable metric group keys, managing credits and commits, configuring invoicing, syncing invoices with Stripe Billing, billing AI applications for token usage, setting up self-serve (PLG) pricing, reviewing customer health, commit burn, portfolios, or renewals, or migrating from Stripe Billing Meters to Metronome.

This plugin packages the [`metronome`](skills/metronome/SKILL.md) skill from
[stripe/ai](https://github.com/stripe/ai/tree/main/skills/metronome) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/metronome/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install metronome@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmetronome),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `metronome`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[stripe/ai](https://github.com/stripe/ai).
