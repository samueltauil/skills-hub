# detection-engineering-coverage-evaluation

Automates the end-to-end detection engineering workflow in Google SecOps using MCP tools. Use when fetching threat intelligence from blogs, generating Threat Detection Opportunities (TDOs), simulating attacker behavior with synthetic UDM events, evaluating rule coverage, and deploying gap-closing rules. Don't use for standalone YARA-L 2.0 rule authoring/tuning (use secops-detection-engineering), threat hunting, or SOC investigation.

This plugin packages the [`detection-engineering-coverage-evaluation`](skills/detection-engineering-coverage-evaluation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/detection-engineering-coverage-evaluation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/detection-engineering-coverage-evaluation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install detection-engineering-coverage-evaluation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddetection-engineering-coverage-evaluation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `detection-engineering-coverage-evaluation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
