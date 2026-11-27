# datanalysis-credit-risk

Credit risk data cleaning and variable screening pipeline for pre-loan modeling. Use when working with raw credit data that needs quality assessment, missing value analysis, or variable selection before modeling. it covers data loading and formatting, abnormal period filtering, missing rate calculation, high-missing variable removal,low-IV variable filtering, high-PSI variable removal, Null Importance denoising, high-correlation variable removal, and cleaning report generation. Applicable scenarios arecredit risk data cleaning, variable screening, pre-loan modeling preprocessing.

This plugin packages the [`datanalysis-credit-risk`](skills/datanalysis-credit-risk/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/datanalysis-credit-risk) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/datanalysis-credit-risk/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install datanalysis-credit-risk@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddatanalysis-credit-risk),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `datanalysis-credit-risk`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
