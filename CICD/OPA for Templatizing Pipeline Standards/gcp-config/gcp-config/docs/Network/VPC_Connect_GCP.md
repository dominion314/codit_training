# GCP Connectivity

Inter-GCP connectivity is leveraged with HA VPN tunnels to a centralized transit VPC.  Cloud Routers are used to dynamically propagate routes as subnets are created and deleted.

For connectivity out of a given VPC to the internet, Cloud NAT is created using the same Cloud Routers that are used for the HA VPN tunnels.

## Cloud Router Base Configuration

The Cloud Router is built with the template `vpcVPNRouter.yml.j2`.  The variables to populate the template should come from a var file that contains the suffix `{{ VPC_NAME }}-connect-gcp.yml`.  The formatting required for the router configuration is as followed.  

```yaml
---
vpcs:
  demo-vpc:

    routerDef:
      {{ ROUTER_NAME }}:
        region: {{ REGION }}
        description: {{ DESCRIPTION }}
        routerASN: # no
        advertiseMode: (DEFAULT|CUSTOM)
        custom_advertised_ip_ranges:
          includeSubnetDef: (true|false)
          customIPList:
            - {{ CIDR }}
```

| Parameter                                    | Notes                                                                                            |
|----------------------------------------------|--------------------------------------------------------------------------------------------------|
| region                                       | Required. Central and East Regions only                                                          |
| description                                  | Optional.                                                                                        |
| routerASN                                    | Optional. Pulls from Default level variables when blank                                          |
| advertiseMode                                | Required. Default automatically pulls all subnets to advertise.  CUSTOM enables following option |
| custom_advertised_ip_ranges                  | Used only when advertiseMode is Custom                                                           |
| custom_advertised_ip_ranges.includeSubnetDef | Include subnets where parameter definition for subnet has advertiseRoutes as True                |
| custom_advertised_ip_ranges.customIPList     | List of IP CIDR ranges to advertise           |

The cloud router is a regional construct.  With the VPC routing mode as GLOBAL the behavior will change to include all subnets in the VPC for routing updates.  When configuring a new router, it is required to provide it a unique ASN found in the default variables directory.  The file structure will as such:

```yaml
---
# ASNs between 4,200,000,000 - 4,294,967,294
ha_vpn_to_global_transit_asn:
  doms-cpe-xpn-lle:
    cpe-nx-lle-c1-gcp-rtr01: 4200000010
    cpe-nx-lle-e1-gcp-rtr01: 4200000011
```

When adding a router, this default file MUST be updated with the `{{ project }}.{{ router_name }}` key.  The resulting value must be a unique ASN between 4,200,000,000 and 4,294,967,294.  

Routers within a custom VPC should be set to DEFAULT.  This will automatically advertise routes of all subnets found in the VPC.  Do not flip VPC routers to CUSTOM without understanding the impact to your traffic being routed inbound to VPC.

## Adding HA VPN to Transit

"HAVPN to Transit" settings are exclusively to build connectivity to other GCP projects and VPCs without needing to route back on-prem.  The transit VPC is currently defined in [default variables](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/default_vars/default-vpn.yml)

```yaml
transit_hub:
  namespace: gcp-doms-dev-cne-transit-lle
  vpc: xpn-transit
  centralRouterName:  transit-hub-central1-router
  eastRouterName: transit-hub-east1-router
```

**These settings should never be modified as they are global to all GCP projects.**

When a connection to transit is needed, the same parameter file is used `{{ VPC_NAME }}-connect-gcp.yml`.  The VPN connection is appended to the router definition in the file.  

```yaml
---
vpcs:
  demo-vpc:

    routerDef:
      {{ ROUTER_NAME }}:
        region: {{ REGION }}
        description: {{ DESCRIPTION }}
        routerASN: # no
        advertiseMode: (DEFAULT|CUSTOM)
        custom_advertised_ip_ranges:
          includeSubnetDef: (true|false)
          customIPList:
            - {{ CIDR }}
        # Begin HA VPN to Transit Section

        ha_vpn_gateways_to_transit:
          demo-vpc-c1-tohub:
            description:
            if0_peer_cidr:
              cidr: {{ Peer CIDR }}
              spoke: {{ PEER CIDR LOWER }}
              hub: {{ PEER CIDR UPPER }}
            if1_peer_cidr:
              cidr: {{ Peer CIDR }}
              spoke: {{ PEER CIDR LOWER }}
              hub: {{ PEER CIDR UPPER }}
```

Peer IP addresses need to be unique and allocated from bluecat.  With the information attached to a router, it will create the necessary resources to establish two VPN connections and establish dynamic routing.

Multiple HAVPN transit connections can be created from one router.  At most for GCP connectivity, one router per region should be leveraged so quotas are not exceeded.

## Adding Cloud NAT

Cloud NAT is created in a similar fashion to the Transit HAVPN. A section is created under a given Cloud Router.  

```yaml
---
vpcs:
  demo-vpc:

    routerDef:
      demo-vpc-c1-gcp-rtr01:
        region: us-central1
        description:
        routerASN:  # Custom ASN, if blank will pull from GLOBAL-ASN.YML
        advertiseMode: DEFAULT
        custom_advertised_ip_ranges:
          includeSubnetDef: true
          customIPList:

        # Begin Cloud NAT Creation
        outbound_nat_gateway:
          name:
          icmp_timeout:
          tcp_est_timeout:
          tcp_trans_timeout:
          udp_timeout:
          min_ports_per_vm:
          logConfig:
            enable: false
            filter:
```

| Parameter         | Notes                                                                      |
|-------------------|----------------------------------------------------------------------------|
| name              | Required. Name of the NAT Gateway                                          |
| icmp_timeout      | Optional, default 30s. ICMP Mapping Timeout                                |
| tcp_est_timeout   | Optional, default 1200s. Established TCP Session Timeout                   |
| tcp_trans_timeout | Optional, default 30s. Transitory TCP Session Timeout                      |
| udp_timeout       | Optional, default 30s. UDP Transaction Timeout                             |
| min_ports_per_vm  | Optional, default 64. Minimum TCP/IP Ports per Instance                    |
| logConfig.enable  | Enable Stackdriver logging for Cloud NAT, Leave False                      |
| logConfig.filter  | Required if logging is enabled. Default is ERRORS_ONLY. Additional options are ALL and TRANSLATIONS_ONLY |

Only one Cloud NAT can be associated with a Router. When a Cloud NAT is created, it will require references to subnetwork objects that are allowed to talk through it.  This setting is found on the subnetwork definition in the parameter `natRouter`.  This parameter needs to be defined and to reference the name of the Cloud Router.  See the example below. 

```yaml
---
vpcs:
  demo-vpc:
    subnets:

      sampleappname-c1-prv01:
        advertiseRoutes: true
        natRouter: demo-vpc-c1-gcp-rtr01
        region: us-central1
        network:
          ip: 192.168.10.0/28
          bluecat-id: 1231232
```

Note: You MUST have a participating subnet created in order for this to work.  If you have no participating subnets planned, then the NAT serves no purpose and you must omit the NAT creation.  