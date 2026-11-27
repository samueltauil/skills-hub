# triage-frontend-issues

Triage new issues in the Sentry `javascript` project by archiving non-actionable noise. Use when asked to "triage issues", "triage the javascript project", "archive non-actionable issues", "triage new frontend issues", or "clean up the sentry/javascript queue". Operates only on the sentry/javascript project, only archives (never resolves), and always archives with `untilEscalating`.

This plugin packages the [`triage-frontend-issues`](skills/triage-frontend-issues/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/triage-frontend-issues) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/triage-frontend-issues/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install triage-frontend-issues@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtriage-frontend-issues),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `triage-frontend-issues`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
