# OPA:
Open Policy Agent or OPA is a data validation check used in the gcp-config pipeline. It is used to validate that the roles, APIs, and several other forms of configurations do not violate our data standards. This prevents project changes from being merged that are invalid to be used for Google Cloud or contain security risks. The policies that OPA currently runs checks are for cloud connectivity, firewall egress, firewall ingress, bandwidth limit, ​​service APIs, iam roles, custom iam roles, and project settings. In the case that your project violates our policies, OPA should in most cases provide assistance to identify why the job has failed when viewing the job in the pipeline.

# OPA Exceptions:
If your project requires for your use case a role or API that violates our policies you can request a per-project exception to use that role/API. However it is greatly preferred to remove the violating role/API if possible. Follow the steps below to have an exception added, it must be approved by the platform and security team.
- First, clone the cloud-resources repo located <a href="https://gitlab.com/kohls/infra/platform_enablement/cloud-config/cloud-resources" target="_blank">here</a> to make a merge request for your per-project exception.
- Second, add to the yaml file located <a href="https://gitlab.com/kohls/infra/platform_enablement/cloud-config/cloud-resources/-/blob/main/opa/data/iam/iam-roles-per-project.yml" target="_blank">here</a> for iam and custom iam roles under cloud-resources/opa/data/iam/iam-roles-per-project.yml or <a href="https://gitlab.com/kohls/infra/platform_enablement/cloud-config/cloud-resources/-/blob/main/opa/data/service/apis-per-project.yml" target="_blank">here</a> for APIs under cloud-resources/opa/data/service/apis-per-project.yml.
- Follow the structure in the file of project name and then the iam role/API as shown below. Iam roles can be set to be allowed for users, groups, and service accounts, only set to true for what you need to use.
### Iam Roles:
```yaml
    kohls-cpa-lle:
      roles:
      - cloudsql.viewer:
          allowedForGroups: true
          allowedForServiceAccounts: true
          allowedForUsers: false
```
### APIs:
```yaml
    kohls-cpa-lle:
    - cloudtrace.googleapis.com
```
- Next, create a branch with your change, create a merge request, and have it reviewed and merged into main. You can request a review in the NetX GitOps and Firewall Q&A Webex space.
- Lastly, push a new commit to your merge request for the gcp-config repo to update the OPA data standards. Based off of how GitLab works only rerunning the job will not use the changes from your new merge request and requires a new commit to your branch.