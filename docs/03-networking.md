# Networking: Reachability Is Not Authorization

A successful request needs name resolution, a route, permitted traffic, a listening service
and application authorization. A private address alone establishes none of the other four.

## Network and Subnet Scope

AWS VPCs and Azure VNets are regional. Google VPC networks are global. AWS subnets are zonal;
Azure and Google subnets are regional. Defaults depend on account or project creation and
organization policies, so inspect the actual network instead of assuming a default exists.
[Network and location drawing](01-mental-models.md).

## Traffic Filtering

![Scope and behavior of native traffic controls](assets/architecture/firewall.svg)

| Control | Association or target | State and rule behavior |
| --- | --- | --- |
| AWS security group | Network interfaces of supported resources | Stateful allow rules; no explicit deny |
| AWS network ACL | Subnet | Stateless, numbered allow/deny rules; first match wins |
| Azure NSG | Subnet, interface, or both | Stateful allow/deny rules; lower priority number evaluated first |
| Google VPC firewall rule | Defined on a network, applying to selected VM interfaces | Stateful allow/deny; priority and rule interactions matter |

A new AWS security group has no inbound rules, while a default security group allows inbound
traffic from members of that group. Default and custom network ACLs also have different initial
rules. In Azure, custom NSG rules have higher precedence than built-in defaults. In Google,
a deny takes precedence over an allow at the same priority; omitted targets mean all instances
in the network, while supported selectors include network tags and service accounts.
[AWS security groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html),
[AWS ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html),
[Azure NSGs](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview),
[Google firewall rules](https://docs.cloud.google.com/firewall/docs/firewalls).

To block an address while broad AWS security-group allows remain, select a suitable deny-capable
control. An ACL is one option; a network firewall or application-layer rule may better match
the traffic and inspection requirement. A stateless ACL needs explicit return-path rules.

## Outbound Access

For IPv4 internet access, choose an explicit egress path and inspect routes and firewall rules.
AWS has both zonal and regional NAT gateways. Regional automatic mode can expand across workload
zones, but expansion is not instantaneous and regional NAT does not support private NAT.
Azure NAT Gateway behavior depends on SKU and configuration. Google Cloud NAT provides
translation through distributed networking rather than a NAT VM in the packet path.
[AWS regional NAT](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html),
[Azure NAT](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview),
[Google Cloud NAT](https://docs.cloud.google.com/nat/docs/overview).

A NAT gateway is not a way to accept unsolicited inbound requests. Public IPs, proxies and
load balancers have separate purposes. IPv6 egress has different design options.

## Connecting Networks

Ordinary VPC/VNet peerings are not transit routers. A-to-B and B-to-C peering alone does not
create A-to-C reachability. Address overlap and route exchange restrictions vary by provider
and address type. Use a supported transit design for a hub network.
[AWS peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html),
[Azure peering](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview),
[Google peering](https://docs.cloud.google.com/vpc/docs/vpc-peering).

Direct Connect, ExpressRoute and Cloud Interconnect provide private connectivity options;
private connectivity is not a universal promise of encryption. Verify encryption, routing,
redundancy and failure behavior for the selected connection.

## Accessing Managed Services Privately

![Private endpoint patterns with separate consumer and service boundaries](assets/architecture/private-access.svg)

| Mechanism | Important distinction |
| --- | --- |
| AWS gateway endpoint | Route-based S3 or DynamoDB access; no endpoint fee; not accessible through VPN, Direct Connect or peering |
| AWS interface endpoint | Endpoint interfaces for supported PrivateLink services; service support, DNS and costs vary |
| Azure service endpoint | Service retains its public address; not an on-premises private endpoint |
| Azure private endpoint | Private IP in the consumer VNet; hybrid clients need routing and DNS |
| Google Private Google Access | Access mechanism for supported Google APIs; distinct from a PSC private endpoint |
| Google Private Service Connect | Consumer endpoint/backend and producer-service patterns; connectivity varies by configuration |

Sources: [AWS gateway endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html),
[AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html),
[Azure service endpoints](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview),
[Azure private endpoints](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview),
[Google private access](https://docs.cloud.google.com/vpc/docs/private-google-access),
[Google PSC](https://docs.cloud.google.com/vpc/docs/private-service-connect).

Creating a private endpoint does not universally disable the service's public endpoint, grant
data access, or solve DNS. The managed service remains outside the consumer subnet; the
endpoint is the network entry point, not the service itself.

## Load Balancing and DNS

| Requirement | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Regional HTTP proxy | Application Load Balancer | Application Gateway | Regional Application Load Balancer |
| Global HTTP entry point | CloudFront | Front Door | Global external Application Load Balancer |
| DNS traffic steering | Route 53 routing policies | Traffic Manager | Cloud DNS routing policies |
| Appliance insertion | Gateway Load Balancer | Gateway Load Balancer | Use a supported appliance/routing architecture |

These are functional comparisons, not identical implementations. CloudFront is also a CDN;
Global Accelerator is a TCP/UDP service, not a layer-7 header-routing engine. DNS steering does
not proxy the connection or migrate established sessions. Proxy failover also does not promise
that an existing connection survives an origin failure.
[AWS global acceleration](https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html),
[Azure Traffic Manager](https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview),
[Azure Gateway Load Balancer](https://learn.microsoft.com/en-us/azure/load-balancer/gateway-overview),
[Google DNS routing](https://docs.cloud.google.com/dns/docs/routing-policies-overview),
[Google load balancing](https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview).

**Next:** [database availability](05-databases.md) · [architecture atlas](architecture.md).

<!-- This document follows common-doc-guidelines.md. -->
