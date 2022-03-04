# IP Address Allocation

At this time, IP address allocations are automated with a PR check running in the `cloud-config/gcp-config` and `cloud-config/cloud-resources` repositories.  When creating a subnetwork object within test or production parameters, the check will detect certain keywords within a specific YAML structure, and populate a Bluecat IPAM IP address CIDR for you via a commit to your PR.

## High Level Process

As mentioned, the automation is triggered by a Pull Request.  It is expected for schema validations and checks to fail due to a lack of proper IP address info.  However the PR will rectify this for you.

> NOTE: For Bluecat and IPAM allocations to work, any new branches need to be created off of the main repo.  Forked branches off of the main repo will not work with the automation in place.

The process of allocating an IP address is as follows.
1. User creates a new branch and subnetwork YAML document or appends to an existing one.
2. A subnetwork YAML section is created to describe subnetwork attributes
3. User should omit `ip` and `bluecat-id` keys.
4. User populates [`status`](#requesting-a-ip-cidr-with-the-status-field) key with a designated keyword that specifies type of IP address segment.
5. User commits changes, pushes branch to Gitlab, and opens a Pull Request
6. Bluecat Automation Webhooks trigger automation and finds designated keywords in yaml for an IP CIDR request.
7. Bluecat Automation adds a commit to the existing PR, replacing `status` with the word `PROVISIONED` and replaces/adds `ip`, `bluecat-id`, `cidr` where appropriate.
8. PR checks run again, and can proceed.

The process of removing an subnet is as follows.
1. User creates a new branch
2. A subnetwork YAML section is deleted, including any sections of `yaml` that describe the bluecat-id and ip address.
3. User commits changes, pushes branch to Gitlab, and opens a Pull Request
4. Pull Request checks are performed and passed.  Approvals are submitted.  PR is merged to master.
5. Bluecat Automation Webhooks trigger automation and detects a PR close and checks for removed code
6. Bluecat Automation detects a removed IP section, and uses removed bluecat-id to clean up allocation from Bluecat IPAM

> NOTE: Do not add an IP address allocation to a PR, then remove it within the same PR.

## Purpose Built Subnet Naming

Subnetwork configuration keys translate to the name of the subnet in GCP.  The naming of these subnets looks like this

`[vpcName]-[purpose]-[regionCode]-[subnetType][digit]`

| Subnet Section| Description|
|---|----|
| vpcName | The VPC/Network name.  Often at the top of the YAML|
| purpose | Owner/purpose of the subnet.  CNE recommends that subnets be pinned to an owner/purpose/application for easy firewall rule submission |
| regionCode | shortened region codes in GCP, currently allowing `c1` or `e1`|
| subnetType | Type of subnet, see below |
| digit | incrementing numbers in case multiple subnets of same name are needed, starting at `01`|
And example of this may be

`test-nx-lle-myapp-presgresdb-c1-prv01`

When deciding on subnet types, please choose from the following

| Subnet Type | Description|
|---|----|
| `prv` | Standard privately routed subnet, for most workloads |
| `pub` | Resources deployed onto these subnets will have an external IP attached |
| `sec` | Resources deployed onto these subnets will contain PCI or PII data |

## Parameter Sections Capable of IP Address Allocations

Only particular sections of your YAML code will trigger the IP allocation function to check a status field for an allocation request keyword.  The sections of YAML eligible are listed here:

```yaml
# Traditionally within a VPC-subnetwork-std.yml file
---
vpcs:
  {{ VPC_NAME }}:
    subnets:
      {{ SUBNET_NAME }}:
        region:               # Region for your subnetwork
        advertiseRoutes:      # Boolean to route subnet outside of VPC
        outbound_nat_gateway: # (Optional) permit access to NAT Gateway
        network:              # IP CIDR section
          ip:                 # IP CIDR populated manually or by automation
          bluecat-id:         # Populated by IP Automation, do not modify
          status:             # See section below for usage
```

> NOTE: The following is for Cloud Network Engineering Use ONLY

```yaml
# Traditionally within a VPC-connect-gcp.yml file
---
vpcs:
  demo-vpc:
    routerDef:
      {{ ROUTER_NAME }}:
        ha_vpn_gateways_to_transit:
          demo-vpc-c1-tohub:
            description:
            if0_peer_cidr:   # <--- This section will trigger a keyword search
              cidr:          # <--- IP CIDR populated manually or by automation
              bluecat-id:    # <--- Populated by IP Automation
              status:        # <--- Keyword field for a IP CIDR Request
            if1_peer_cidr:   # <--- This section will trigger a keyword search
              cidr:          # <--- IP CIDR populated manually or by automation
              bluecat-id:    # <--- Populated by IP Automation
              status:        # <--- Keyword field for a IP CIDR Request
```

## Requesting a IP CIDR with the `status` Field

The following are valid status entries and the resulting IP range provided by the automation.

| Status Code               | Description                                      |
|---------------------------|--------------------------------------------------|
| PROVISIONED               | Nothing to be done. IP ranges already provisioned|
| BLUECAT_ALLOC_GCP_##      | Allocate approiate subnet of cidr size ## in resource's region and (non)prod range|
| BLUECAT_ALLOC_BGP_30      | Allocate /30 subnet for use in HA VPNs           |
| BLUECAT_ALLOC_TST_##      | Allocates a non-routeable 192.168.x.x address for testing |
| BLUECAT_ALLOC_GCPSHIFT_## | Allocates a subnet for Openshift cluster nodes   |
| BLUECAT_ALLOC_PSA_24      | Allocates a subnet for Private Service Access    |

> The BLUECAT_ALLOC_GCP keyphrase will allocate the following subnet ranges: Regular, Openshift, GKE, and GKE Master.  The region and nonprod/prod subnets are determined from vpc naming and from the region field of the resource consuming the subnet.

> Note: The ## requires an appropriate CIDR prefix length.  If you are not familiar with CIDR prefixes, please refer to [this document](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/CIDR_Prefix_Table.md) for a table that will convert network sizing to the CIDR prefix.
