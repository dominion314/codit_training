# Connectivity to GCP/on-prem for your Host Project

> NOTE:  All VPN and/or Interconnect related tasks should be validated or performed by Network Engineering staff at Kohl's.  Attempts to push your own updates to routes, router, interconnect, or VPN objects in Google may impact network connectivity within your project and possibly workloads in Cloud environments and on-prem locations such as stores. 

## Intra-GCP Connectivity

The following is required to build connectivity between a host project to other Kohl's host projects in Google Cloud Platform.

1. Prerequisites
2. `default_vars/default-vpn.yml`
3. Deployed VPN Secrets
4. `VPC-connect-gcp.yml`
5. `default_vars/default-router-asn.yml`

### 1. Prerequisites

The host project should have the following resource deployed at a minimum
-  `project.yml` file to ensure the project name is available for templating.  The project itself does NOT need to be managed by GitOps or the Google Operator
- `network.yml` file since various Google resources will require a functional VPC to deploy objects to.
### 2. `default_vars/default-vpn.yml`

This file will usually be deployed already and should require no updates.  This simply identifies for your host project, what transit VPC it should connect to in order to hop to another host project for Kohl's.  This file also defines what shared secret it should use for any VPNs.

### 3. Deploy VPN Secrets

As metioned above, a shared secret is required for a VPN to be built.  This secret is kept in Vault and deployed to your project namespace in the form as a `secret`.  The process of deploying this secret can be found in other documentation for supporting Jenkin's pipelines and/or operators.  This process is strictly managed by Cloud Networking.

### 4. `VPC-connect-gcp.yml`

Your project folder will require a definition file for the `{{ VPCname }}-connect-gcp.yml`document.  Please reference `vpcConnectGCP.md` to understand the formatting of this file.

The end result should be similar to this.

```yaml
---
vpcs:
  demo-nx-lle:
    routerDef:
      demo-nx-lle-c1-gcp-rtr01:
        region: us-central1
        description:
        routerASN:  
        advertiseMode: DEFAULT
        custom_advertised_ip_ranges:
          includeSubnetDef: true
          customIPList:  #only needed when advertiseMode is true
        ha_vpn_gateways_to_transit:
          cpe-nx-lle-c1-totransit:
            description:
            if0_peer_cidr:
              cidr: 169.254.0.0/30
            if1_peer_cidr:
              cidr: 169.254.0.4/30
```
> NOTE: These parameters allow for custom values for `routerASN`.  However, in order to prevent overlapping Autonomous System Numbers across the Kohl's GCP environment, these should be stored in a global variable file listed in the following step.  

### 5. `default_vars/default-router-asn.yml`

Autonomous System Numbers is a concept used for BGP routing.  In order for customer and engineering environments to talk with each other, each line of business router requires a unique ASN so routing can properly advertise their environments to the rest of Kohl's.  

Because of this, the ASN assignments needs global visibility to prevent overlap.  These assignments are stored in the `default_vars` folder and is named `default-router-asn.yml`.  Staff will be required to allocate an unused ASN in this document, and reserve it using the router name that was picked in step 4. 

Update this file and ensure proper formatting is followed and that you do not modify other ASNs reserved by other customers.  The resulting file looks like this.

```yaml
---
# ASNs between 4,200,000,000 - 4,294,967,294
#
# 4200000008: intra-xpn-transit-c1-gcp-rtr01
# 4200000009: intra-xpn-transit-e1-gcp-rtr01
# 4200000010: cpe-nx-lle-c1-gcp-rtr01
# 4200000011: cpe-nx-lle-e1-gcp-rtr01
# 4200000012: cpe-nx-prd-c1-gcp-rtr01
# 4200000013: cpe-nx-prd-e1-gcp-rtr01
# 4200000014: demo-nx-lle-c1-gcp-rtr01 <-- Update the comment here for easy, sequential searches for ASNs

ha_vpn_to_global_transit_asn:
  kohls-intra-transit-xpn-prd:
    intra-xpn-transit-c1-gcp-rtr01: 4200000008
    intra-xpn-transit-e1-gcp-rtr01: 4200000009
  kohls-cpe-xpn-lle:
    cpe-nx-lle-c1-gcp-rtr01: 4200000010
    cpe-nx-lle-e1-gcp-rtr01: 4200000011
  kohls-cpe-xpn-prd:
    cpe-nx-prd-c1-gcp-rtr01: 4200000012
    cpe-nx-prd-e1-gcp-rtr01: 4200000013
  kohls-demo-xpn-lle:                    #<-- Add your host project as a new key
    demo-nx-lle-c1-gcp-rtr01: 4200000014 #<-- Add the router that you've created here with the appropriate assignment
```
## On-Prem Connectivity

** Coming Soon **
