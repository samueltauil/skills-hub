# incident-postmortem

Use when an outage, production incident, or significant service degradation has occurred and the team needs a blameless post-mortem / RCA document in the Google SRE format. Triggers on phrases like "write a post-mortem", "incident review", "what went wrong", "outage report", "root cause analysis", "RCA", or "fishbone". Collects incident inputs from the user, uses a fishbone (Ishikawa) diagram to surface candidate causes, drills the strongest branches with 5 Whys, and produces typed action items. Outputs Markdown by default, with HTML, DOCX, or PDF on request.

This plugin packages the [`incident-postmortem`](skills/incident-postmortem/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/incident-postmortem) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/incident-postmortem/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install incident-postmortem@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dincident-postmortem),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `incident-postmortem`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
