# shopify-review-triage

Use this skill when someone wants public Shopify App Store reviews, low-star reviews, or merchant feedback triaged, prioritized, clustered, or turned into a product or support brief. Trigger for prompts like "triage these app store reviews", "what should we fix first from this feedback", "cluster our 1-star reviews", or "write a weekly low-star review brief", for a single Shopify app or a portfolio plus watched competitors. Produces a P0-P3 brief covering incident risk, repeated friction, pricing confusion, feature requests, and an explicit needs-human-read bucket, where every item keeps its public source link and stays labeled first pass or human-checked. Do not trigger for support tickets, order data, or any other private merchant data, and never use it to reply to or contact a reviewer.

This plugin packages the [`shopify-review-triage`](skills/shopify-review-triage/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/shopify-review-triage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/shopify-review-triage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install shopify-review-triage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dshopify-review-triage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `shopify-review-triage`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
