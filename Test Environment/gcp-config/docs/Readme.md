# Getting Started

To get started building and managing your own infrastructure with GitOps, follow the general guidelines below.  This will go over how to onboard to NetX with either a "greenfield" or "brownfield" deployment.  It will also point you to the correct documentation while providing high level objectives for you to plan out for your team(s).

Here are the overall considerations you should take when building or managing infrastructure in GCP:

1. Is a migration necessary? What about Openshift?
2. NetX Provisioning (VPC and Network)
3. Managing and Creating Service Projects
4. Managing IAM Permissions and Service Accounts
5. Planning and Managing Subnets for Compute
6. Planning and Requesting Firewall Rules

## Is a Migration Necessary?  What about Openshift?

If you don't have any existing resources in GCP, feel free to skip this section.

However if you DO have resources in a Google project, you can easily determine if you need to move your GCE resources by looking at the what `Network` they are deployed to.  All NetX VPCs have been named with nomenclature that contains `-nx-` in the middle of the name.   NetX and Legacy VPCs can indeed co-exist in the same host project, however these networks use completely different resources for connectivity.

If your GCE resources do not have `-nx-` within the name, a migration is likely needed.  A migration will involve moving or recreating your GCE resources to NetX.  To move these resources, it's ultimately up to the application owner on how they'd like to move these compute resources.  Some may want to lift and shift, others will create additional resources in tandem and shifting workloads over slowly.  If your host project remains the same, your service projects can simply be managed with GitOps and you can continue to use it as you have.

> **NOTE: If your compute  resources are found in `doms-xpn-project`, or a new host project is required, you will not be able to retain your existing service projects for GCE use.**

When evaluating your options to migrate, the infrastructure teams encourage all staff to consider onboarding to the Kohl's platform which uses both NetX and shared Openshift clusters.  These clusters abstract most infrastructure away from you, to allow you to focus on your codebase and deployments.  If you're unsure if these environments will suit your needs, open a conversation with Product Owners/Managers to determine the right approach.

## NetX Provisioning (VPC and Network)

While it's true that GitOps enables customers to provision most resources they need with nothing more than a Pull Request (PR), customers shouldn't need to learn how to provision network infrastructure.  This is a one time PR that is submitted to create your new NetX VPC via GitOps while also ensuring all of the appropriate network "plumbing" is in place.  

The Cloud Network Team will provision your new NetX environment and all of the backend connectivity that comes with it. When your team is ready, please fill out the following form: [NetX On-Boarding](https://docs.google.com/forms/d/e/1FAIpQLSfTPbj1-_WRqpcYjTORc5XFYh4kuB7yS0E4lvGYo5ptOptVcA/viewform)

Network staff will retain management of the HOST project (where the VPC and network resources reside), though customers are able to request resources and configurations to be deployed there.  Proceed with the following sections to learn how to provision resources you need

## Managing and Creating Projects

Generally, the service project is the project that customers use to deploy their compute or storage workloads.  GCE instances, BigQuery, PubSub, ILBs, ELBs, etcs all find their way to the a service project.  A service project can only be associated to a single host project

Host projects group together network resources to ensure proper management by Kohl's network teams.  This is usually addressed in the previous section.  

Managing an existing service project (which is possible in some scenarios) and creating a new one requires the same steps.  Simply create the project definition, and request a merge to master.  If the project already exists, the operators supporting this repo will manage it.  If the project doesn't exist, it will create it.

> KEY CONCEPT: Resources created in this repository will be managed by various operators if the resource already exists.  If it does not exist, it will create the object.

> Note: Customers manage their own resources in their service projects.  While Network will initially provision settings in their host projects, customers are able to see and request changes to those resources.  In host projects, customers are 100% responsible for requesting and managing their own subnetwork resources.

The documentation for building project definitions in this repo refer to some of the following documents

- [Projects/](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/tree/main/docs/Projects)
- [Projects/Project_Jump_Start_Guide.md](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Project_Jump_Start_Guide.md)
- [Projects/Service_Projects.md](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Service_Projects.md)

## Managing IAM Permissions and Service Accounts

If you already have IAM and service accounts set up in your existing projects, you can skip this section, however any new permissions need to be done through GitOps.  

To build your IAM policy sets and/or service accounts, refer to these details to help build your config file in the appropriate project folder

- [Projects/Parameter_Schema.md](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Parameter_Schema.md)

## Planning and Managing Subnets for Compute

When IAM has been set up and your [service project has been connected to the host project](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Service_Projects.md#4-attach-host-project-to-the-service-project), getting subnetworks shared to the project is now possible.

The process will require code to be deployed to your host project with permission information.  Here are some documents to help with this configuration.

- [Network/IP_Address_Allocation](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/IP_Address_Allocation.md)
- [Network/Adding_Subnetworks_To_Service_Projects.md](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/Adding_Subnetworks_To_Service_Projects.md)
- [Network/VPC_Networks_Subnetworks.md](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Network/VPC_Networks_Subnetworks.md#subnetworks)

## Planning and Requesting Firewall Rules

Once you have IAM, service accounts, and subnetworks available to your service project, firewall rules need to be considered to permit access into most GCE you create.  The following documents will help guide you through planning and request FW rules.

- [Firewall/Planning_Firewall_Rules.md](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Firewall/Planning_Firewall_Rules.md)
- [Firewall/VPC_Firewalls.md](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Firewall/VPC_Firewalls.md)