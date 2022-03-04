# Gitops Google Environments
The intent of this document is to explain how the different Google GCP organizations will be utilized to support the following gitops environments - dev, qa and production. 

## Google Dev Environment
When using the project.yml input vars file (explained here: link to be added), use the appropriate folderID below to make sure you are creating your resources in the appropriate folder for your team.
```
┌───────────────────────────┐       ┌───────────────────────────────────────────────────┐
│          Minikube         │       │                  GCP Organization                 │ 
│ ┌───────────────────────┐ │       │    dev.kohls.com                                  │
│ │ k8s namespace         │ │       │       │                                           │
│ │   cnrm-system         │ │       │       └── Billing 00C36A-CD0BDB-E543D0            │
│ │ secret                │ │       │               │                                   │
│ │   gcp_key.json        │ │       │               ├── gitops-dev-cne (144994841496)   │
│ └───────────────────────┘ │       │               │       │                           │
│                           │       │               │       └── {CNE Projects go here}  │
│                           │ ====> │               │                                   │
│ ┌───────────────────────┐ │       │               ├── gitops-dev-cpa (922938220950)   │
│ │ k8s namespace         │ │       │               │       │                           │                       
│ │   gcp-kohls-cpa-lle   │ │       │               │       └── {CPA Projects go here}  │
│ │ k8s annotation        │ │       │               │                                   │ 
│ │   kohlsdev-cpa-lle    │ │       │               └── gitops-dev-paas (510585446647)  │
│ └───────────────────────┘ │       │                       │                           │              
│                           │       │                       └── {PaaS Projects go here} │
└───────────────────────────┘       └───────────────────────────────────────────────────┘
```
The following service accounts and team roles will have permissions to create projects and project resources in the above folders in the dev.kohls.com Google GCP organization.

### gitops-dev-cne
This setup is for the CNE team.

**Accounts**
* cnrm-system-gitops-dev-cne@kohls-cpa-lle.iam.gserviceaccount.com
* Team role: TBD (waiting on new team roles to be created)

**Permissions**
* Billing Account User (applied at kohls.com)
* Project Owner (applied at gitops-dev-cne folder in dev.kohls.com)
* Project Creator (applied at gitops-dev-cne folder in dev.kohls.com)
* Compute Shared VPC Admin (applied at gitops-dev-cne folder in dev.kohls.com)

### gitops-dev-cpa
This setup is for the CPA team.

**Accounts**
* cnrm-system-gitops-dev-cpa@kohls-cpa-lle.iam.gserviceaccount.com
* gcp-iaas-cpa-devops-l3@kohls.com 

**Permissions**
* Billing Account User (applied at kohls.com)
* Project Owner (applied at gitops-dev-cpa folder in dev.kohls.com)
* Project Creator (applied at gitops-dev-cpa folder in dev.kohls.com)
* Compute Shared VPC Admin (applied at gitops-dev-cpa folder in dev.kohls.com)

### gitops-dev-paas
This setup is for the PaaS team.

**Accounts**
* cnrm-system-gitops-dev-paas@kohls-cpa-lle.iam.gserviceaccount.com
* gcp-xpaas-openshift-admin@kohls.com

**Permissions**
* Billing Account User (applied at kohls.com)
* Project Owner (applied at gitops-dev-paas folder in dev.kohls.com)
* Project Creator (applied at gitops-dev-paas folder in dev.kohls.com)
* Compute Shared VPC Admin (applied at gitops-dev-paas folder in dev.kohls.com)

## Google QA Environment
The QA gitops process will have automated testing of gcp resource lifecycle management in the qa.kohls.com Google organization.  Google's Config Connector and Eunomia K8S operators will be installed in a lle GKE cluster built in the project kohls-cpe-kcc-lle.

The cloud-resources git repo will be integrated with Eunomia running in a GKE cluster.  Google Config Connector will be running in the same GKE cluster and will be integrated with GCP.  The GKE cluster will use workload identity and will bind the gcp service account cnrm-system-qa-cpe@kohls-cpe-kcc-lle.iam.gserviceaccount.com to the k8s service account used within Google Config Connector namespace: cnrm-system

![Alt Text](https://confluence.kohls.com:8443/download/attachments/101226947/gitops-qa-deployment.png?api=v2)

### Accounts & Roles
Account:
* cnrm-system-qa-cpe@kohls-cpe-kcc-lle.iam.gserviceaccount.com

Roles:
* Billing Account User (applied at kohls.com)
* Project Owner (applied at qa-kohls.com/ Billing 00C36A-CD0BDB-E543D0 folder in qa.kohls.com)
* Project Creator (applied at qa-kohls.com/Billing 00C36A-CD0BDB-E543D0 folder in qa.kohls.com)
* Compute Shared VPC Admin (applied at qa-kohls.com/Billing 00C36A-CD0BDB-E543D0 folder in qa.kohls.com)

Account:
* inspec-qa-cpe@kohls-cpe-kcc-lle.iam.gserviceaccount.com

Roles:
* Organization Viewer (applied at qa.kohls.com)
* Folder Viewer (applied at qa.kohls.com)
* Project Viewer (applied at qa.kohls.com)
* Security Reviewer (applied at qa.kohls.com)

## Google Production Environment
The production gitops process will lifecycle manage gcp resources within the kohls.com Google organization.  This includes management of prd, hle and lle projects within kohls.com.  Google's Config Connector and Eunomia K8S operators will be installed in a production GKE cluster built in the project kohls-cpe-kcc-prd.

The cloud-resources and gcp-config git repos will be integrated with Eunomia running in a GKE cluster.  Google Config Connector will be running in the same GKE cluster and will be integrated with GCP.  The GKE cluster will use workload identity and will bind the gcp service account cnrm-system-cpe@kohls-cpe-kcc-prd.iam.gserviceaccount.com to the k8s service account used within Google Config Connector namespace: cnrm-system

![Alt Text](https://confluence.kohls.com:8443/download/attachments/101226947/gitops-prod-deployment.png?api=v2)

### Accounts & Roles
Account:
* cnrm-system-cpe@kohls-cpe-kcc-prd.iam.gserviceaccount.com

Roles:
* Billing Account User (applied at kohls.com)
* Project Owner (applied at kohls.com/Billing 00C36A-CD0BDB-E543D0 folder in kohls.com) - will not enable until we have a process to enable management of brown field projects
* Project Creator (applied at kohls.com/Billing 00C36A-CD0BDB-E543D0 folder in kohls.com)
* Compute Shared VPC Admin (applied at kohls.com/Billing 00C36A-CD0BDB-E543D0 folder in kohls.com)

Account:
* inspec-cpe@kohls-cpe-kcc-prd.iam.gserviceaccount.com

Roles:
* Organization Viewer (applied at kohls.com)
* Folder Viewer (applied at kohls.com)
* Project Viewer (applied at kohls.com)
* Security Reviewer (applied at kohls.com)
