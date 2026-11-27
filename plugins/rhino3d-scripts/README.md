# rhino3d-scripts

Authoring and debugging scripts for Rhinoceros 3D (Rhino 8 and later). Use when asked to write RhinoScript (VBScript / .rvb / .vbs), RhinoPython, or RhinoCommon-based scripts; automate Rhino modeling tasks; build command macros; manipulate Rhino geometry, layers, blocks, or document objects; pick objects from the viewport; control redraw and undo; or load and run scripts from the Rhino Script Editor. Covers `rhinoscriptsyntax`, `scriptcontext`, the `Rhino.*` RhinoCommon namespaces (`Rhino.Geometry`, `Rhino.DocObjects`, `Rhino.Input`, `Rhino.UI`, `Rhino.Display`, `Rhino.FileIO`), and the Rhino 8 unified Script Editor.

This plugin packages the [`rhino3d-scripts`](skills/rhino3d-scripts/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/rhino3d-scripts) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/rhino3d-scripts/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install rhino3d-scripts@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Drhino3d-scripts),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `rhino3d-scripts`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
