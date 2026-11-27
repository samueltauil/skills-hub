# diagnose-ci-gate

Determine whether a failing CI check was caused by the current change, then recommend exactly one action. Use when a required check fails on a pull request, when asked "is this failure mine?", when a job passes locally but fails in CI, or before retrying a red build. Covers fetching the real log, reading the first error instead of the tail, classifying bug / flaky / environment / pipeline, comparing against the base branch and recent runs, reproducing with CI versions, and fixing a flaky test rather than re-running it forever.

This plugin packages the [`diagnose-ci-gate`](skills/diagnose-ci-gate/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/diagnose-ci-gate) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/diagnose-ci-gate/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install diagnose-ci-gate@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddiagnose-ci-gate),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `diagnose-ci-gate`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
