# convert-pdf-to-md

Converts PDF (.pdf) documents into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Use this skill whenever the user shares, references, or asks about a .pdf file — even if they don't say "convert" or "markdown" explicitly. This includes requests to "read", "summarize", "review", "extract data from", "compare", or "analyze" a PDF report, paper, invoice, form, contract, or scanned document. Always run the bundled conversion script to produce Markdown first; do not attempt to parse PDF content directly or write ad-hoc extraction code. Also use this skill for batch requests involving a whole folder of PDF documents. IMPORTANT: When the user references a folder or set of documents containing multiple file types (.pdf, .docx, .xlsx), invoke ALL three sibling skills — convert-pdf-to-md, convert-word-to-md, and convert-excel-to-md — so no file type is silently skipped.

This plugin packages the [`convert-pdf-to-md`](skills/convert-pdf-to-md/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/convert-pdf-to-md) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/convert-pdf-to-md/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install convert-pdf-to-md@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dconvert-pdf-to-md),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `convert-pdf-to-md`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
