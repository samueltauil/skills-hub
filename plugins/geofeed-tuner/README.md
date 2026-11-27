# geofeed-tuner

Use this skill whenever the user mentions IP geolocation feeds, RFC 8805, geofeeds, or wants help creating, tuning, validating, or publishing a self-published IP geolocation feed in CSV format. Intended user audience is a network operator, ISP, mobile carrier, cloud provider, hosting company, IXP, or satellite provider asking about IP geolocation accuracy, or geofeed authoring best practices. Helps create, refine, and improve CSV-format IP geolocation feeds with opinionated recommendations beyond RFC 8805 compliance. Do NOT use for private or internal IP address management — applies only to publicly routable IP addresses.

This plugin packages the [`geofeed-tuner`](skills/geofeed-tuner/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/geofeed-tuner) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/geofeed-tuner/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install geofeed-tuner@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgeofeed-tuner),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `geofeed-tuner`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
