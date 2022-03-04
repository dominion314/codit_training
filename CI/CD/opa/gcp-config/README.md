# If you are having trouble accessing this repo or submitting PRs please contact kt-cpa@kohls.com #
Comment, suggestions, bugs? Please fil out this form so we can make this the best experince for all..
https://docs.google.com/forms/d/1I8v_JZoSCTl17VZpiXcPZ0VcxW-xrJOXTsvV_uRxpYI

# GitOps Configuration Repo for GCP Infrastructure (NetX)

This repo and the files within contain YAML definitions of GCP infrastructure.  The arrangement of managed network infrastructure are considered to Kohl's GCP 2.0 or NetX by name, as the legacy networks are managed elsewhere.  This repo replaces a variety of Service Now forms.

The repo currently is capable of deploying a GCP foundation in which you can build your application or workflow on top of.  The current capabilities of the GitOps process includes, but are not limited to management of:

- Network Infrastructure (NetX), both to other GCP projects and to on-premises locations
- IAM Permissions and Service Accounts
- New Projects
- Storage Buckets
- Pub/Sub
- BigQuery Datasets 

## What is GitOps?

GitOps is a Continuous Delivery methodology that empowers developers to manage their infrastructure like their applications, using developer tools they are already familiar with (Git and Gitlab).

Exposing GCP Infrastructure with GitOps means customers have a clear picture of how their environment is supposed to look like, by providing an intended, declarative endstate.  Pull Requests are used to approve of resource requests and various CI checks will run "continuously" to ensure the code merged in is stable, error free, and will abide by Kohl's policy. 

## What is NetX?

### What Does NetX Mean?

NetX is a codeword that describes the next iteration of GCP architecture that Kohl's is deploying.  Think of it as versioning of the infrastructure type that all resources in GCP are built upon.

### Why bother with NetX?

The foundational Google infrastructure that has been put together by various teams used very early iterations of code practices and Google products.  

Over the years that Kohl's has been deployed in Google Cloud Platform, there have been lessons learned over management of our infrastructure at scale.  Quotas became a key component to monitor, complexity of environments grew, and cost of communication between different projects increased.

Networking products that are being used in Google will no longer be supported in the coming years.  As support goes away, the existing architecture will not be able to create or modify connectivity to and from your projects.

At this time, NetX offers the following benefits for any product team:

- **Consolidated VPC Design** - Service projects within the same line of business and environment will talk directly, free of VPN limitations.
- **GitOps Methodologies** - the CPE team has wrapped the NetX environments with our new GitOps processes.  A Pull Request and peer review is all you need to deploy new resources to your environment.  Service Now forms are a thing of the past with most requests!
- **Access to Future Google Resources** - The NetX/GitOps processes will be updated repeatedly in the future to offer whatever new features Google has to offer.  The old environments will be maintained for some time, but new features will only arrive on the NetX environment.
- **Dedicated Connectivity to On-Prem** - Multiple hops to on-prem datacenters is a thing of the past.  Google has released the Partner Interconnect product that allows direct L2 connectivity to customer datacenters.  With this, a customer is able to get their own dedicated circuit, while also specifying the speed of the link (starting at 50Mbps) 

## Getting Started!

Please visit [docs/Readme.md](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Readme.md).
<!-- 
## Structure


```bash
├── environment-vars # Not applicable to current repo features
│   ├── LOB-ABBRV
│   │   ├── ops|sbx|lle|hle|prd
│   │   ├── ...
│   │   └── ...
├── global-vars # variables to be tracked or applied globally
│   ├── global-firewall.yml
│   └── route-vars.yml
├── lob-vars # variables to be applied to a line of business
│   ├── LOB-ABBRV
│   │   └── lob-firewall.yml
│   └── ...
└── project-vars # Project/VPC specific variables
    ├── PROJECT-NAME01
    │   ├── project.yml
    │   ├── VPC1-NAME-firewall.yml
    │   ├── VPC1-NAME-interconnect.yml
    │   ├── VPC1-NAME-network.yml
    │   ├── VPC1-NAME-networkpeering.yml
    │   ├── VPC1-NAME-subnetwork-gke.yml
    │   ├── VPC1-NAME-subnetwork-std.yml
    │   ├── VPC2-NAME-firewall.yml
    │   ├── VPC2-NAME-interconnect.yml
    │   ├── VPC2-NAME-network.yml
    │   ├── VPC2-NAME-networkpeering.yml
    │   ├── VPC2-NAME-subnetwork-gke.yml
    │   ├── VPC2-NAME-subnetwork-std.yml
    │   └── ...
    └── ...
``` -->
