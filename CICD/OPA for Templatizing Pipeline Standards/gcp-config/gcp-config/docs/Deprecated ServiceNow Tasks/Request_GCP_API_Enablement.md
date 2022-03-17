## Request GCP API Enablement:

# API Policies:
Be aware that only certain APIs are allowed to be assigned to a project for each environment type. For a full list of allowed APIs per environment please click <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources/-/blob/main/opa/data/service/apis.yml" target="_blank">here</a>.

APIs are evaluated by OPA or Open Policy Agent at the “opa-check” job of the pipeline for a given merge request. If you add an API that is not allowed for an environment it will fail the data integrity check. As a result the configuration will not be allowed to be applied and must be removed and the merge request resubmitted.

However as an alternative, exceptions can be made to an individual project to contain APIs that are not allowed otherwise. Adding a project and an API for that project under the section “allowedAPIsPerProject” to the yaml file <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources/-/blob/main/opa/data/service/apis-per-project.yml" target="_blank">here</a> will allow that lone project to contain the API without causing a violation.

For example, from production the project doms-eta-hr-lle is allowed to use the API calendar-json.googleapis.com.
```yaml
---
service:
  allowedAPIsPerProject:
    doms-eta-hr-lle:
    - calendar-json.googleapis.com
...
```

# File Location:
APIs for each project are located in a yaml file under a “serviceAPIs'' section. This is usually located within either the project.yml file or otherwise within a separate serviceapi.yml, service-usage.yml, or a file of a similar name depending on the project.
For example from production APIs are located at:
gcp-config/project_vars/doms-scf-lle/serviceapi.yml
or
gcp-config/project_vars/doms-cpe-kcc-prd/project.yml

For more information on APIs from resources provided from Google [click here](https://cloud.google.com/apis/docs/overview).

# Structure:
Below is a sample structure of a service API.
```yaml
---
serviceAPIs:
  {sample-API}.com:
  {sample-API}.com:
```
In many production projects service APIs are commonly included in the project.yml with other configurations at the bottom of a file.
Below is an example of how two service APIs are defined in production on line 16-18.
```yaml
---
billingDeptId: 90585
project:
  name: doms-bda-xpn-prd
  managed: true
  deletionProtect: true
  folderId: 778811484176
  billingAccount: 00C36A-CD0BDB-E543D0
  labels:
    billing-dept-id: 90585
    project-manager: eric-cherveny
    devops-lead: ramkishore-modukur
    environment-type: prd
    line-of-business: bda
    project-requestor: larry-mcmahon
serviceAPIs:
  cloudresourcemanager.googleapis.com:
  cloudasset.googleapis.com:
```

# API Enablement:
To enable an API to be used for a project, simply add it indented to the serviceAPIs section of the project, add a colon to the end of the API. Likewise removing an API is done by removing it from the list. If a serviceAPIs section is not listed it can be added to the project by adding the section to one of the yaml files, preferably the project.yml file.
From the example above the API logging.googleapis.com has been enabled for this project.
```yaml
---
billingDeptId: 90585
project:
  name: doms-bda-xpn-prd
  managed: true
  deletionProtect: true
  folderId: 778811484176
  billingAccount: 00C36A-CD0BDB-E543D0
  labels:
    billing-dept-id: 90585
    project-manager: eric-cherveny
    devops-lead: ramkishore-modukur
    environment-type: prd
    line-of-business: bda
    project-requestor: larry-mcmahon
serviceAPIs:
  cloudresourcemanager.googleapis.com:
  cloudasset.googleapis.com:
  logging.googleapis.com:
```
To help identify APIs that may provide value for your project Google APIs Explore [here](https://developers.google.com/apis-explorer) provides a searchable list and an explanation for various APIs. Otherwise explore [this](https://cloud.google.com/apis) list of popular APIs provided by Google.
