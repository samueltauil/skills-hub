# google-cloud-storage-basics

Stores, retrieves, and manages data as objects in Cloud Storage on Google Cloud (also known colloquially as GCS) buckets. Use when you need to interact with Cloud Storage — set up a Storage MCP server (remote or local Toolbox), create or configure buckets, upload, download, stream, or transfer data, organize objects with folders, generate signed URLs, control access (IAM, ACLs, public access prevention), set storage classes (Standard, Nearline, Coldline, Archive), manage lifecycle and cost, protect data (versioning, CMEK, retention, Bucket Lock, holds, soft delete), host static websites, trigger Pub/Sub notifications, mount buckets (gcsfuse), or optimize performance. Covers gcloud storage / gsutil, JSON/XML APIs, client libraries, Terraform, and Cloud Storage MCP servers. Don't use for generic MCP setup that doesn't mention Cloud Storage, other MCP servers, block storage (Persistent Disk), BigQuery, or databases (Cloud SQL, Spanner, Bigtable, Firestore).

This plugin packages the [`google-cloud-storage-basics`](skills/google-cloud-storage-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-storage-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-storage-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-storage-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-storage-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-storage-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
