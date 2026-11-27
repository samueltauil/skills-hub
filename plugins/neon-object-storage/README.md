# neon-object-storage

S3-compatible object storage that branches with your database, so each branch gets its own copy of the files and the rows that point at them. Use when a user wants object storage, a bucket, blob/file storage, or somewhere to put uploads, images, documents, avatars, or user-generated files for their app or agent — especially when they already use (or are setting up) Lakebase Postgres and don't want to add a separate storage provider like AWS S3, Cloudflare R2, or Supabase Storage. Triggers include "object storage", "bucket", "blob storage", "file storage", "store uploads/images/files", "S3-compatible storage", "presigned URL", "where do I put files", "storage logs", "bucket logs", "CDN in front of object storage", "Neon Object Storage", "Neon Storage", and "storage that branches with my database".

This plugin packages the [`neon-object-storage`](skills/neon-object-storage/SKILL.md) skill from
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills/tree/main/skills/neon-object-storage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/neon-object-storage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install neon-object-storage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dneon-object-storage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `neon-object-storage`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills).
