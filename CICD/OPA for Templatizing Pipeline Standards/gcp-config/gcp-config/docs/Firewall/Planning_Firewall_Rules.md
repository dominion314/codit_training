# Planning and Requesting Firewall Rules in GCP

As a customer of the Public Cloud Network Infrastructure, customers should plan and document your network connectivity needs between their own app components, other customers of GCP, across Kohl's Infrastructure, and beyond.  When development and/or infra staff understand how the application needs to communicate with other resources, they can use the following document to plan a Firewall request to build said connectivity.

## GCP Firewall Rule Components and How to Use Them

By Kohl's default, an instance in GCP will have open access for egress communication, and limited access for ingress.  Chances are, a dev team will need to configure `Machine Tag` for their VM and a VPC firewall rule that uses the `Machine Tag` to grant the access.  

> Note: Egress rules are generally permitted leaving your GCP VM Instance, however a FW request will still be required if the destination goes to a Network Endpoint outside of Kohl's (public or SaaS provider) or potentially to some On Prem Segments
> 
A Single Firewall Rule requires the following:

- A source and/or destination VPC (or Network in GCP Terms) if source/destination is within GCP
- Either source IP Address(es), or Network Tag.  (For Network Tag, see the same-VPC section below)
- One or combination of destination IP Address(es), and Network Tag. 
- A combination of protocol(s) and port(s)

### VPCs (Networks)

A VPC is a resource in Google that houses network connectivity for your NetX (and other) projects. As you choose to deploy a VM instance, you will need to choose a subnetwork and VPC (Network) that the compute instance will use for communication. 

With Legacy types of environments you may have many VPCs, while NetX environments have one.  The Cloud Networking team encourages teams to understand what Host Project your Service Projects are connected to and understand what VPCs you're using today.

### IP Addresses and CIDR Blocks

IP address blocks are allocated to your VPC via subnetwork objects.  One compute instance can use one or many IP addresses.  While it's possible to use a single IP address in a firewall rule it's not advised.

In order to be cloud native, teams will need to determine deployment patterns that will scale up and down quickly, where instances are created and destroyed as needed.  Because of this, it's not advised to use singular IP addresses unless the resource referenced is static.

Subnetworks have the ability to be purpose driven, so instead of creating a large subnet for all compute, users have the choice to create smaller subnets for different purposes.  With this in mind it is recommended that IP CIDRs are used instead.  IP CIDRs are shorthand notation for IP address networks and their subnet masks.  [This](https://www.keycdn.com/support/what-is-cidr#how-does-cidr-work) article is useful in understanding how to use this notation.  [Here](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/CIDR_Prefix_Table.md) is a chart that can help customers determine a CIDR block based on how many IPs (and VM hosts) can be within.

### Network Tags

Network Tags are a compute instance attribute.  It's up to the developer to create and manage their own tags whether manually or by automation.  When a tag is created it is referenced in a firewall rule that is applied to the instance.  

Tags can be used for both source and destination traffic when within the same VPC.  However a source tag is not retained once traffic leaves the VPC, leaving only target tags as the viable option.

Developers are responsible for creating and keeping track of their own network tags.  It's HIGHLY recommended that tags reference the LOB, environment, and purpose.

## Firewall Rule Patterns

When planning for a new firewall rule, one rule could be deployed in multiple places.  For example, a single traffic flow with the source of "Stores" to a destination of "example-nx-lle" VPC in GCP, will potentially need to traverse: Store Firewalls, Onprem Firewalls, Cloud Exchange Firewalls, and GCP Firewalls

Because of this, a single rule will need all of the information that will suit a deployment on whatever firewalls automation or deployment teams will require.

A single firewall rule can fit 4 different classifications (but really just 3) that might change the information that's required.

1. Same VPC Communication within GCP
2. Destination is a GCP VPC from anywhere except the same VPC
3. Destination is anywhere except GCP
4. Destination is a GCP VPC that is not your own.

### 1. Same VPC Communication

Users who are building different components to their application will need some clusters and VMs to talk to to other resources in their own project.  It's required that these traffic patterns use both `source tag` and `target tag` for this communication.

IP Addressing is not required since it will not pass through onprem firewalls.  Omitting any IP addresses gives full control on what subnet and IP the instances are using, while still giving the access that is required. 

#### Example

  - Source: `myapp-lle-client-tag`
  - Source VPC: `myapp-nx-lle`
  - Destination: `myapp-lle-server-tag`
  - Destination VPC: `myapp-nx-lle`
  - Ports: `tcp:80`

### 2. Destination is your VPC; Source is Anywhere Else

As mentioned above, while it's ideal to use `tag` to `tag` for firewall access, `tags` are not retained when traffic leaves a VPC.  Because of this, it's recommended that the source contains an IP address CIDR or an IP address.  

When planning firewall rules, customers MUST consider rules that should be deployed that allows access to their service in GCP.  This means the source IP ranges should include all potential customers (with considerations if the destination are secure or PCI sensitive).  The goal is to ensure that firewall rules are deployed in a way that consumers of a service will not need to worry about firewall rules.  Some examples of source locations could be:
- Stores
- eFCs/DCs
- eECs/DCs user segments
- Corp Wireless segments
- Remote Access VPN segments
- KIC User Segments
- WCITO User Segments
- many more

Consider what segments in the Kohl's enterprise should have access to your service, and if needed contact Network for assistance on determining the correct IP segments to list in your firewall rule.  If this application should be open to all Kohl's segments and environments, please use the IP CIDRs `10.0.0.0/8 and 172.26.0.0/15`.  

A `target tag` is required in this case, but customers should consider adding a IP CIDR for their resource if the source range includes non-GCP networks.  The reason for this, is a rule that could originate from an onprem location may need to be deployed on a firewall that is not `tag` aware.  In these cases an IP CIDR should be available.  

#### Example

- Source: `10.57.0.0/16`
- Source VPC: `N/A`
- Destination: `10.187.0.0/24`, `myapp-server-lle`
- Destination VPC: `myapp-nx-lle`
- Ports: `tcp:8443`

### 3. Destination is anywhere except GCP

As mentioned before, Egress firewall rules are all open on instances in GCP.  This means that users will only need to consider Firewall access onprem or to non Kohl's Segments (SaaS provider as an example).  These onprem firewalls do not use tagging, and instead require IP addressing to determine source and destination.  

> Note: When choosing rules that are not for deployment into GCP, you have the option to use an `Object Group`.  An `Object Group` is a logical name for one or more CIDRs that can be used in multiple firewall rules.  As customers, you have the option create and update your own `Object Group` and potentially use an existing `Object Group` as needed. The form to request these groups can be found [here](https://doms.service-now.com/nav_to.do?uri=%2Fcom.glideapp.servicecatalog_cat_item_view.do%3Fv%3D1%26sysparm_id%3Dec1f723cdb1d8c5080c3ec51ca9619fe%26sysparm_link_parent%3D5e0dd8c02b190100ca80b14d59da1561%26sysparm_catalog%3De0d08b13c3330100c8b837659bba8fb4%26sysparm_catalog_view%3Dcatalog_default%26sysparm_view%3Dcatalog_default)

#### Example

- Source: `10.187.0.0/24`
- Source VPC: `N/A`
- Destination: `Store Subnets` # Example of an Object Group
- Destination VPC: `N/A`
- Ports: `tcp:22,80,443`

### 4. Destination is another VPC in GCP

Stop!  Do you own the resources in that VPC?  Is it appropriate for you to deploy firewall rules in another customer's environment?  Consider these questions before you proceed.  While it's feasible to do, you could introduce risk or redundant rules.  

It's recommended that you work with Network Service Delivery or the other customer to determine if a new FW request is warranted.  

If the other VPC belongs to you, the customer, the consider this as an Ingress rule from the other side (scenario 2).

## Requesting Firewall Rules

Due to strict auditing and review processes involving teams across the environment, a form is utilized for all firewall related activities and can be found below:

[Service Now Firewall Request](https://doms.service-now.com/nav_to.do?uri=%2Fcom.glideapp.servicecatalog_cat_item_view.do%3Fv%3D1%26sysparm_id%3D60c03d6fd5a16d008555ecdaf8f2ed65%26sysparm_link_parent%3D5e0dd8c02b190100ca80b14d59da1561%26sysparm_catalog%3De0d08b13c3330100c8b837659bba8fb4)

With the planned rules you have documented, you should be able to use this form to get the process started.  The form itself may change and improve over time, but the core structure of the rule will stay the same.

As new features and tagging methods are released into GCP, this document and the firewall form will also update.  