# ServiceNow Task Deprecation Documentation

The following services are no longer available to be requested on the ServiceNow platform. However making these changes can still be requested by creating a merge request on GitLab. Each link in this index provides further explanation and documentation on how the process of each of the items is to be accomplished.

## Creating a Merge Request:
Requested changes for each of these items are done in the form of merge requests for the gcp-config repository in GitLab located <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/tree/main" target="_blank">here</a>.

1. Clone the repository by using the “clone” button on the right-hand side to clone a copy locally.
2. Create a new branch following Kohl's naming structure listed <a href="https://confluence.doms.com:8443/display/KTJEN/GitHub+Pull+Request+Format" target="_blank">here</a>, changes cannot be made to Main directly but by merge requests.
3. When your changes are finished, publish and push the branch to gitlab.
4. Then on the side bar for gcp-config on the left side of the screen select “Merge requests”, afterwards click the blue “New merge request” button and choose your branch.
5. Once your merge request is made a pipeline is created that will run data validation against your changes and can be viewed by clicking its number. If this check fails evaluate the cause of error and resubmit your branch for a new pipeline evaluation.
6. When the pipeline validation is successful your change will be reviewed and upon approval the change will be made to production.

Please review the following links for more information.
    - [GitLab basics guides](https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html)
    & [How to create a merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)

## <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Deprecated%20ServiceNow%20Tasks/Add_Modify_GCP_Group_IAM_Roles.md" target="_blank">Add/Modify GCP Group IAM Roles:</a>
The above documentation defines where and how group IAM roles can be added and or modified for an existing GCP project. In addition it also covers policy standards to prevent data violations and possible points of confusion.

## <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Deprecated%20ServiceNow%20Tasks/Request_Access_to_GCP_Resource.md" target="_blank">Request Access to GCP Resource</a>
The above documentation defines how to request access to a GCP Resource for service level items like Bigquery Data Sets, Pub Sub Topics/Subscriptions and Storage Buckets Iam. This adds IAM binding at the service level, not the project. So for things like BigQuery, Pub/Sub and Storage Buckets specifically that have their own IAM bindings.

## <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Deprecated%20ServiceNow%20Tasks/Request_GCP_API_Enablement.md" target="_blank">Request GCP API Enablement:</a>
The above documentation defines where and how APIs can be enabled for use by an existing GCP project. In addition it also covers policy standards to prevent data violations and possible points of confusion.

## <a href="https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Deprecated%20ServiceNow%20Tasks/Request_New_or_Modify_Existing_GCP_Service_Account.md" target="_blank">Request New or Modify Existing GCP Service Account:</a>
The above documentation defines where and how Service Accounts can be added, modified, and/or removed. It covers where and how files should be handled.
