# Verification Runbook for serving, sharing, and evaluating

## 1. A server binds where and how you intend
```bash
docker agent serve mcp ./agent.yaml --http --listen 127.0.0.1:9090 --auth-token "$TOKEN" &
sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9090/         # no token
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $TOKEN" http://127.0.0.1:9090/
```
Pass: the process reports it is listening on the given address; the request
without the bearer token is rejected (non-2xx, typically 401), and the
request with the correct token succeeds. Fail: it starts on a non-loopback
address without `--auth-token`/`--insecure-no-auth` set explicitly, or the
unauthenticated request succeeds — stop it, add/fix authentication, and
restart.

## 2. A pushed agent round-trips
```bash
docker agent share push ./agent.yaml docker.io/<user>/<name>:<tag>
docker agent share pull docker.io/<user>/<name>:<tag> --force
docker agent debug config docker.io/<user>/<name>:<tag>
```
Pass: the pulled config's resolved form matches the original (including any
`instruction_file` contents, now inlined). Fail: a resolution error or
missing instruction content — check for `instruction_file` paths outside the
config directory, which are rejected on push.

## 3. Evals run and produce a report
```bash
docker agent eval ./agent.yaml ./evals
```
Pass: console summary shows per-eval pass/fail plus Tool Calls / Relevance /
Size / Assertions metrics, and a `results/` directory with JSON, `.db`, and
log files. Fail: "No model is currently available" inside the eval
container — use `docker-agent-run` for local credential/model troubleshooting,
then check the eval-specific boundary: credentials must be set in the invoking
shell. Dedicated model keys are forwarded automatically; `GITHUB_TOKEN`/`GH_TOKEN`
are not — pass the one your provider needs explicitly (e.g. `-e GITHUB_TOKEN`).

## 4. A regression gate actually gates
```bash
docker agent eval ./agent.yaml --baseline results/<prior-run>.json --regression-tolerance 0.05
```
Pass: exit code 0 when quality is within tolerance of the baseline, non-zero
when a previously-passing eval now fails or an aggregate rate drops beyond
tolerance. Fail (gate never fails): confirm the baseline file actually
contains evaluations — a baseline or run with none is rejected, not treated
as passing.
