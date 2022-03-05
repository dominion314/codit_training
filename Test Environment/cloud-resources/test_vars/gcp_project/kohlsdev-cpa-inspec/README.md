# Hierarchy Support for Parameter Files (yaml vars)
## Eumomia Configuration for domsdev-cpa-inspec project
After installation of Eunomia in Minikube or GKE, eunomia needs to be configured to setup a k8s service account that has rights to the namespace whose CRs will be managed.  A sample configuration for domsdev-cpa-inspec namespace is explained below.

Eunomia also needs to be configured to reference the templates and parameter (yml var) files that should be monitored.  A sample configuration for gcp project domsdev-cpa-inspec is explained below.

Eunomia configuration files are found here in the repo - templates/eunomia/eunomia/minikube-mark
    eunomia-cr.yml
    eumovia-sa.yml

eunomia-cr.yml contents
```
apiVersion: eunomia.doms.io/v1alpha1
kind: GitOpsConfig
metadata:
  name: domsdev-cpa-inspec
  namespace: gcp-domsdev-cpa-inspec
spec:
  templateSource:
    uri: https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources.git
    ref: CPA-2249
    contextDir: templates/gcp-project
  parameterSource:
    uri: https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources.git
    ref: CPA-2249
    contextDir: test_vars/gcp_project/domsdev-cpa-inspec
  triggers:
  - type: Change
  #- type: Periodic
    #cron: '*/1 * * * *'
  serviceAccountRef: eunomia-runner
  templateProcessorImage: quay.io/domstechnology/eunomia-jinja:latest
  resourceHandlingMode: CreateOrMerge
  resourceDeletionMode: Delete

```
eunomia-sa.yml
```
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: eunomia-runner
  namespace: "gcp-domsdev-cpa-inspec"
subjects: 
- kind: ServiceAccount
  name: eunomia-runner
  namespace: "gcp-domsdev-cpa-inspec"
roleRef:
  kind: ClusterRole
  name: admin
  apiGroup: rbac.authorization.k8s.io  
---
# Service accounts for app namespaces
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eunomia-runner
  namespace: "gcp-domsdev-cpa-inspec"
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: eunomia-operator-cluster-admin-gcp-domsdev-cpa-inspec
  namespace: "gcp-domsdev-cpa-inspec"
subjects:
- kind: ServiceAccount
  name: eunomia-runner
  namespace: "gcp-domsdev-cpa-inspec"
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
---

```
## 
hierarchy.lst file in the project folder defines folder precedence of parameter files.  The directories are relative to the project folder itself for this project.
```
../../gcp_default
../../gcp_lob
../../gcp_env/lle
./
```
Parameter files are processed in folder list from top to bottom.

**If folders are defined, at least one parameter file needs to be in each folder, otherwise an error will occur in the Eunomia template processor.**

For more information on how Eunomia hierarchies work, click on the following link - https://github.com/domsTechnology/eunomia#variable-hierarchy
