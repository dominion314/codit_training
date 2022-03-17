# Add/Modify GCP Group IAM Roles

## IAM Policies:
Be aware that only certain roles are allowed to be assigned to a group for each environment type. For a full list of allowed roles per environment please click <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources/-/blob/main/opa/data/iam/iam-roles.yml" target="_blank">here</a>.

Group roles, as well as the other two forms of IAM roles users and service accounts, are evaluated by OPA or Open Policy Agent at the “opa-check” job of the pipeline for a given merge request. If you add a role that is not allowed for an environment it will fail the data integrity check. As a result the configuration will not be allowed to be applied and must be removed and the merge request resubmitted. However as an alternative, exceptions per-project can be made as discussed below.

## File Location:
Group IAM roles are expected to be defined within an iam-policy-members.yml file located in their respective project folder in project_vars.
For example:
gcp-config/project_vars/{your-project}/iam-policy-members.yml


For more information on roles and their permissions, please reference [Google Understanding Roles Documentation](https://cloud.google.com/iam/docs/understanding-roles).

## Structure:
Below is a sample structure of a GCP group IAM role within the iam-policy-members.yml file.
```yaml
---
iamPolicyMembers:
  groupsByEmail:
    {group-email}@{address}.com:
      roles:
      - {group-role}
      - {group-role}
```
The third line “groupsByEmail” designates that these rules are group roles, the next lists the email of the group that defines the members of the group. Following this the file lists the role(s) that the group will have.

Below is an example of valid GCP group IAM roles with two groups.
```yaml
---
iamPolicyMembers:
  groupsByEmail:
    gcp-iaas-cpa-devops-admin@doms.com:
      roles:
      - compute.loadBalancerAdmin
      - bigquery.dataViewer
    gcp-iaas-cpa-devops-l3@doms.com:
      roles:
      - bigquery.dataViewer
      - bigtable.viewer
```

# Modifying Group Roles:
To modify the roles for a particular group simply remove or add to the roles section of the file. Or on the other hand, to remove the group entirely, remove both of the group email and the correlating role(s) below it. To first create GCP group IAM roles you will have to first create the iam-policy-members.yml in the project folder and follow the proper structure provided above.
For example this iam-policy-members.yml file will be changed to include the role “compute.networkUser” in the group.
```yaml
---
iamPolicyMembers:
  groupsByEmail:
    gcp-iaas-cpa-devop-admin@doms.com:
      roles:
      - compute.storageAdmin
      - iam.serviceAccountUser
```
Therefore it must follow the correct indentation and be preceded with a dash as below.
```yaml
---
iamPolicyMembers:
  groupsByEmail:
    gcp-iaas-cpa-devop-admin@doms.com:
      roles:
      - compute.storageAdmin
      - iam.serviceAccountUser
      - compute.networkUser
```
## Additional Concerns:
Exceptions can be made to an individual project to contain roles that are not allowed otherwise. Adding a project and roles for that project to the yaml file <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/cloud-resources/-/blob/main/opa/data/iam/iam-roles-per-project.yml" target="_blank">here</a> will allow that lone project to contain those roles without causing a violation. In addition, for each role it must define whether it is allowed to be used by groups, service accounts, and or users. To have your listed roles as a group role it must have allowedForGroups as true.

The following is a sample for that structure.
```yaml
   {project-name}:
      roles:
      - {role-name}:
          allowedForGroups: {true OR false}
          allowedForServiceAccounts: {true OR false}
          allowedForUsers: {true OR false}
      - {role-name}:
          allowedForGroups: {true OR false}
          allowedForServiceAccounts: {true OR false}
          allowedForUsers: {true OR false}
```
You may find other section designations within the iam-policy-members.yml file such as serviceAccountsByEmail and usersByEmail which lists roles given to service accounts and users respectively. Therefore only the email and their corresponding roles under the section groupsByEmail will contain the group roles.

For example the file below has two groups gcp-iaas-cpa-devop-admin and gcp-iaas-cpa-devop-l3.
```yaml
---
iamPolicyMembers:
  groupsByEmail:
    gcp-iaas-cpa-devop-admin@doms.com:
      roles:
      - compute.storageAdmin
      - iam.serviceAccountUser
      - storage.admin
      - compute.instanceAdmin
      - compute.networkUser
    gcp-iaas-cpa-devop-l3@doms.com:
      roles:
      - compute.storageAdmin
      - iam.serviceAccountUser
      - storage.admin
      - compute.instanceAdmin
      - compute.networkUser
 serviceAccountsByEmail:
    bda-devops@doms-bda-dse-lle.iam.gserviceaccount.com:
      roles:
      - compute.storageAdmin
```
