# Adding Subnetworks for Use in Service Projects

Most of GCP compute relies on a subnetwork for communication across the Kohl's Enterprise Enviornment.  These subnetworks require a unique range of IP addresses that do not overlap another, across all 1100+ locations.  Because of this, subnetwork objects are managed and kept in a customer's host project, and subsequently shared to appropriate service projects for compute to use.

While the host project is under strict IAM control, customers have the ability to perform the following steps (through code) to allocate their own IP address subnet, and share it with one or many of their service projects.

[Video_overview_of_process](https://drive.google.com/file/d/1pH8taDM0O42MIcL92lV7EkhUI7jyyBPG/view?usp=sharing)

## Creating Subnetwork YAML in a Host Project

Subnetwork objects reside in a host project.  If you do not know which host project to use or if you need one created, contact cloud teams for support.  Find your appropriate host project by finding the `xpn` designation in the name.  Examples of this will be `kohls-cpe-xpn-lle`, `kohls-bda-xpn-prd`, and `kohls-platform-xpn-lle`.  The project folder will be within the `gcp-config` repository in a folder named `project_vars`.

> Note: If you do not know which host project to use or if you need one created, contact cloud teams for support.

Within the host project configuration folder, there will be `yaml` documents that describe various resources.  Follow `yaml` guidelines in [this document](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/VPC_Networks_Subnetworks.md) to create your own `yaml` for a subnetwork.

> NOTE: Standard and GKE Subnetworks should be in seperate documents

> NOTE: DO NOT choose your own IP address network to populate into Google.  Failure to do so may risk routing issues and other problems that will cause GCP traffic to stop working.

Follow [these guidelines](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Parameter_Schema.md#iam-policy-subnets) to add a `permissions` structure to your subnet or create a separate document for them.

If you haven't navigated there already, follow [this document](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/IP_Address_Allocation.md) on how to have Enterprise IP Space allocated for your project, and added to your `yaml` structure.

## Managing Subnets Across Service Projects

Subnets are shared via IAM rules, and it's possible to have a subnet be visible/usable by multiple service projects.  Using a subnet across multiple service projects is discouraged.