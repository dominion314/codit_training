# How to Create/Manage a NetX Environment (Host Project)

## Summary

> Note: Environments for NetX, or Host projects in general should be initially set up by Network Engineering staff, as VPNs, inter-site connectivity, and routing can have drastic impact to the network connectivity across Kohl's.

> Note: NetX design specifies that host projects be reused for NetX environments and a consolidated VPC be created within. NetX design also indicates only a single NetX VPC be created for each host project.

The host project is a organizational object that contains all of your Google Cloud networking resources.  Within the host project users will be able to manage resources such as firewall rules, routes, routers, subnetworks, and access outside of your enviornment.

In order to create or manage a host project with GitOps, the steps are as follows

1. Create the project code
2. Update eunomia variables.
3. Create `heirarchy.lst`
4. Create the network.yml definition
5. IP Connectivity outside of your project.

### 1. Create Project

Within the `project_vars` directory in the `gcp-config` repo, create a new folder with the appropriate service project name.  Once inside that folder, create a new file called `project.yml`

Follow directions within the `parameter_schema.md` file.  After created your `project.yml` will look like this.

```yaml
---
billingDeptId: "90546"
project:
  name: kohls-cpe-sample-lle
  managed: true
  folderId: "345254712059"
  billingAccount: "00C36A-CD0BDB-E543D0"
  labels:
    billing-dept-id: "90546"
    project-manager: josh-doll
    devops-lead: mark-doll
    environment-type: lle
    line-of-business: cpe
    project-requestor: zaki
serviceAPIs:
  compute.googleapis.com:
  storage-component.googleapis.com:
  storage-api.googleapis.com:
  stackdriver.googleapis.com:
  logging.googleapis.com:
  monitoring.googleapis.com:
  cloudasset.googleapis.com:
```

### 2. Add your Host Project in Eunomia Config

Eunomia will pull your new folder definition once the Eunomia seed configuration is updated with the relevant details.

Navigate to the `gcp-config` repo, then to `eunomia_vars/kohls-cpe-kcc-prd-01/vars/projects.yml`

Add your project folder to the list of managed projects.  The file will look like this.  Ensure you use proper indentation.

```yaml
---
projects:
- name: kohls-cpe-xpn-lle
  gitRef: master
- name: kohls-cpe-xpn-prd
  gitRef: master
- name: kohls-intra-transit-xpn-prd
  gitRef: master
```

### 3. Create a heirarchy.lst file

Eunomia can import variables to your namespace/project that are relevant at a global level.  This file is necessary for host projects for global firewall definitions and information needed to build connectivity to other GCP projects and on-prem datacenters.

The `heirarchy.lst` file should be located in your project specific folder in the `gcp-config` repo.  Most of these files will require this at a minimum

```yaml
../../default_vars
./
```

The file states that template processing engines should consume variables from `../../default_vars` (reletive from the project specific folder), then consume the project folder itself.

### 4. Create the network.yml definition

The network definition creates the appropriate VPC for your NetX environment.  Follow details in the readme file `vpcNetworksAndSubnetworks.md`.  The resulting file will look like this

```yaml
---
vpcs:
  cpe-nx-lle:

    routingMode: GLOBAL
```

### 5. IP connectivity outside of your project.

Please refer to `Host_Project_Connectivity.md` for more details on this.

> NOTE:  All VPN and/or Interconnect related tasks should be validated or performed by Network Engineering staff at Kohl's.  Attempts to push your own updates to routes, router, interconnect, or VPN objects in Google may impact network connectivity within your project and possibly workloads in Cloud environments and on-prem locations such as stores.
