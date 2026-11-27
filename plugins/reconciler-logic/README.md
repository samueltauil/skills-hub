# reconciler-logic

Implement reconcilers and watchers for grafana-app-sdk apps — write `TypedReconciler[*MyKind]` reconcile functions, apply generation-based skip patterns, do conflict-safe status updates via `resource.UpdateObject`, configure `BasicReconcileOptions` (namespace, label/field filters, finalizer management), use `Watcher` for event-style handling, reconcile `UnmanagedKinds` (resources your app doesn't own), and register the whole thing in `app.go`. Use when writing a reconciler, implementing the reconcile loop, adding async business logic, handling create/update/delete events, processing resource state changes, scheduling periodic resyncs with `RequeueAfter`, picking between Watcher and Reconciler, or wiring a controller into `app.go` — even when the user says "process this resource", "handle X events", or "write a controller" without saying "reconciler".

This plugin packages the [`reconciler-logic`](skills/reconciler-logic/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-app-sdk/reconciler-logic) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/reconciler-logic/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install reconciler-logic@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dreconciler-logic),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `reconciler-logic`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
