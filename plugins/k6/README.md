# k6

Generate, validate, and review k6 test scripts — load, stress, spike, soak, smoke, breakpoint, functional, and protocol. Covers HTTP, WebSocket, gRPC, browser, all executors, thresholds, checks, custom metrics, the k6-testing library, k6 Cloud execution, and the xk6 extension ecosystem; uses the xk6-docs CLI (with grafana.com web fallback) for docs lookup and validates every script by running it. Use when writing, generating, validating, or debugging any k6 or load-test script (including plain-language asks like "load test this API" or "stress test my service"), choosing executors/scenarios, or setting thresholds. For end-to-end website performance suites use k6-perf-test-website; for documenting k6 itself use k6-docs; for a browser/UI test authored from a plain-language user journey (selectors discovered by exploring the live site) use k6-browser-test.

This plugin packages the [`k6`](skills/k6/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
