# Identity and Access

**Goal:** explain who can act, what they can do, and where the permission applies.
Start with [the first application](00-landscape.md) if these terms are new.

An **identity** represents a person or a workload. Authentication establishes that identity;
authorization decides whether its request is permitted. A **principal** is the identity making
a request. A **scope** is the resource or collection to which a grant applies.

## Same Word, Different Object

<!-- diagram: role -->

The nearest translation runs the other way from the name: an Azure or Google role is closest to
an **AWS managed policy**, and an AWS role is closest to a **service principal or service
account**. The categories match; the trust and credential mechanisms do not.
[AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) ·
[Azure](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions) ·
[Google](https://docs.cloud.google.com/iam/docs/roles-overview)

## Directory Administration Is Not Workload Access

| Provider | Directory or workforce administration | Access to cloud resources |
| --- | --- | --- |
| AWS | IAM Identity Center administration | Permission sets grant access through roles in target accounts |
| Azure | Microsoft Entra directory roles | Azure role-based access control (RBAC) assignments |
| Google Cloud | Workspace or Cloud Identity super administrator | Organization and resource IAM roles |

For Azure, Global Administrator does not itself grant access to virtual machines. An elevated
administrator receives User Access Administrator at root scope and can assign the needed resource
roles. For Google, Organization Administrator manages organization IAM; it is not unrestricted
access to all workloads. Keep recovery administration separate from routine work.
[AWS workforce access](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html),
[Azure elevation](https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin),
[Google separation of duties](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization).

## How to Evaluate an AWS Request

First identify the principal, resource, account relationship, action, and applicable policies.
Identity and resource policies can grant access; boundaries and organization policies constrain
it. An applicable explicit deny overrides an allow. The interaction depends on context, so a
single six-step “every layer must allow” rule is misleading.
[AWS evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).

### Worked decision: an identity grant constrained by a boundary

Assume an IAM user requests `s3:PutObject`. Its identity policy allows that action, but its
permissions boundary allows only `s3:GetObject`. There is no resource-policy grant and no other
policy grants or restrictions in this example. **Denied:** the identity grant is limited by
the boundary. Adding another identity allow does not expand the boundary.

### Worked decision: a same-account resource grant

Assume an S3 bucket policy grants `s3:GetObject` directly to an IAM user's ARN in the same account.
The user's identity policy and boundary omit that action, but neither explicitly denies it.
No other applicable control restricts the request. **Allowed:** this kind of direct resource
grant is not limited by those implicit denies. Naming a role ARN instead changes the analysis.
[AWS boundary and principal rules](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html).

These are deliberately bounded examples, not advice to use IAM users for application credentials.
For real requests also consider cross-account access, session policies, organization controls,
resource-specific settings, conditions, and explicit denies.

## Inherited Grants in Azure and Google Cloud

Assigning a smaller role at a child resource does not subtract a grant inherited from its parent.
An Azure Reader assignment on a resource group does not reduce a subscription-level Contributor
grant. In Google Cloud, a project-level Viewer grant does not reduce inherited Editor access.
Deny controls and conditions can restrict effective access; changing an allow grant alone is
not the same operation. Configuration governance (Azure Policy or Google Organization Policy)
answers a separate question from who may perform an operation.
[Azure access model](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview),
[Google resource hierarchy](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control),
[Google deny policies](https://docs.cloud.google.com/iam/docs/deny-overview).

## Give the Application an Identity

| Workload | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Virtual machine | IAM role through an instance profile | Managed identity | Attached service account |
| Container application | ECS task role | Managed identity | Service identity on Cloud Run |
| Kubernetes workload | EKS Pod Identity or workload federation | Microsoft Entra Workload ID | Workload Identity Federation for GKE |

An Azure system-assigned managed identity follows the resource lifecycle; a user-assigned identity
is independent and can be shared. A Google service account is both an identity and a resource:
permission to attach or impersonate it differs from the permissions it exercises. Prefer attached
identities or federation to distributing long-lived keys, where the workload supports them.
[AWS instance profiles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html),
[Azure managed identities](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview),
[Google service accounts](https://docs.cloud.google.com/iam/docs/service-account-overview).

## Check Your Understanding

A photo service needs to create objects in one bucket. Does giving it an organization-wide
administrator role solve the problem well?

<details><summary>Answer and reasoning</summary>

It may grant sufficient access, but it grants far more than the task needs. Give the workload
an identity and an object-creation permission at the appropriate resource scope. Check whether
it also needs to read, overwrite, or delete objects before adding those permissions. A role's
name is not evidence that its permissions fit the task.

</details>

**Next:** [networking](03-networking.md) · [compare identity mappings](02-identity.md) ·
[practice scenarios](practice.md).

<!-- This document follows common-doc-guidelines.md. -->
