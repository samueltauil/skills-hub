# Networking

There are **two** network legs, and they fail for different reasons.

```
  agent  ──(1) client leg──▶  Agent Gateway  ──(2) callout leg──▶  Apigee
                                                                    proxy
```

-   **Leg 2, gateway → Apigee**, is the one this skill builds. It is self-serve
    and covered below.
-   **Leg 1, agent → gateway**, is a *prerequisite you do not build by hand*.
    Get it wrong and every other thing on this page still passes while no
    traffic ever arrives. Read "The client leg" at the bottom before you start.

## Contents

-   [Leg 2 — gateway to Apigee (the callout)](#leg-2-gateway-to-apigee-the-callout): lines 26-36
-   [Prerequisites](#prerequisites): lines 37-51
-   [Find the service attachment](#find-the-service-attachment): lines 52-60
-   [Reserve the IP and create the endpoint](#reserve-the-ip-and-create-the-endpoint): lines 61-80
-   [Private DNS](#private-dns): lines 81-94
-   [Order of operations](#order-of-operations): lines 95-101
-   [Leg 1 — the client leg (agent to gateway)](#leg-1-the-client-leg-agent-to-gateway): lines 102-227

## Leg 2 — gateway to Apigee (the callout)

The gateway egresses into your VPC, resolves the callout host on a private DNS
zone, and reaches the Apigee runtime through a PSC endpoint pointed at the
Apigee instance's service attachment.

```
CALLOUT_HOST  --A-->  PSC IP  -->  forwarding rule  -->  Apigee instance
                                                          serviceAttachment
```

## Prerequisites

-   The Agent Gateway needs an **egress `networkAttachment`** into the VPC, and
    a **`dnsPeeringConfig`** exposing your private domain to it. Without the
    peering the host does not resolve from the gateway and nothing else matters.
    This one the skill can supply: `scripts/ensure_gateway_connectivity.sh`
    creates the attachment and adds both to the gateway, gated on
    `gateway.manageNetworkConfig` and on the user confirming the diff. See
    workflow step 0 in `SKILL.md`.
-   Your project must be in the Apigee instance **`consumerAcceptList`** or the
    PSC connection never reaches `ACCEPTED`.
-   The gateway calls the ext-proc as its own Google-managed
    `serviceExtensionsServiceAccount`
    (`service-<num>@gcp-sa-dep.iam.gserviceaccount.com`).

## Find the service attachment

No `gcloud` equivalent; read it off the instance.

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://apigee.googleapis.com/v1/organizations/$ORG/instances"
```

## Reserve the IP and create the endpoint

```bash
gcloud compute addresses create agent-gateway-callout-psc-ip \
  --region=$REGION --subnet=$SUBNET --purpose=GCE_ENDPOINT --project=$PROJECT

gcloud compute forwarding-rules create agent-gateway-callout-psc-endpoint \
  --region=$REGION --network=$NETWORK --address=agent-gateway-callout-psc-ip \
  --target-service-attachment=$APIGEE_INSTANCE_SERVICE_ATTACHMENT \
  --project=$PROJECT
```

Confirm `pscConnectionStatus=ACCEPTED` before going further.
`--purpose=GCE_ENDPOINT` is verified — it is the correct value for this
endpoint.

Acceptance here is automatic *provided your project is on the instance's*
`consumerAcceptList`. This is the one PSC endpoint in the setup that you can
expect to reach `ACCEPTED` on your own; contrast the client leg below.

## Private DNS

```bash
gcloud dns managed-zones create $ZONE --dns-name=$DOMAIN \
  --visibility=private --networks=$NETWORK --project=$PROJECT

gcloud dns record-sets create $CALLOUT_HOST. --type=A --ttl=300 \
  --rrdatas=$PSC_IP --zone=$ZONE --project=$PROJECT
```

The A record name must be exactly the envgroup hostname and the AuthzExtension
`authority`. Check all three against each other before you conclude anything
else is broken.

## Order of operations

Environment property → build and deploy the proxy → envgroup host, DNS and PSC
(`ACCEPTED`) all in place → **then** the AuthzExtension → then the AuthzPolicy →
then traffic. The AuthzExtension is inert until the host resolves and the proxy
is deployed, so creating it early tells you nothing.

## Leg 1 — the client leg (agent to gateway)

**Where the agent runs decides whether this works at all.** This is a
prerequisite, not a step: nothing here is built with the commands above, and
getting it wrong is silent — leg 2 stays green and no traffic arrives.

Reference:
[Route traffic through Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy.md.txt),
[Set up VPC connectivity](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/set-up-vpc-connectivity.md.txt),
and
[Delegate authorization](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/delegate-authorization.md.txt).

### Use Agent Runtime

Agent Runtime is the supported path and the only self-serve one. Pass
`agent_gateway_config` at creation and the orchestrator builds the PSC endpoint,
routing, DNS and certificate trust for you:

```python
import agentplatform

client = agentplatform.Client(project=PROJECT, location=LOCATION)
client.runtimes.create(
    agent=adk_app,
    config={
        "staging_bucket": "gs://…",
        "requirements": ["google-cloud-aiplatform[agent_engines,adk]>=2.1,<3", "google-adk>=2.9,<3"],
        "agent_gateway_config": {
            "agent_to_anywhere_config": {"agent_gateway": AGENT_GATEWAY_RESOURCE},
        },
        "identity_type": "AGENT_IDENTITY",
        # Required. Without it every invocation 401s -- see below.
        "env_vars": {
            "GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES": "False",
        },
        # Required if the agent carries any custom class -- see below.
        "extra_packages": ["my_agent_pkg"],
    },
)
```

**`env_vars` is not optional here.** Omit it on a gateway-attached agent built
recently and *every* invocation fails, before any user code runs, with a
`400 INVALID_ARGUMENT` wrapping a `401 UNAUTHENTICATED` on the agent's own
`sessions.create`. Both conditions are needed — attached to a gateway, and a
recent build — which is why an older agent on the same gateway keeps working
and makes the new one look like a code problem. The deploy succeeds and the
engine reports healthy, so it stays invisible until the first request. Set the
variable explicitly rather than relying on the platform default, which has
already moved once.

The trap is where the symptom points: it is a 401 on a model call, so the first
suspect is the Apigee proxy you were just told to build. It is not. Rule this
out before debugging anything on the Apigee side.

**`extra_packages` matters as soon as the agent is non-trivial.** A plain
`Agent` is pickled by value and needs nothing. An agent carrying a custom class
is pickled by *reference*, and the remote cannot import it:

```
ModuleNotFoundError: No module named 'my_agent_pkg'
UserCodeControlPlaneError: Control plane operation failed due to user code
```

The create then fails and the engine is rolled back, so no resource is left to
pull logs from — diagnosis means searching Cloud Logging by resource type
alone. Name the package at create time instead. Drop the line only for an agent
with no custom classes.

Use `agentplatform`, not `vertexai`: `vertexai.Client` is deprecated and warns
(`Please use agentplatform.Client instead`), and `client.agent_engines` is
renamed `client.runtimes`. Both ship inside `google-cloud-aiplatform`, and
`agent_gateway_config` / `identity_type` are unchanged across the rename.

`AGENT_GATEWAY_RESOURCE` is the full
`projects/{p}/locations/{r}/agentGateways/{name}`. There is no `gcloud` surface
for Agent Runtime — no `agent-engines` group on any track — so this is SDK only.

**Grant the Vertex AI service agent read access to the gateway first.** It
resolves the gateway on your behalf, and without it creation fails at once with
a `400 FAILED_PRECONDITION`: *"Permission denied to get Agent Gateway … Please
ensure Vertex AI Service Agent has `networkservices.agentGateways.get`
permission on the gateway project."* The error suggests waiting for propagation,
which sends you off to wait for something that will never arrive if the binding
simply is not there.

```bash
gcloud projects add-iam-policy-binding $GATEWAY_PROJECT \
  --member="serviceAccount:service-$PROJECT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com" \
  --role="roles/networkservices.viewer"
```

`roles/networkservices.viewer` is the narrowest predefined role carrying that
permission — the `agentGatewayUser` and `agentGatewayViewer` roles do **not**
include it, despite the names.

### A GCE VM will never work

The supported compute is GKE or Cloud Run — there is no GCE. The egress guide is
explicit that the gateway is only compatible with Cloud Run in **ambient
networking** mode (`--ambient-networking=regional`, `--vpc-egress=all-traffic`,
plus an env var installing the SWP TLS-inspection root cert). Do not spend time
on a VM; it is a dead end.

### Do not hand-build the consumer PSC endpoint

The gateway's client entry point is an **mTLS PSC service attachment in a Google
tenant project**. You can create a consumer forwarding rule to it, and it will
sit at `PENDING` forever: acceptance requires an internal
`References.CreateReference` call that gcloud does not expose. A `PENDING`
endpoint presents as TCP 443 simply closed, which reads like a firewall problem
and is not.

Raw Cloud Run is possible but is explicitly "the hard way": it additionally
needs a catch-all Cloud DNS response policy, a `ClientTlsPolicy`, a
`BackendService` onto the gateway attachment, and project-level `HTTPRoute` and
`TCPRoute` — resources that require a reserved `aersvd-` name prefix that
Traffic Director only lets specific P4SAs create. Treat it as not self-serve.

### Known limits

Agent Gateway governs agents **running on GCP only** (Agent Runtime, Gemini
Enterprise). Agents outside GCP are unsupported until a public endpoint ships.
Self-signed-cert destinations are also unsupported, and PSC automation and DNS
service binding are not yet available — which is why leg 2's network attachment
and DNS peering are built by hand above.
