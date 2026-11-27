# Verification runbook for Docker docs retrieval

This runbook is manual and has not been executed by CI. It checks that the
retrieval paths in `SKILL.md` still behave as described. The checks are
read-only, need no credentials, and create one temporary file. Use a shell
with `curl` and `jq` and HTTPS access to `ai-backend-service.docker.com` and
`docs.docker.com`.

```bash
MCP_URL=https://ai-backend-service.docker.com/mcp
WORK=$(mktemp -d)
```

## 1. The MCP server lists the docs search tool

```bash
curl -fsS -X POST "$MCP_URL" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | jq -r '.result.tools[] | "\(.name) \(.inputSchema.required)"'
```

Pass: the output lists `search_docker_docs` with the required argument
`["message"]`. If the name changed, update `SKILL.md` and the
`compatibility` field.

## 2. A search returns sourced documents

```bash
TOOL=$(curl -fsS -X POST "$MCP_URL" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | jq -r '.result.tools[0].name')
jq -n --arg tool "$TOOL" \
  '{jsonrpc:"2.0",id:2,method:"tools/call",params:{name:$tool,arguments:{message:"sbx policy allow network"}}}' \
  | curl -fsS -X POST "$MCP_URL" \
      -H 'Content-Type: application/json' \
      -H 'Accept: application/json, text/event-stream' \
      --data-binary @- \
  | jq -r '.result.content[0].text | fromjson | .documents[].metadata | "\(.source_type) \(.source)"'
```

Pass: at least one line starts with `docs https://docs.docker.com/ai/sandboxes/`.

## 3. llms.txt and the page index are reachable

```bash
curl -fsS https://docs.docker.com/llms.txt | grep -E '^## (Primary sections|Product documentation)'
curl -fsS https://docs.docker.com/llms-full.txt -o "$WORK/llms-full.txt"
grep -c '^Markdown: ' "$WORK/llms-full.txt"
```

Pass: both section headings print, and the index has more than 1,000
`Markdown:` entries.

## 4. Pages are served as Markdown both ways

```bash
curl -fsS -o /dev/null -w '%{content_type}\n' https://docs.docker.com/ai/sandboxes.md
curl -fsS -o /dev/null -w '%{content_type}\n' -H 'Accept: text/markdown' https://docs.docker.com/ai/sandboxes/
curl -fsS -o /dev/null -w '%{content_type}\n' https://docs.docker.com/ai/sandboxes/
```

Pass: the first two print `text/markdown`, and the third, without the header,
prints `text/html`.

## 5. Product map paths resolve

```bash
grep -oE '`/[a-z0-9/._-]+/`' skills/docker-docs/references/product-map.md \
  | tr -d '`' | sort -u \
  | while read -r path; do
      code=$(curl -sS -o /dev/null -w '%{http_code}' "https://docs.docker.com$path")
      [ "$code" = 200 ] || echo "$code $path"
    done
```

Run this from the repository root. Pass: no output. Fix any path that
reports a redirect or 404 in `references/product-map.md`.

## Cleanup

```bash
rm -rf "$WORK"
```
