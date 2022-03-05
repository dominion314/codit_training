# Eunomia configuration for Templates Repo

## Quick Start
Initial bootstrap. Do this exactly one time.
```
kubectl apply -f eunomia-cr/clusters/<cluster name>/kcc-seed-namespace.yml
kubectl apply -f eunomia-cr/clusters/<cluster name>/kcc-seed-service-account.yml
kubectl apply -f eunomia-cr/clusters/<cluster name>/kcc-seed-role-binding.yml
kubectl apply -f eunomia-cr/clusters/<cluster name>/kcc-seed-cr.yml
```

## Directory Structure
```bash
├── eunomia-cr
│   ├── clusters
│   │   └── <cluster name>
│   │       ├── vars
│   │       │    ├── cluster_defaults.yml
│   │       │    └── projects.yml
│   │       ├── kcc-seed-namespace.yml
│   │       ├── kcc-seed-role-binding.yml
│   │       ├── kcc-seed-service-account.yml
│   │       └── kcc-seed-cr.yml
│   ├── templates
│   │   ├── gcp-namespaces-folders.yml.j2
│   │   ├── gcp-namespaces-projects.yml.j2
│   │   ├── gitops-config-folders.yml.j2 
│   │   ├── gitops-config-projects.yml.j2
│   │   ├── service-accounts-folders.yml.j2
│   │   └── service-accounts-projects.yml.j2 
│   └── readme.md
```
## Templates
* gcp-namespace-folders.yml.j2 - template for creating namespace with folder name and folder annotation
* gcp-namespace-projects.yml.j2 - template for creating namespace with project name and project annotation
* gitops-config-folders.yml.j2 - template for creating folder eunomia custom resource
* gitops-config-projects.yml.j2 - template for creating project eunomia custom resource
* service-accounts-folders.yml.j2 - template for creating folder namespace service account for eunomia
* service-accounts-project.yml.j2 - template for creating project namespace service account for eunomia

## Vars
* folders.yml
List of folders that will be managed by qa kcc cluster.
```yaml
folders:
  - {{ sample folder name 1 }}:
    gitUri: {{ repo uri }
    gitRef: {{ repo branch or tag }}
  - {{ sample folder name 2 }}:
```

* projects.yml
List of projects that will be managed by qa kcc cluster.
```yaml
projects:
  - {{ sample project name 1 }}:
    gitUri: {{ repo uri }}
    gitRef: {{ repo branch of tag }}
  - {{ sample project name 2 }}:
```

Project name is required
gitUri: is optional.  If not defined, gitUri will be https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources
gitRef: is optional.  If not defined, gitRef will be master

Sample projects.yml configuration
```yaml
projects:
  - domsdev-cpa-test001-lle:
    gitUri: https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources
    gitRef: master
  - domsdev-cpa-test002-lle:
```
## Seed CR
The seed CR will be installed in the eunomia-operator namespace in the doms-cpe-kcc-lle k8s cluster by the PaaS team.
The seed CR points to eunomia-cr/templates and eunomia-cr/vars directories.
The seed CR will render and apply new project and folder eunomia CRs based on data in projects.yml and folders.yml configuration files.
Seed CR will create the following objects for each project and folder listed in vars files:
* namespace --> gcp-{project name}
* service account in namespace --> eunomia-runner
* gitops config pointing to templates directory --> templates/gcp-project
*   and project vars directory --> test_vars/gcp_project/{project name}
