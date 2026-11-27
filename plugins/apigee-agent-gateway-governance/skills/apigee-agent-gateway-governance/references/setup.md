# Environment setup before you start

Everything here is a prerequisite the skill does **not** create. Work through
it once per project; `scripts/assess_integration.sh` checks the Apigee and
gateway side afterwards, but it cannot check your local toolchain or whether
billing is attached.

## Contents

-   [1. Install the Google Cloud SDK](#1-install-the-google-cloud-sdk): lines 19-35
-   [2. Select the project](#2-select-the-project): lines 36-48
-   [3. Attach a billing account](#3-attach-a-billing-account): lines 49-69
-   [4. Enable the APIs](#4-enable-the-apis): lines 70-106
-   [5. Pick the region, once](#5-pick-the-region-once): lines 107-127
-   [6. Authenticate](#6-authenticate): lines 128-153
-   [7. IAM roles](#7-iam-roles): lines 154-180
-   [8. What the skill still needs from you](#8-what-the-skill-still-needs-from-you): lines 181-189

## 1. Install the Google Cloud SDK

The skill drives `gcloud` throughout and several steps have no `gcloud`
equivalent, so it also calls the Apigee REST API with a token minted by
`gcloud`.

-   [Install the gcloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk.md.txt)

Version **588.0.0 or later** is required: `gcloud apigee apis import
--from-template` is GA only from 588. `assess_integration.sh` checks this and
warns if the installed version is older.

```bash
gcloud version
gcloud components update
```

## 2. Select the project

```bash
gcloud config set project PROJECT_ID
```

The skill takes `project` from the input file in prod mode and from this
setting or the conversation in dev mode. One project holds the gateway, the
VPC and the network attachment. Apigee may live in **a different project** —
the callout reaches it over PSC — but the region must match (see 5).

-   [Create and manage projects](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects.md.txt)

## 3. Attach a billing account

The project must have an **active billing account**. Apigee, Agent Gateway and
Vector Search are all billable, and a project without billing fails partway
through the build rather than up front — typically at the Apigee environment
or the index deploy, after earlier steps have already created resources.

```bash
gcloud billing projects describe PROJECT_ID
```

-   [Enable, disable or change billing for a project](https://docs.cloud.google.com/billing/docs/how-to/modify-project.md.txt)
-   For what each component costs, see the published pricing pages rather than
    any figure quoted in a skill: [Google Cloud pricing](https://cloud.google.com/pricing)

Only one resource in this skill bills **continuously whether or not traffic
flows**: a deployed Vector Search index, used by the semantic cache. It is
off by default, disclosed before it is created, and
`scripts/teardown_vector_search.sh` removes it in the order that does not
fault live traffic.

## 4. Enable the APIs

Base set, always needed:

```bash
gcloud services enable \
  apigee.googleapis.com \
  networkservices.googleapis.com \
  networksecurity.googleapis.com \
  compute.googleapis.com \
  dns.googleapis.com \
  --project PROJECT_ID
```

| API | Used for |
| --- | --- |
| `apigee.googleapis.com` | the environment, envgroup, proxy and deployment |
| `networkservices.googleapis.com` | the Agent Gateway and the AuthzExtension |
| `networksecurity.googleapis.com` | the AuthzPolicy that routes traffic to the callout |
| `compute.googleapis.com` | the network attachment, PSC endpoint and subnet checks |
| `dns.googleapis.com` | the private zone and A record for the callout hostname |

Per feature, only if you enable it:

```bash
# semantic cache -- Vector Search index and index endpoint
gcloud services enable aiplatform.googleapis.com --project PROJECT_ID

# Model Armor prompt screening
gcloud services enable modelarmor.googleapis.com --project PROJECT_ID
```

`aiplatform.googleapis.com` is also what the agent itself runs on, so it is
usually already enabled in a project that has a working agent.

-   [Enabling and disabling services](https://docs.cloud.google.com/service-usage/docs/enable-disable.md.txt)

## 5. Pick the region, once

**The Agent Gateway, the subnet and the Apigee runtime instance must all be in
the same region.** This is the constraint most likely to force a rebuild,
because an Apigee instance's region is fixed at creation.

```bash
gcloud config set compute/region REGION
```

Choose a region where **both** Apigee and Agent Gateway are available —
availability differs by product, so check before committing:

-   [Google Cloud locations](https://docs.cloud.google.com/about/locations.md.txt)
-   [Apigee locations](https://docs.cloud.google.com/apigee/docs/locations.md.txt)

This skill has been exercised in `us-west1` and `us-east1`. Preview features
are often restricted to `us-central1` or `global`, so if you are enabling
something still in preview, confirm it is offered in the region you picked
rather than assuming the general default.

## 6. Authenticate

Two credentials, for two different callers.

```bash
# for gcloud itself
gcloud auth login

# for the REST calls the scripts make, and for client libraries
gcloud auth application-default login
```

The scripts deliberately use **Application Default Credentials** for the
Apigee REST API. On some organizations a plain `gcloud auth
print-access-token` is rejected by `apigee.googleapis.com` with
`401 UNAUTHENTICATED / ACCESS_TOKEN_TYPE_UNSUPPORTED`; ADC is not. If you make
ad-hoc `curl` calls alongside the scripts, use ADC for those too:

```bash
TOKEN=$(gcloud auth application-default print-access-token)
```

For an unattended or CI run, use a service account instead:

-   [Service account credentials](https://docs.cloud.google.com/iam/docs/service-account-creds.md.txt)

## 7. IAM roles

The identity running the skill needs, at minimum:

| Role | Why |
| --- | --- |
| `roles/apigee.admin` | create the environment, envgroup, proxy and deployment |
| `roles/compute.networkAdmin` | network attachment, PSC endpoint, subnet reads |
| `roles/dns.admin` | the private zone and A record |
| `roles/networkservices.agentGatewayUser` | read and modify the Agent Gateway |
| `roles/networkservices.serviceExtensionsAdmin` | create the authorization extension |
| `roles/networksecurity.admin` | create the authorization policy that attaches it |

Feature-specific, and granted to the **proxy's** service account rather than
to you:

| Role | Why |
| --- | --- |
| `roles/aiplatform.user` | the semantic cache calls Vector Search |
| `roles/modelarmor.user` | Model Armor prompt screening |

Granting a role to a service account is a **sensitive operation**: it widens
what the deployed proxy can reach. Review the grant before applying it, and
prefer a dedicated service account for the proxy over the Compute default.

-   [Understanding IAM roles](https://docs.cloud.google.com/iam/docs/roles-overview.md.txt)

## 8. What the skill still needs from you

Three things it never creates, checked by `assess_integration.sh`:

-   **An Agent Gateway.** This skill attaches to one; it does not create one.
-   **An agent whose traffic actually routes through that gateway.** On Agent
    Runtime that is set with `agent_gateway_config` at agent **creation** time
    and cannot be added afterwards.
-   **An Apigee org with a runtime instance in the gateway's region.**
