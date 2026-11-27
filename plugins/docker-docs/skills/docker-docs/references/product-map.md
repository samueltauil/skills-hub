# Docker product map

Use this map to work out which Docker product the user means and which docs
section to start from. Use it to choose a search query or landing page. It
is not a source to cite. It lists only top-level sections. Find deeper pages
with the search tool, `https://docs.docker.com/llms.txt`, or the
`llms-full.txt` page index. `llms.txt` wins when it disagrees with this file.

Paths are relative to `https://docs.docker.com`. Any page is also available
as Markdown at `<path without trailing slash>.md`.

## AI and agents

| Product | Aliases and terms users say | Section |
| --- | --- | --- |
| Docker Sandboxes | `sbx`, sandbox, microVM sandbox, local sandbox, "run Claude/Codex in a sandbox", sandbox policy or governance, `sbxenv.yaml` and `sbx env` environment files, `sbx mcp` sandbox MCP servers | `/ai/sandboxes/` |
| Cloud sandboxes | `sbx --cloud`, remote sandbox, "keep my agent running in the cloud" | `/ai/sandboxes/cloud/` |
| Sandboxes API and SDK | TypeScript SDK, REST API, create sandboxes programmatically | `/ai/sandboxes-api/` |
| Docker Agentic Platform | Agentic Platform, Console, cloud kits | `/agentic-platform/` |
| Docker Agent | `docker agent`, `cagent`, `agent.yaml`, multi-agent team | `/ai/docker-agent/` |
| MCP Catalog and Toolkit | MCP Toolkit, MCP Gateway, `docker mcp`, MCP profiles | `/ai/mcp-catalog-and-toolkit/` |
| Docker Model Runner | DMR, `docker model`, local LLMs, models in Compose | `/ai/model-runner/` |
| Gordon | Docker AI, "Ask Gordon", the assistant in Docker Desktop | `/ai/gordon/` |
| Docker Skills | this skill catalog, installing Docker skills into an agent | `/ai/skills/` |

`sbx` is the Docker Sandboxes CLI for both local and cloud sandboxes. Local
and cloud sandboxes use separate secret stores and policy sources, so check
the cloud section before you carry a local answer over to cloud.

## Application development

| Product | Aliases and terms users say | Section |
| --- | --- | --- |
| Docker Desktop | Desktop, settings, Docker Desktop for Mac/Windows/Linux, extensions, Enhanced Container Isolation, Settings Management | `/desktop/` |
| Docker Engine | `dockerd`, daemon, networking, storage, logging, rootless, Swarm | `/engine/` |
| Docker Build | BuildKit, Buildx, Bake, build cache, build checks, Dockerfile | `/build/` |
| Docker Build Cloud | cloud builders, remote builds | `/build-cloud/` |
| Docker Compose | `compose.yaml`, `docker compose`, Compose Bridge | `/compose/` |
| Docker Offload | `docker offload`, run containers in the cloud from Desktop | `/offload/` |
| Testcontainers | integration tests with real dependencies, Testcontainers Cloud | `/testcontainers/` |

## Supply chain security

| Product | Aliases and terms users say | Section |
| --- | --- | --- |
| Docker Hardened Images | DHI, hardened base image, DHI migration, image mirroring | `/dhi/` |
| Docker Scout | `docker scout`, CVEs, SBOM, policy evaluation | `/scout/` |
| Docker Hub | repositories, rate limits, pull usage, official images | `/docker-hub/` |

The search tool can return per-image DHI guides as Docker-maintained
`catalog` sources on GitHub. Cite them as DHI catalog guides, not as Docker
Docs pages.

## Accounts, administration, and billing

| Area | Aliases and terms users say | Section |
| --- | --- | --- |
| Accounts and organizations | Docker ID, Docker Home, admin console, org, company, members | `/accounts/` |
| Security and access | SSO, SCIM, roles, personal and org access tokens, 2FA | `/security/` |
| Subscriptions and billing | plans, seats, Pro, Team, Business, invoices | `/subscription-billing/` |

Answer plan, price, seat, and entitlement questions only from a fetched page,
and say when the docs leave something unestablished.

## References and release notes

CLI, API, and file-format references are under `/reference/`, for example
`/reference/cli/docker/` and `/reference/cli/sbx/`. Most products have a
release notes page in their own section. Check it when a user reports
behavior that doesn't match the docs, or asks when something changed.
