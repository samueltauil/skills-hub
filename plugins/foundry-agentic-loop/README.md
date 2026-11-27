# foundry-agentic-loop

Build agentic solutions on Microsoft Foundry, GitHub and Azure: hosted agents, toolbox tools and skills, Foundry IQ grounding and a React/FastAPI app. Three modes: rapid prototyping in an existing Foundry project; spec-driven development (SDD), where the foundry-agentic-loop-workflow runs Specify, Implement, Verify and Deploy to create the Foundry project and deploy with azd, or one phase runs alone; and Improve, which refines this skill and the workflow from past runs. Use for Agentic Loop requests and canvas actions, or end-to-end agent solutions from architecture to Azure deployment. Not for isolated Azure administration or unrelated UI edits.

This plugin packages the [`foundry-agentic-loop`](skills/foundry-agentic-loop/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/foundry-agentic-loop) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/foundry-agentic-loop/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install foundry-agentic-loop@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfoundry-agentic-loop),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `foundry-agentic-loop`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
