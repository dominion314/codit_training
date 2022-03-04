# On-Prem Connectivity

On-prem connectivity consists of use of the [Partner Interconnect](https://cloud.google.com/interconnect/docs/concepts/partner-overview) product from Google to directly connect to our Equinix Datacenters CH2 (Chicago, IL) and DC11 (Ashburn, VA).

The Partner Interconnect product is responsible initializing a connection from a Cloud Router in GCP, and extending this as a L2 connection to our On-Prem Routers across the datacenter using the Equinix Fabric Portal capabilities for configruations across the datacenter.

## Configuration of Partner Interconnect @ GCP

The Partner Interconnect is created with the template `vpcPIRouter.yml.j2`.  This template consumes the contents of the parameter file named `{{ VPC_NAME }}-connect-onprem.yml`.  The file is formated as such.

```yaml
---
vpcs:
  {{ VPC_NAME }}:

    interconnectRouterDef:
      {{ ROUTER_NAME }}:
        region: {{ REGION }}
        description: {{ DESCRIPTION }}
        advertiseMode: (DEFAULT|CUSTOM)
        custom_advertised_ip_ranges:
          includeSubnetDef: (true|false)
          customIPList:
            - {{ CIDR }}

        partnerInterconnect:
          description:  {{ DESCRIPTION }
          availabilityDomain: (1|2)

```

Much like how the GCP connectivity parameters work, a router definition is created and routing is configured.  To understand how to configure this, reference the `vpcConnectGCP.md` documentation.  Bear in mind that these routers are not under the key `routerDef` and is instead nested under `interconnectRouterDef` since these Routers abide by special rules that do not apply to GCP directed Cloud Routers.

More Documentation to come.
