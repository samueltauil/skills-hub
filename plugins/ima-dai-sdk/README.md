# ima-dai-sdk

Integrates the Google Interactive Media Ads (IMA) Dynamic Ad Insertion (DAI) SDK into websites, web apps, mobile apps, or TV apps. Use when: - A video player needs to load and play HLS or DASH streams in web apps, Android apps, iOS apps, tvOS apps, Cast (CAF) receivers, or Roku channels. - The app needs to make use of a Google DAI livestream event asset key, or content source CMS ID, video ID for video on demand. Don't use this skill to load and play a VAST or VMAP URL.

This plugin packages the [`ima-dai-sdk`](skills/ima-dai-sdk/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/ads/ima-dai-sdk) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/ima-dai-sdk/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install ima-dai-sdk@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dima-dai-sdk),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `ima-dai-sdk`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
