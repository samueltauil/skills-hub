# data-breach-blast-radius

Pre-breach impact analysis: inventories sensitive data (PII, PHI, PCI-DSS, credentials), traces data flows, scores exposure vectors, and produces a regulatory blast radius report with fine ranges sourced verbatim from GDPR Art. 83, CCPA § 1798.155(a), and HIPAA 45 CFR § 160.404. Cost benchmarks from IBM Cost of a Data Breach Report (annually updated). All citations in references/SOURCES.md for verification. Use when asked: "assess breach impact", "what data could be exposed", "calculate blast radius", "data exposure analysis", "how bad would a breach be", "quantify data risk", "sensitive data inventory", "data flow security audit", "pre-breach assessment", "worst-case breach scenario", "breach readiness", "data risk report", "/data-breach-blast-radius". For any stack handling user data, health records, or financial information. Output labels law-sourced figures (exact) vs heuristic estimates (planning only). Does not replace legal counsel.

This plugin packages the [`data-breach-blast-radius`](skills/data-breach-blast-radius/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/data-breach-blast-radius) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/data-breach-blast-radius/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install data-breach-blast-radius@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddata-breach-blast-radius),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `data-breach-blast-radius`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
