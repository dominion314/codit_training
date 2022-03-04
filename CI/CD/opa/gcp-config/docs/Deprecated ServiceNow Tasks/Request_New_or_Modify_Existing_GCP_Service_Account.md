## Request New or Modify Existing GCP Service Account

# File Location:
Service accounts are defined within the service-accounts.yml file located in the respective project folder in project_vars.
For example:
gcp-config/project_vars/{your-project]}/service-accounts.yml

# Service Account Resource:
Multiple service accounts can be defined within the same parameter file. The display name field is required for each service account. Labels are optional and can be defined for each service account as needed. A description is also optional and can be defined for each service account.

deletionProtect: Valid values are true or false. If the field is not defined, default value is false. When deletionProtect is set to true, deletion of service accounts within git and kubernetes clusters will not delete the service account in Google. This allows the service account to become unmanaged from kcc without deleting the service account in Google.

Default service-account.yml below:
```yaml
---
iamServiceAccounts:
  gitops-example-1:
    displayName: GitOps Example Service Account 1
    labels:
      app-name: "amazon-returns"
  gitops-example-2:
    displayName: GitOps Example Service Account 2
    description: used for testing
    deletionProtect: true
```
# Modifying Service Accounts:
To modify a service account simply remove the account and its configurations. Or on the other hand, to add a new account include it with the appropriate configuration.
