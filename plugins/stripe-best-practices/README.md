# stripe-best-practices

Guides Stripe integration decisions across development and test environment planning (separate sandboxes vs the shared test mode sandbox), API selection (Checkout Sessions vs PaymentIntents), Connect platform setup (Accounts v2, controller properties), billing/subscriptions, tax and registrations (Stripe Tax, automatic_tax, product tax codes), Treasury financial accounts, integration options (Checkout, Payment Element), migrating from deprecated Stripe APIs, and security best practices (API key management, API key permissions, webhooks, OAuth). Use when planning, building, modifying, testing, or reviewing any Stripe integration, including choosing a development environment, accepting payments, building marketplaces, integrating Stripe, processing payments, setting up subscriptions, collecting sales tax, VAT, or GST, creating connected accounts, or implementing secure key handling.

This plugin packages the [`stripe-best-practices`](skills/stripe-best-practices/SKILL.md) skill from
[stripe/ai](https://github.com/stripe/ai/tree/main/skills/stripe-best-practices) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/stripe-best-practices/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install stripe-best-practices@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dstripe-best-practices),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `stripe-best-practices`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[stripe/ai](https://github.com/stripe/ai).
