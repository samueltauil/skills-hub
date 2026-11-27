# stripe-pay

Helps users send funds to another Stripe business, transfer money to a Stripe Profile handle or network ID, or ask whether an agent can pay a Stripe business. Use Stripe Directory to find or verify a recipient when the user doesn't provide an exact Stripe Profile handle or network ID.

This plugin packages the [`stripe-pay`](skills/stripe-pay/SKILL.md) skill from
[stripe/ai](https://github.com/stripe/ai/tree/main/skills/stripe-pay) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/stripe-pay/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install stripe-pay@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dstripe-pay),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `stripe-pay`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[stripe/ai](https://github.com/stripe/ai).
