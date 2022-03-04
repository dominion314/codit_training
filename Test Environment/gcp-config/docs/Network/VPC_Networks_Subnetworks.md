# vpcNetworks and vpcSubNetworks

## Networks (VPCs)

The template vpcNetworks.yml.j2 contains the operator CRs to create a VPC network (`computeNetwork`) and subnetworks (`computeSubNetwork`) within a given VPC.  

VPC definitions in the config repo should be defined inside of project specific folder, in a file named `{{ VPC_NAME }}-network.yml`.  There are no hierarchy capabilities with this resource.  Within this document, the YAML syntax should be structured as follows.

```yaml
vpcs:
  {{ VPC_NAME }}:
    vpcName: {{ VPC_NAME }}
    routingMode: (REGIONAL|GLOBAL)
```

| Parameter             | Notes                                             |
|-----------------------|---------------------------------------------------|
| vpcName               | Lower case, only hyphens allowed, end when letter |
| routingMode           | REGIONAL or GLOBAL                                |
| autoCreateSubnetworks | Can be omitted and will default to false          |

The VPC name should follow the standard of `(LOB_ABRIV)-nx-(ENV_TYPE)`.  An example of this would be `bda-nx-prd`

## Subnetworks

To process subnetworks, this is split between two files.  

- `{{ VPC_NAME }}-subnetwork-std.yml`
- `{{ VPC_NAME }}-subnetwork-gke.yml`

These were seperated because the gke networks have specific requirements to be built.  The seperation helps user identify GKE networks that are present and ensures they are aware that a minimum of two secondary networks are needed to for the template.

### Standard

`{{ VPC_NAME }}-subnetwork-std.yml` contains the following structure to be used in the template

```yaml
vpcs:
  {{ VPC_NAME }}:
    subnets:

      {{ SUBNET_NAME }}:
        advertiseRoutes: (true | false)
        outbound_nat_gateway: (NAME_OF_CLOUD_NAT_GATEWAY)
        region: (us-central1 | us-east1)
        network:
          ip: {{ CIDR_ADDRESS }}
          bluecat-id: {{ BLUECAT_OBJECT_ID }}
          status: {{ IPAM Allocation Status }}
        secondary:
          {{ SECONDARY_SUBNET_NAME }}:
            ip: {{ CIDR_ADDRESS }}
            bluecat-id: {{ BLUECAT_OBJECT_ID }}
          {{ SECONDARY_SUBNET_NAME }}:
            ip: {{ CIDR_ADDRESS }}
            bluecat-id: {{ BLUECAT_OBJECT_ID }}
```

| Parameter                 | Notes                                                                      |
|---------------------------|----------------------------------------------------------------------------|
| Subnet_name               | Refer to Naming Standards Document.|
| advertiseRoutes           | Required. See Cloud Router Documents for details                           |
| outbound_nat_gateway      | Can be omitted.  See Cloud NAT Documents for details                       |
| region                    | Required. us-central and us-east regions only.  Zones can vary             |
| network                   | Section is required.                                                       |
| network.ip                | CIDR Formatted address                                                     |
| network.bluecat-id        | bluecat object ID                                                          |
| network.status            | bluecat allocation request or status                                       |
| secondary                 | Section is Optional.                                                       |
| secondary.name.ip         | Key is the name of the secondary subnet.  IP is the CIDR formatted address |
| secondary.name.bluecat-id | bluecat object ID                                                          |

To add additional subnets within this VPC, simply add another `dict` as another value under the `subnets` key.

> To understand how Network IP and Bluecat values are populated, please review the IP addressing section below.

### GKE

`{{ VPC_NAME }}-subnetwork-gke.yml` contains the following structure to be used in the template.  **NOTE!: The `MASTER` subnet is not required in GKE, but is allocated with the `POD` and `SERVICE` subnets.  The `MASTER` subnet is provided directly to customers.**

```yaml
vpcs:
  {{ VPC_NAME }}:
    subnets:
      {{ SUBNET_NAME }}:
        advertiseRoutes: (true | false)
        region: (us-central1 | us-east1)
        network:
          ip: {{ CIDR_ADDRESS }}
          bluecat-id: {{ BLUECAT_OBJECT_ID }}
        gke:
          - podNetwork:  
              name: {{ POD_NETWORK_NAME }}
              ip: {{ CIDR_ADDRESS }}
              bluecat-id: {{ BLUECAT_OBJECT_ID }}
              status: {{ IPAM Allocation Status }}
            serviceNetwork:
              name: {{ SERVICE_NETWORK_NAME }}
              ip: {{ CIDR_ADDRESS }}
              bluecat-id: {{ BLUECAT_OBJECT_ID }}
              status: {{ IPAM Allocation Status }}
            masterNetwork:
              ip: {{ CIDR_ADDRESS }}
              bluecat-id: {{ BLUECAT_OBJECT_ID }}
              status: {{ IPAM Allocation Status }}
          - podNetwork:  #Additional clusters are optional
              name: {{ POD_NETWORK_NAME }}
              ip: {{ CIDR_ADDRESS }}
              bluecat-id: {{ BLUECAT_OBJECT_ID }}
              status: {{ IPAM Allocation Status }}
            serviceNetwork:
              name: {{ SERVICE_NETWORK_NAME }}
              ip: {{ CIDR_ADDRESS }}
              bluecat-id: {{ BLUECAT_OBJECT_ID }}
              status: {{ IPAM Allocation Status }}
            masterNetwork:
              ip: {{ CIDR_ADDRESS }}
              bluecat-id: {{ BLUECAT_OBJECT_ID }}
              status: {{ IPAM Allocation Status }}
```
| Parameter                 | Notes                                                                      |
|---------------------------|----------------------------------------------------------------------------|
| Subnet_name               | Refer to Naming Standards Document.                                        |
| advertiseRoutes           | Required. See Cloud Router Documents for details                           |
| outbound_nat_gateway      | Can be omitted.  See Cloud NAT Documents for details                       |
| region                    | Required. us-central and us-east regions only.  Zones can vary             |
| network                   | Section is required.                                                       |
| network.ip                | CIDR Formatted address                                                     |
| network.bluecat-id        | bluecat object ID                                                          |
| gke                   | Section will specifically take in GKE parameters.  key is a list                |
| gke.[].podNetwork     | name, ip, status, and bluecat-id for the pod range                             |
| gke.[].serviceNetwork | name, ip, status, and bluecat-id for the service range                         |
| gke.[].masterNetwork  | ip, status, and bluecat-id for the master range                                |

## Subnetwork Permissions

When creating subnetworks, the resources live in the host project.  If the host project is attached to many service projects, permissions are used to determine which of the service projects will have access to use the subnetwork.  You can create these permissions by following [this document](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Parameter_Schema.md#iam-policy-subnets).

It is important to note, that while the subnetwork permissions can reside in it's own YAML file, you have the option to code your `permissions` dict directly into the subnetwork structure.  An example of this would look like so.

```yaml
---
vpcs:
  demo-nx-lle:
    subnets:

      demo-nx-lle-sampleapp-c1-prv01:
        advertiseRoutes: true
        region: us-central1
        network:
          ip: 1.1.1.1/28
          bluecat-id: 1234546
          status: PROVISIONED
        permissions:
          serviceAccountsByEmail:
          - terraform-demo@kohls-demo-lle.iam.gserviceaccount.com
          groupsByEmail:
          - demo-role-monitoring-devops-l3@kohls.com
          - demo-role-devops-admin@kohls.com
          - demo-role-devops-l2@kohls.com
          - demo-role-devops-l3@kohls.com
          - demo-role-devops-manager@kohls.com
```

> Note: if a team or service account is given access to a subnet, it's possible the subnet will be shared with multiple service accounts if that team has IAM permissions on the project.

## IP Address CIDR allocation

Please review the following document to understand how IP address allocations are requested and performed

https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/IP_Address_Allocation.md