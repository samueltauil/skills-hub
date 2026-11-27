# xlsx

Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like "the xlsx in my downloads") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.

This plugin packages the [`xlsx`](skills/xlsx/SKILL.md) skill from
[anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/xlsx) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/xlsx/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install xlsx@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dxlsx),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `xlsx`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[anthropics/skills](https://github.com/anthropics/skills).
