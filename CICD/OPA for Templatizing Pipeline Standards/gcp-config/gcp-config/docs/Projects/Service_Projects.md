# How to Create a Service Project

## Summary

Staff who want to create a new service project will need to do the following:

1. Create a project folder and `project.yml` file to specify details of the project.
2. Create an `iam-policy-members.yml` to assign IAM permissions to the project.
3. Update eunomia vars to include the new folder in the eunomia build process
4. Update the attached host project's `project.yml` file with details of your service project to establish the host to service project relationship
5. Create or update a subnetwork definition with permissions matching what has been defined in your `iam-policy-members.yml`.

[Video_overview_of_process](https://drive.google.com/file/d/1p0UmW7_e-2999E4QRCtA1aihEYmwlUlm/view?usp=sharing)

## Detail

### 1. Create Project

Within the `project_vars` directory in the `gcp-config` repo, create a new folder with the appropriate service project name.  Once inside that folder, create a new file called `project.yml`

Follow directions within the [`parameter_schema.md`](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Parameter_Schema.md) file.  After created your `project.yml` will look like this.

```yaml
---
billingDeptId: "00000"
project:
  name: doms-demo-lob-lle
  managed: true
  folderId: "11111111111"
  billingAccount: "8675-309-jenny"
  labels:
    billing-dept-id: "00000"
    project-manager: project_guy
    devops-lead: dev_guy
    environment-type: lle
    line-of-business: demo
    project-requestor: requestor_guy
serviceAPIs:
  compute.googleapis.com:
  oslogin.googleapis.com:
  cloudresourcemanager.googleapis.com:
  storage-component.googleapis.com:
  storage-api.googleapis.com:
  stackdriver.googleapis.com:
  logging.googleapis.com:
  monitoring.googleapis.com:
  cloudasset.googleapis.com:
```
### 2. Create IAM Policies

create a new file called `iam-policy-members.yml`

Follow directions within the `parameter_schema.md` file.  After created your `iam-policy-members.yml` will look like this.

```yaml
---
iamPolicyMembers:
  groupsByEmail:
    gcp-demo-lob-devops-admin@doms.com:
      roles:
        - compute.storageAdmin
        - iam.serviceAccountUser
        - storage.admin
        - compute.instanceAdmin
        - compute.networkUser
        - container.admin
    gcp-demo-lob-devops-l3@doms.com:
      roles:
        - compute.storageAdmin
        - iam.serviceAccountUser
        - storage.admin
        - compute.instanceAdmin
        - compute.networkUser
        - container.admin
```
### 3. Update Eunomia Configuration

Eunomia will pull your new folder definition once the Eunomia seed configuration is updated with the relevant details.

Navigate to the `gcp-config` repo, then to `eunomia_vars/doms-cpe-kcc-prd-01/vars/projects.yml`

Add your project folder to the list of managed projects.  The file will look like this.  Ensure you use proper indentation.

```yaml
---
projects:
- name: doms-cpe-xpn-lle
  gitRef: master
- name: doms-cpe-xpn-prd
  gitRef: master
- name: doms-intra-transit-xpn-prd
  gitRef: master
- name: doms-multitenant-xpn-lle
  gitRef: master
- name: doms-cpe-kcc-lle
  gitRef: master
- name: doms-cpe-cpa-lle
  gitRef: master
- name: doms-ocf-lle
  gitRef: master
- name: doms-ocf-stateful-lle
  gitRef: master
- name: doms-cpe-cne-lle
  gitRef: master
```
### 4. Attach Host Project to the Service Project

Service projects need to be associated to a host project for network resources.  Identify the appropriate project for your LOB/ENV named `doms-{{LOB}}-xpn-{{ENV}}`.  Find the `project.yml` file for the host project and add/update your service project under the `projectSharing` key as a list.  An example of this will be so:

```yaml
project:
  name: doms-demo-xpn-lle
  managed: true
...
projectSharing:
  - doms-demo-svc1-lle
  - doms-demo-svc2-lle
```

With NetX, there has been a reduction in the number of host(xpn) projects. The [Netx_Host_Project_Mapping](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Netx_Host_Project_Mapping.md) in this folder will assist you in identifying the proper one for your team. You will need to know your Product Domain which can be found by visiting the [Kohl's Balanced Teams](https://sites.google.com/doms.com/kt-way/how-we-work/balanced-teams) site.

### 5. Add Subnet IAM

After setting up your project sharing, subnets need permission to be shared in the same manner.

Navigate to the host project and create/update the file named `{{VPC}}-subnetwork-std.yml`  Add a subnetwork per the documentation found in `vpcNetworksAndSubnetworks.md`.

Add subnet IAM to the subnetwork object with the documentation found in `parameter_schema.md`

The resulting subnetwork object should look like this.

```yaml
      demo-nx-lle-svc1-c1-prv01:
        advertiseRoutes: true
        region: us-central1
        network:
          ip: 11.1.1.1/22
          bluecat-id: 111111
        permissions:
          groupsByEmail:
          - gcp-demo-devops-admin@doms.com
          - gcp-demo-devops-l3@doms.com
