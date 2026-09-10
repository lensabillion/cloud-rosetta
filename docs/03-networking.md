# Networking

Second only to identity as a source of lost marks. Three clouds use "firewall" for objects that
attach at different layers, evaluate in different orders, and default differently.

## The Network Container

| | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Name | VPC | Virtual network, VNet | VPC network |
| Scope | Regional | Regional | **Global** |
| Subnet scope | **One availability zone** | Regional, spans zones | Regional |
| Default on creation | A default VPC per region | None | A default VPC with auto-mode subnets in every region |
| Address planning | CIDR per VPC, then per subnet | Address space per VNet, then per subnet | Subnets carry the ranges; the VPC itself has none |

A Google VPC has no CIDR of its own; the subnets carry the ranges. Auto-mode VPCs create a subnet
in every region for you, which is convenient and almost always the wrong answer in a design
question, where custom mode is expected.

## Firewalling: The Big Divergence

<!-- diagram: firewall -->

| | AWS security group | AWS network ACL | Azure NSG | Google VPC firewall rule |
| --- | --- | --- | --- | --- |
| Attaches to | Network interface | Subnet | Subnet, network interface, or both | **The VPC network** |
| Stateful? | Yes | **No** | Yes | Yes |
| Deny rules? | **No, allow only** | Yes | Yes | Yes |
| Rule order | No order, all evaluated | Numbered, lowest first, first match wins | Priority number, lowest first, first match wins | Priority number, lowest first, first match wins |
| Selects targets by | Attachment | Attachment | Attachment | **Network tag or service account** |
| Default ingress | Deny | Allow, on the default ACL | Deny, after built-in rules | Deny, implied |
| Default egress | Allow | Allow, on the default ACL | Allow, after built-in rules | Allow, implied |

Four traps live in that table.

- **An AWS security group cannot deny.** Blocking one specific address is a network ACL job. This
  is the most reliably tested networking fact in the AWS catalogue.
- **A network ACL is stateless.** Allowing traffic in does not allow the reply out; return traffic
  needs its own rule on ephemeral ports. The symptom is traffic arriving and no response coming back.
- **Google rules have implied entries** that cannot be deleted: allow all egress, deny all ingress.
- **Azure NSGs can attach at both levels at once**, subnet then interface inbound and the reverse
  outbound. Traffic must pass both. Built-in rules sit above anything you write.

Note the acronym: an Azure **application security group** names a set of interfaces so NSG rules
can reference them by name. It has nothing to do with an AWS Auto Scaling group.

## Getting Traffic In and Out

| Function | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Inbound from internet | Internet gateway | Public IP on the resource | External IP on the resource |
| Outbound for private machines | NAT gateway, or NAT instance | NAT Gateway, or outbound rules on a load balancer | Cloud NAT |
| Outbound default | None until you build it | Historically implicit; explicit NAT now expected | None until you configure Cloud NAT |
| Static public address | Elastic IP | Public IP with Static allocation | Reserved static external IP |

Cloud NAT is worth a note: it is a software-defined feature of the network rather than an
instance in the data path, so there is no NAT appliance to size or place in a subnet. AWS NAT
gateways are per-zone resources, which means a zone-resilient design needs one per zone, and
that is a recurring cost and availability question.

## Connecting Networks Together

| Need | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Two networks, same cloud | VPC peering | VNet peering | VPC Network Peering |
| Many networks, hub topology | Transit Gateway | Virtual WAN, or hub-and-spoke with a firewall | Network Connectivity Center |
| Peering transitive? | **No** | **No** | **No** |
| Overlapping CIDRs allowed? | No | No | No |
| To on-premises, private circuit | Direct Connect | ExpressRoute | Cloud Interconnect, Dedicated or Partner |
| To on-premises, over internet | Site-to-Site VPN | VPN Gateway | Cloud VPN, HA VPN or Classic VPN |

Peering is non-transitive everywhere. If A peers with B and B peers with C, A cannot reach C, and
the answer is a transit construct: Transit Gateway, Virtual WAN, or Network Connectivity Center.

## Reaching Managed Services Privately

The worst naming in the subject, and Azure is the main offender.

| Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Private path to a first-party service | Gateway endpoint, for S3 and DynamoDB | Service endpoint | Private Google Access |
| Private IP inside your network for a service | Interface endpoint, powered by PrivateLink | **Private endpoint**, powered by Private Link | Private Service Connect |
| Publish your own service privately | PrivateLink endpoint service | Private Link service | Private Service Connect producer |

Azure's **service endpoint** and **private endpoint** sound like synonyms and are not:

- A **service endpoint** keeps traffic on the Microsoft backbone but the service keeps its
  public IP. Nothing enters your address space. It is a routing optimisation with an access
  control hook.
- A **private endpoint** places a network interface with a private IP from your subnet in front
  of the service. The service becomes addressable inside your VNet, and it works from
  on-premises over ExpressRoute or VPN. Service endpoints do not.

"Must be reachable from on-premises" or "must have a private IP" selects private endpoint. Every
time.

The AWS pair has the same shape with clearer names: a **gateway endpoint** is a route table
entry and only serves S3 and DynamoDB and costs nothing. An **interface endpoint** is an elastic
network interface with a private IP, works for most services, and is billed hourly plus data.

## Load Balancers

| Layer and reach | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Layer 7, regional | Application Load Balancer | Application Gateway | Regional external Application Load Balancer |
| Layer 7, global | CloudFront | Front Door | Global external Application Load Balancer |
| Layer 4, regional | Network Load Balancer | Azure Load Balancer | External passthrough Network Load Balancer |
| Layer 4, global | Global Accelerator | — | External proxy Network Load Balancer |
| Internal | Internal ALB or NLB | Internal Load Balancer | Internal Application or Network Load Balancer |
| Appliance insertion | Gateway Load Balancer | — | — |
| DNS-level routing | Route 53 routing policies | Traffic Manager | — |
| Built-in web firewall | AWS WAF, attached | Application Gateway WAF, Front Door WAF | Cloud Armor |

Points that decide questions:

- **Traffic Manager is DNS only.** It hands out different answers and then steps out of the
  path. It cannot terminate TLS, rewrite a header, or fail over a live connection, because it
  never sees the traffic. Front Door is a reverse proxy and does all of those. A question
  mentioning header-based routing or TLS offload at the edge is a Front Door question.
- Route 53 occupies the same DNS-only position in AWS, and **Global Accelerator** is the anycast
  data-path answer.
- Google renamed its whole load balancer family to describe behaviour, so material written
  before the rename uses names like "HTTP(S) Load Balancing" and "TCP Proxy". The current names
  say external or internal, then passthrough or proxy, then Application or Network.
- **Google's global external Application Load Balancer uses a single anycast IP worldwide.** AWS
  and Azure need a global service in front of regional load balancers to achieve the same thing.

## DNS

| Need | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Public authoritative DNS | Route 53 | Azure DNS | Cloud DNS |
| Private zones inside the network | Route 53 private hosted zone | Azure Private DNS zone | Cloud DNS private zone |
| Domain registration | Route 53 Domains | App Service Domains | Cloud Domains |
| Health-checked failover | Route 53 health checks | Traffic Manager probes | Load balancer health checks |

Route 53 is one service doing registration, DNS, health checks and traffic policy. Azure splits
those three ways, so a weighted-routing question there goes to Traffic Manager, not Azure DNS.

## Drill

| Question | Answer |
| --- | --- |
| Block one specific IP address in AWS. Which object? | A network ACL. Security groups cannot deny |
| Traffic reaches the instance, replies never return. Likely cause? | A stateless network ACL missing a return rule on ephemeral ports |
| Service must be reachable from on-premises over ExpressRoute with a private IP | Private endpoint, not service endpoint |
| A peers with B, B peers with C. Can A reach C? | No, in all three clouds |
| Which Google objects select firewall rule targets? | Network tags or service accounts |
| TLS termination and header routing at the global edge in Azure | Front Door. Traffic Manager is DNS only |
| One global anycast IP for a web app, natively | Google global external Application Load Balancer |
| AWS endpoint type that is free and only serves S3 and DynamoDB | Gateway endpoint |

## Next

[04-compute.md](README.md), then [09-confusing-terms.md](09-confusing-terms.md) for the
firewall and endpoint vocabulary in one place.

<!-- This document follows common-doc-guidelines.md. -->
