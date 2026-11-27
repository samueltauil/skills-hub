# frontend-session-rca

Diagnoses a Grafana Frontend Observability (RUM) session: whether it is healthy, what went wrong, ranked problems with timestamps and evidence, likely cause, how to fix it. Optional follow-up: zoom in on the top error, impact across sessions, Session Replay, or a Tempo trace if the user asks. Fetches telemetry with `gcx frontend sessions get --save` and reads only that dump file. Use when the user asks to explain, diagnose, analyse, RCA, or review a session; asks if a session is healthy; pastes Frontend Observability session context (app id, session id, datasource UID); or mentions Faro, user journey, Core Web Vitals, exceptions, ANR, or a web or mobile RUM session — even if they do not say "session narrator" or "frontend-session-rca". Do not use this skill to instrument an app (Faro Web, React Native, Flutter, native OpenTelemetry) — use `app-observability` for Faro Web setup instead.

This plugin packages the [`frontend-session-rca`](skills/frontend-session-rca/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/frontend-session-rca) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/frontend-session-rca/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install frontend-session-rca@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfrontend-session-rca),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `frontend-session-rca`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
