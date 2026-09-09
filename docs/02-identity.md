# Identity and Access

Candidates report this as the hardest area on both the Google Associate Cloud Engineer exam,
where service account edge cases bite, and on Azure AZ-104, where scope inheritance bites. It
is also where the vocabulary collides most violently. Budget more time here than anywhere else.

## The One Structural Difference

**AWS attaches permissions to things. Azure and Google Cloud grant permissions at a place.**

In AWS, a policy document is attached to an identity or to a resource. The document itself
names actions, resources, and conditions. Permissions travel with the attachment.

In Azure and Google Cloud, you make a three-part statement: *this principal* has *this role* at
*this scope*, and everything below that scope inherits it. The role is just a named bag of
permissions; it carries no information about where it applies until you assign it.

That difference explains most of the confusion below.

## Role Is the Worst Word in Cloud Computing

| | AWS IAM role | Azure role | Google Cloud role |
| --- | --- | --- | --- |
| What kind of thing is it? | **An identity** | **A permission set** | **A permission set** |
| Does it have credentials? | Yes, temporary ones issued by STS | No | No |
| Can something "be" it? | Yes, you assume it and become it | No, you are granted it | No, you are granted it |
| Does it say who may use it? | Yes, in its trust policy | No, the assignment does | No, the binding does |
| Closest analogue elsewhere | Google service account, roughly | AWS managed policy | AWS managed policy |

Read that first row again. An AWS role is a thing you *become*, with its own temporary access
keys. An Azure or Google role is a *list of verbs* that gets pinned to somebody else. They are
not the same category of object, and a question that says "assign a role" means something
different depending on which logo is in the corner.

The nearest AWS equivalent of an Azure or Google role is an **IAM managed policy**. The nearest
Azure or Google equivalent of an AWS role is a **service principal** or **service account**.

## The Building Blocks Mapped

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Identity service | IAM, plus IAM Identity Center for the organization | Microsoft Entra ID | Cloud Identity, or Google Workspace |
| Human identity | IAM user, or federated identity | Entra ID user | Google account |
| Group | IAM group | Entra ID group | Google group |
| Machine identity | IAM role | Managed identity, backed by a service principal | Service account |
| Application registration | IAM role with a trust policy | App registration plus service principal | Service account, or OAuth client |
| Named permission set | Managed policy | Role definition | Role |
| Granting act | Attach policy | Role assignment | IAM binding, inside an allow policy |
| Where grants apply | Attachment target | Scope, inherited downward | Resource node, inherited downward |
| Organization-wide guardrail | Service control policy, resource control policy | Azure Policy, plus deny assignments | Organization policy constraints, plus deny policies |
| Break-glass superuser | Root user | Global Administrator, after elevation | Organization Administrator |

## Azure Has Two Separate Role Systems

This trips up nearly everyone, and Microsoft's own naming does not help.

| | Microsoft Entra roles | Azure RBAC roles |
| --- | --- | --- |
| Govern | The identity tenant: users, groups, app registrations, licences | Azure resources: virtual machines, storage, networks |
| Examples | Global Administrator, User Administrator, Application Administrator | Owner, Contributor, Reader, Virtual Machine Contributor |
| Scope | The tenant, or an administrative unit | Management group, subscription, resource group, resource |
| Assigned in | Entra ID | Azure Resource Manager |

A Global Administrator does **not** automatically have access to Azure resources. They must
first elevate to User Access Administrator at the root management group. Being the most
powerful identity administrator and having no rights over a virtual machine is a real and
intentional state, and exam questions use it.

Neither AWS nor Google Cloud splits identity administration from resource administration this
way.

## Evaluation Order, Which Decides the Answer

### AWS

Evaluated in this order, and the first decisive result wins:

1. **Explicit deny** anywhere. Always final. Nothing overrides it.
2. **Service control policies** and resource control policies. These set a ceiling for the
   account. An SCP never grants anything; it only limits what may be granted.
3. **Resource-based policies**, such as an S3 bucket policy.
4. **Permissions boundaries**, which cap what an identity policy can grant.
5. **Session policies**, passed when a role is assumed.
6. **Identity-based policies**.

Anything not allowed is denied. The mental shortcut: **a permission must survive every layer,
and any single explicit deny kills it.**

The SCP point is the one most often misread. An SCP attached to an organizational unit does not
give anyone permission. If the SCP allows an action and no IAM policy grants it, the answer is
still no. Also worth knowing: when SCPs are enabled, **every entity must have at least one SCP
attached at all times**, and the last one cannot be removed.

### Azure

1. **Deny assignments** are checked first and win. They are rare and mostly created by managed
   applications and Azure Blueprints rather than by hand.
2. **Role assignments** are then combined. RBAC is **additive**: the effective permission set is
   the union of everything assigned at the resource and every scope above it.
3. **Azure Policy** is evaluated separately, at resource-write time, and a policy with a `deny`
   effect will block a deployment that RBAC would have permitted.

The trap: RBAC and Azure Policy are different systems answering different questions. RBAC
answers "may this principal act?". Azure Policy answers "is this resource configuration
permitted?". A question about enforcing that all storage accounts use a particular redundancy
setting is an Azure Policy question, and every RBAC answer offered is a distractor.

There is no Azure equivalent of an AWS permissions boundary.

### Google Cloud

1. **Deny policies** are evaluated before allow policies and take precedence.
2. **Allow policies** are combined and are **additive** up the hierarchy: a binding at the
   organization applies to every folder, project, and resource beneath it.
3. **Organization policy constraints** are separate and restrict what configurations are
   permitted, regardless of IAM.

Two things that surprise AWS engineers:

- **You cannot subtract a permission by granting a narrower role lower down.** Inheritance is
  purely additive. If somebody has Editor at the folder, giving them Viewer on one project
  inside it changes nothing. To reduce access you must remove the higher binding. AWS engineers
  reach for an explicit deny, and until deny policies existed there was no such thing.
- **Basic roles are wider than they look.** Owner, Editor, and Viewer predate the granular
  roles and span every service in the project. Editor can delete most resources. Any answer
  proposing a basic role in a production or least-privilege scenario is almost always wrong;
  the intended answer is a predefined role.

## Machine Identity: How Compute Gets Credentials

| | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Virtual machine | IAM role, attached through an **instance profile** | Managed identity, system-assigned or user-assigned | Service account attached to the instance |
| Container task | ECS task role | Managed identity on the container app | Service account on the workload |
| Kubernetes pod | IAM Roles for Service Accounts, or EKS Pod Identity | Microsoft Entra Workload ID | Workload Identity Federation for GKE |
| Function | Lambda execution role | Managed identity on the function app | Service account on the function |
| From outside the cloud | IAM Roles Anywhere, or OIDC federation | Workload identity federation | Workload Identity Federation |

Notes that decide questions:

- The **instance profile** is a container for an IAM role that exists purely so EC2 can attach
  one. In the console it is created invisibly, which is why many people have never heard of it
  and then meet it in a command-line question.
- Azure's **system-assigned** managed identity is tied to one resource and dies with it.
  A **user-assigned** managed identity is a standalone resource that survives and can be shared
  across several resources. "Should outlive the virtual machine" or "shared by several apps"
  selects user-assigned every time.
- A Google **service account is both an identity and a resource**. You grant it roles, and you
  also grant other people roles *on* it. That second part is the edge case candidates report
  failing. Being able to use a service account requires a role on the service account itself,
  typically Service Account User, which is separate from any permission that service account
  holds.
- **Never use service account keys** as an answer if any alternative is offered. Downloadable
  JSON keys are long-lived credentials and every modern exam treats them as the wrong choice
  where attached identities or federation are available.

## Federation and Single Sign-On

| Need | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Workforce SSO into the cloud | IAM Identity Center | Entra ID, natively | Cloud Identity, or Workforce Identity Federation |
| Corporate directory sync | AD Connector, or SCIM into Identity Center | Entra Connect | Google Cloud Directory Sync |
| Trust an external workload | IAM Roles Anywhere, OIDC provider | Workload identity federation | Workload Identity Federation |
| Customer-facing sign-in | Cognito | Entra External ID | Identity Platform |

IAM Identity Center was called AWS SSO, and material published before the rename still uses the
old name. Entra ID was called Azure Active Directory, and the same applies with much greater
volume, since the rename is recent enough that most third-party courses still say Azure AD.

## Least Privilege Under Exam Conditions

The pattern is nearly identical everywhere, which makes it easy marks.

1. Grant to a **group**, never to an individual, whenever a group is offered.
2. Prefer a **predefined or managed role** over a custom one; prefer a custom one over a broad
   built-in one.
3. Attach an identity to compute rather than distributing keys.
4. Grant at the **narrowest scope** that works. In Azure this means the resource group rather
   than the subscription. In Google Cloud it means the project rather than the folder.
5. Basic and owner-level roles are wrong answers unless the question explicitly asks for full
   administrative control.

## Drill

Cover the right-hand column.

| Question | Answer |
| --- | --- |
| Which cloud's "role" is an identity with credentials? | AWS |
| Something must outlive its virtual machine and be shared. Which Azure identity? | User-assigned managed identity |
| An SCP allows an action but no IAM policy grants it. Is it allowed? | No. SCPs limit, never grant |
| Google user has Editor at folder level, Viewer on one project. Effective access on that project? | Editor. Inheritance is additive and cannot be narrowed |
| Global Administrator wants to manage a virtual machine. What is missing? | Elevation to User Access Administrator; Entra roles are not Azure RBAC roles |
| Enforce that every storage account uses a given redundancy setting. RBAC or Azure Policy? | Azure Policy |
| What lets EC2 receive an IAM role? | An instance profile |
| Which single result always wins in AWS evaluation? | An explicit deny |

## Next

- [03-networking.md](03-networking.md), where the security-boundary vocabulary collides again.
- [09-confusing-terms.md](09-confusing-terms.md) for role, policy, and principal side by side.

<!-- This document follows common-doc-guidelines.md. -->
