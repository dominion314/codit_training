# PSA (Private service access)
The template psa-network.yml.j2 creates all of the CRs that enable a PSA connection in a given VPC within a host project.
**Note:**
*No need to add the ServiceNetworking API to the project file, it is enabled as part of this PSA template*

## Enabling PSA  
The {{ vpc_name }}-network.yml file needs to be modified in the XPN project for the VPC, adding the key "psaNetwork".  This key contains a child item, the PSA name, which in turn contains a single key of "network" where the value is the subnet that is allocated to google to host the cloud service.
**Note:**
*There is no bluecat automation associated with PSA at this point*

```yml
---
  vpcs:
    {{ vpc_name }}:

      routingMode: GLOBAL
      autoCreateSubnets: false
      psaNetwork:
        {{ vpc_name }}-{{ service }}-01:
          network: 10.124.xx.xx/xx

```

## Currently supported PSA
We currently have PSA deployed for:
- mySQL
- postgres
- redis

## Considerations
You will need to find out how many cloud services and how many regions will be making use of the PSA.  Out of the above configure supernet, each service will carve out a smaller subnet per region it is deployed in.
ie:
1 mySQL service x 2 regions = 2 x /24's = /23 required for PSA at minimum (no room for further expansion if customer needs more IP's)
1 mySQL + 1 postgress service x 2 regions = 4 x /24's = /22 required for PSA

**Note:**
*mySQL and postgress seem to utilize /24 subnet size whereas redis appears to use only a /29*

## Current process
- Platform connectivity team will first need to allocate an appropriately sized supernet for your PSA and create the above config in your VPC
- Customer will then need to create a resource within the service in each region they intend to use;  this will trigger GCP to carve out child subnets
- Once resources are spun up, platform connectivity team will need to enable routing accordingly for the subnets that GCP allocated
- Firewall rules may need to be requested by customer for required connectivity
