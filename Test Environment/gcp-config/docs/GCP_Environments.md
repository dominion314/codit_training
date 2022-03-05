# Gitops Google Environments
The intent of this document is to explain how the different Google GCP organizations will be utilized to support the following gitops environments - dev, qa and production. 

## Google Dev Environment
When using the project.yml input vars file (explained here: link to be added), use the appropriate folderID below to make sure you are creating your resources in the appropriate folder for your team.
```
┌───────────────────────────┐       ┌───────────────────────────────────────────────────┐
│          Minikube         │       │                  GCP Organization                 │ 
│ ┌───────────────────────┐ │       │    dev.doms.com                                  │
│ │ k8s namespace         │ │       │       │                                           │
│ │   cnrm-system         │ │       │       └── Billing 00C36A-CD0BDB-E543D0            │
│ │ secret                │ │       │               │                                   │
│ │   gcp_key.json        │ │       │               ├── gitops-dev-cne (144994841496)   │
│ └───────────────────────┘ │       │               │       │                           │
│                           │       │               │       └── {CNE Projects go here}  │
│                           │ ====> │               │                                   │
│ ┌───────────────────────┐ │       │               ├── gitops-dev-cpa (922938220950)   │
│ │ k8s namespace         │ │       │               │       │                           │                       
│ │   gcp-doms-cpa-lle   │ │       │               │       └── {CPA Projects go here}  │
│ │ k8s annotation        │ │       │               │                                   │ 
│ │   domsdev-cpa-lle    │ │       │               └── gitops-dev-paas (510585446647)  │
│ └───────────────────────┘ │       │                       │                           │              
│                           │       │                       └── {PaaS Projects go here} │
└───────────────────────────┘       └───────────────────────────────────────────────────┘
```
The following service accounts and team roles will have permissions to create projects and project resources in the above folders in the dev.doms.com Google GCP organization.

### gitops-dev-cne
This setup is for the CNE team.

**Accounts**
* cnrm-system-gitops-dev-cne@doms-cpa-lle.iam.gserviceaccount.com
* Team role: TBD (waiting on new team roles to be created)

**Permissions**
* Billing Account User (applied at doms.com)
* Project Owner (applied at gitops-dev-cne folder in dev.doms.com)
* Project Creator (applied at gitops-dev-cne folder in dev.doms.com)
* Compute Shared VPC Admin (applied at gitops-dev-cne folder in dev.doms.com)

### gitops-dev-cpa
This setup is for the CPA team.

**Accounts**
* cnrm-system-gitops-dev-cpa@doms-cpa-lle.iam.gserviceaccount.com
* gcp-iaas-cpa-devops-l3@doms.com 

**Permissions**
* Billing Account User (applied at doms.com)
* Project Owner (applied at gitops-dev-cpa folder in dev.doms.com)
* Project Creator (applied at gitops-dev-cpa folder in dev.doms.com)
* Compute Shared VPC Admin (applied at gitops-dev-cpa folder in dev.doms.com)

### gitops-dev-paas
This setup is for the PaaS team.

**Accounts**
* cnrm-system-gitops-dev-paas@doms-cpa-lle.iam.gserviceaccount.com
* gcp-xpaas-openshift-admin@doms.com

**Permissions**
* Billing Account User (applied at doms.com)
* Project Owner (applied at gitops-dev-paas folder in dev.doms.com)
* Project Creator (applied at gitops-dev-paas folder in dev.doms.com)
* Compute Shared VPC Admin (applied at gitops-dev-paas folder in dev.doms.com)

## Google QA Environment
The QA gitops process will have automated testing of gcp resource lifecycle management in the qa.doms.com Google organization.  Google's Config Connector and Eunomia K8S operators will be installed in a lle GKE cluster built in the project doms-cpe-kcc-lle.

The cloud-resources git repo will be integrated with Eunomia running in a GKE cluster.  Google Config Connector will be running in the same GKE cluster and will be integrated with GCP.  The GKE cluster will use workload identity and will bind the gcp service account cnrm-system-qa-cpe@doms-cpe-kcc-lle.iam.gserviceaccount.com to the k8s service account used within Google Config Connector namespace: cnrm-system

![Alt Text](https://confluence.doms.com:8443/download/attachments/101226947/gitops-qa-deployment.png?api=v2)

### Accounts & Roles
Account:
* cnrm-system-qa-cpe@doms-cpe-kcc-lle.iam.gserviceaccount.com

Roles:
* Billing Account User (applied at doms.com)
* Project Owner (applied at qa-doms.com/ Billing 00C36A-CD0BDB-E543D0 folder in qa.doms.com)
* Project Creator (applied at qa-doms.com/Billing 00C36A-CD0BDB-E543D0 folder in qa.doms.com)
* Compute Shared VPC Admin (applied at qa-doms.com/Billing 00C36A-CD0BDB-E543D0 folder in qa.doms.com)

Account:
* inspec-qa-cpe@doms-cpe-kcc-lle.iam.gserviceaccount.com

Roles:
* Organization Viewer (applied at qa.doms.com)
* Folder Viewer (applied at qa.doms.com)
* Project Viewer (applied at qa.doms.com)
* Security Reviewer (applied at qa.doms.com)

## Google Production Environment
The production gitops process will lifecycle manage gcp resources within the doms.com Google organization.  This includes management of prd, hle and lle projects within doms.com.  Google's Config Connector and Eunomia K8S operators will be installed in a production GKE cluster built in the project doms-cpe-kcc-prd.

The cloud-resources and gcp-config git repos will be integrated with Eunomia running in a GKE cluster.  Google Config Connector will be running in the same GKE cluster and will be integrated with GCP.  The GKE cluster will use workload identity and will bind the gcp service account cnrm-system-cpe@doms-cpe-kcc-prd.iam.gserviceaccount.com to the k8s service account used within Google Config Connector namespace: cnrm-system

![Alt Text](https://confluence.doms.com:8443/download/attachments/101226947/gitops-prod-deployment.png?api=v2)

### Accounts & Roles
Account:
* cnrm-system-cpe@doms-cpe-kcc-prd.iam.gserviceaccount.com

Roles:
* Billing Account User (applied at doms.com)
* Project Owner (applied at doms.com/Billing 00C36A-CD0BDB-E543D0 folder in doms.com) - will not enable until we have a process to enable management of brown field projects
* Project Creator (applied at doms.com/Billing 00C36A-CD0BDB-E543D0 folder in doms.com)
* Compute Shared VPC Admin (applied at doms.com/Billing 00C36A-CD0BDB-E543D0 folder in doms.com)

Account:
* inspec-cpe@doms-cpe-kcc-prd.iam.gserviceaccount.com

Roles:
* Organization Viewer (applied at doms.com)
* Folder Viewer (applied at doms.com)
* Project Viewer (applied at doms.com)
* Security Reviewer (applied at doms.com)
