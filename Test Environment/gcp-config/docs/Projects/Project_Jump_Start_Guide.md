# Project Jump Start Guide
- [Project Jump Start Guide](#project-jump-start-guide)
  - [Creating and managing projects](#creating-and-managing-projects)
  - [What is the gitops process?](#what-is-the-gitops-process)
  - [Before you begin](#before-you-begin)
  - [Your Project Scenario](#your-project-scenario)
    - [New Service Project - Connecting to existing Host Project](#new-service-project---connecting-to-existing-host-project)
    - [New Host Project](#new-host-project)
- [Appendix](#appendix)
  - [NetX Project Folder ID Lookup Table](#netx-project-folder-id-lookup-table)
## Creating and managing projects
Google Cloud projects form the basis for creating, enabling, and using all Google Cloud services including managing APIs, enabling billing, adding and removing collaborators, and managing permissions for Google Cloud resources.

This page explains how to create and manage Google Cloud projects using Kohl's gitops process.
## What is the gitops process?
Google Cloud resources can now be configured using Kohl's developed yaml definitions for gcp resources stored in this centralized git repo - [gcp-config](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config).  All gcp resource configurations are stored in a folder named after the gcp project within the project_vars directory.  Pick any project folder in the repo to see its gcp resource configuration files.
[Example Folder kohls-cpe-sample-lle](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/tree/main/project_vars/kohls-cpe-sample-lle)

To create and modify gcp resources using the gitops process, the following steps need to occur.
1. Create a branch
2. Create a new project folder under project_vars directory if it doesn't already exist
3. Configure gcp resource yaml files in that project folder
4. Submit a pull request

After pull request tests have completed successfully, the pull request will be approved and merged by a Cloud Platform engineer.  Once merged, the gcp resources will be configured.

Too see some of the types of gcp resources that can be created and managed using the gitops process, please reference the following document.

[Gitops GCP Resource Definitions](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Service_Projects.md#2-create-iam-policies)
## Before you begin
Gather the following the following information that will be used when creating a Google Cloud project.

1.  Determine the name of the project - the naming convention for projects is: kohls-{lob}-{app}-{environment-type}.  Where lob is line of business, app is the application or business domain and environment type is ops, sbx, lle, hle or prd.  Make sure the project name is unique and has not already been used.
2.  Determine the Folder ID that the project should use.  Reference Project Folder ID Lookup Tables at the end of this document.
3.  Determine billing department id that project will be associated with.  Any costs incurred within the project will be charged against that billing department id.
4.  Determine project requestor. *** Add purpose here ***
5.  Determine project manager. *** Add purpose here ***
6.  Determine devops lead. *** Add purpose here ***
7.  Determine line of business (same as in Step 1).  *** Add purpose here ***
8.  Determine environment type (same as in Step 1).  *** Add purpose here ***

## Your Project Scenario
There are two types of gcp projects that can be created and managed, service projects and host projects.

**Service Projects** are gcp projects that application teams will create to contain all of their gcp resources that get deployed.

**Host Projects** are gcp projects that contain all the network configurations that a service project will use.  Service projects are "linked" to Host projects so that the service project can utilize the network configurations stored in the host project.  Many service projects can be connected to the same host project.

### New Service Project - Connecting to existing Host Project
This will be the most common scenario for application teams.  In this scenario, the host project that the service project will be connected to already exists.  Therefore, only the service project needs to be created.  Follow instructions found here in [Creating a service project](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Service_Projects.md).
### New Host Project
This scenario is most likely to be deployed by a Cloud Network Engineer.  Users who are not a Cloud Network Engineer should first consult with the Network team as this configuration can be complex for teams not familiar with Google networking.

To create a host project, follow instructions found here in [How to create/manage a net x environment host project ](https://gitlab.com/kohls/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Host_Projects.md#how-to-createmanage-a-netx-environment-host-project).
# Appendix
## NetX Project Folder ID Lookup Table
#
### Kohl's - Non-Production
#
| Product Domain                      | Folder ID    |
| :---------------------------------- | :------------|
| EnterpriseServices-Credit-Payments  | 859213288423 |
| merch-mkt-analytics                 | 963520663007 |
| supply-field-people                 | 857045434788 |
| ccx                                 | 124759181101 |
| architecture                        | 872364499101 |
| Security                            | 882166644980 |
| infra-ops                           | 345254712059 |
#
### Kohl's - Production
#
| Product Domain                      | Folder ID    |
| :---------------------------------- | :------------|
| EnterpriseServices-Credit-Payments  | 155882274299 |
| merch-mkt-analytics                 | 217021366087 |
| supply-field-people                 | 921350738615 |
| ccx                                 | 121961327479 |
| architecture                        | 863157377269 |
| Security                            | 726913521927 |
| infra-ops                           | 980929416788 |
#
### Kohl's - Platform
#
| Product Domain                      | Folder ID    |
| :---------------------------------- | :------------|
| Production Platform                 | 48229324135  |
| Non-Production Platform             | 1057338141298|
#
