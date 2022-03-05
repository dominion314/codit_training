# Google resource parameters for gitops
## Project resource
The project resource parameter file is required due to other resources depending on the project name definition.  Due to this requirement, if other resources are being managed, but you do not want the project itself to be managed, you can set the project field managed to False.  If managed is True, the project will created if it doesn't already exist or will become managed if it already exists.

The following project fields are **required**:
* **name:** *Must follow doms project naming standards*
* **managed:** *Valid values are True or False.  False is used when project resource should not be managed*
* **folderId:** *This [field](https://gitlab.com/doms/infra/platform_enablement/cloud-config/gcp-config/-/blob/main/docs/Projects/Project_Jump_Start_Guide.md#netx-project-folder-id-lookup-table) must be defined so project will be created in proper organization folder*
* **billingAccount:** *The billing account id is "00C36A-CD0BDB-E543D0" for Kohl's Google account*
* **labels**: *The list shown below are the labels that need to be defined for every project.  The values can also be defined using defaultLabels parameter resource as well*

The following project labels are **required** by Kohl's governence team:
* billing-dept-id:
* project-requestor:
* project-manager:
* devops-lead:
* line-of-business:
* environment-type:

**_Only hyphens (-), underscores (\_), lowercase characters, and numbers are allowed as characters in labels_**

The following project fields are **optional**:
* **deletionProtect:** *Valid values are true or false.  If field is not defined, default value is true.  When deletionProtect is set to true, deletion of project within git and kubernetes cluster will not delete project in Google.  This allows the projec to become unmanaged from kcc without deleting the project in Google.*

* **defaultNetwork:** *Valid values are true or false.  If field is not defined, default value is false.  When defaultNetwork is set to true, the project will be created with the Google default network.*

Service API enablement for a project is also included in the project resource file.  The following Google link shows how to find the most update to date list of Google API services.

https://cloud.google.com/service-usage/docs/list-services

List each service api that should be enabled as a key.  Optional settings for the service API enablement are deletionPolicy and disableDependentServices.

If deletionPolicy is set to abandon (its only valid value), removing the serviceAPI from the parameter file will NOT disable the service in GCP.  disableDependentServices is not a valid option if deletionPolicy is set to abandon.

If disableDependentServices is set to true, when the serviceAPI is removed from the parameter file, not only will that service be disabled in Google for the project, all dependent services of the service disabled will be disabled as well.  If disableDependentServices is set to false, and another serviceAPI is currently dependent upon the service, the service can not be deleted when removed from parameter file.

If no options are included with the serviceAPI key, then the service will be disabled when the serviceAPI key is removed from the parameter file.

Sample project.yml parameter file.
```yaml
---
billingDeptId: "90546"
project:
  name: doms-cpe-sample-lle
  managed: true
  folderId: "345254712059"
  billingAccount: "00C36A-CD0BDB-E543D0"
  labels:
    billing-dept-id: "90546"
    project-manager: josh-doll
    devops-lead: mark-doll
    environment-type: lle
    line-of-business: cpe
    project-requestor: zaki
serviceAPIs:
  compute.googleapis.com:
  storage-component.googleapis.com:
  storage-api.googleapis.com:
  stackdriver.googleapis.com:
  logging.googleapis.com:
  monitoring.googleapis.com:
  cloudasset.googleapis.com:
```

## Default Label resource
For Google resources that support labels, labels can be assigned within that resources parameter file.  When that is done, the label only applies to that resource.  If a label is defined within defaultLabels parameter file, that label will be applied to all resources.  This allows for labels to be defined once under the defaultLabels key without the need to set that label within each resource parameter file.

**_Default labels will be applied to every resource configuration_**

**_Resource labels will always take precedence over default labels_**

**_Only hyphens (-), underscores (\_), lowercase characters, and numbers are allowed as characters in labels_**

Sample default-labels.yml file.
```yaml
---
defaultLabels:
  billing-dept-id: "90000"
  line-of-business: marketing
  app-name: returns
```
## Service Account resource
Mulitple service accounts can be defined within the same parameter file.  The display name field is required for each service account.  Labels are optional and can be defined for each service account as needed. A description is also optional and can be defined for each service account.

* **deletionProtect:** *Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of service account within git and kubernetes cluster will not delete the service account in Google.  This allows the service account to become unmanaged from kcc without deleting the service account in Google.*
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
## IAM Policy Members resource
IAM bindings are made for each member and role combination.  Three types of members can be defined:
* users
* groups
* serviceAccounts

There can be multiple members defined within each member type and multiple roles assigned per member.
Primitiv Roles
* owner
* editor
* viewer

https://cloud.google.com/iam/docs/granting-changing-revoking-access#access_control_via_the_gcloud_tool
Unfortunately, the primitive role owner can not be assigned.

Note: To grant the Owner role for a project, you must use the Google Cloud Console, not the gcloud tool.```

Sample iam-policy-members.yml file

```yaml
---
iamPolicyMembers:
  usersByEmail:
    mark.doll@doms.com:
      roles:
        - editor
        - viewer
    hamilton.hoover@doms.com:
      roles:
        - owner
  groupsByEmail:
    gcp-et-devops-l3@doms.com:
      roles:
        - viewer
  serviceAccountsByEmail:
    gitops-example-2@domsdev-cpa-inspec.iam.gserviceaccount.com:
      roles:
        - viewer
```
For more information on roles and their permissions, please reference [Google Unserstanding Roles Documentation](https://cloud.google.com/iam/docs/understanding-roles)

**_Proper role names are listed in the above documentation link.  All roles defined in configuration do NOT need to be prefaced with 'roles/' as shown in the Google documentation_**

Other optional fields:
**deletionProtect:** Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of IAM bindings within git and kubernetes cluster will not delete IAM bindings in Google.  This allows the IAM bindings to become unmanaged from kcc without deleting the IAM bindings in Google.

## Storage Bucket resource
Many storage buckets can be defined within the same parameter file.  Versioning maybe enabled or disabled as defined by the field named: versioningEnabled.  Other features will be added in the future.  As with other resources, labels are optional.

For more information about storage buckets, please reference [Google Storage Bucket Documentation](https://cloud.google.com/storage/docs/json_api/v1/buckets)

Sample storage-buckets.yml file.
```yaml
---
storageBuckets:
  domsdev-cpa-inspec-test-bucket-01:
    location: US-EAST1
    versioningEnabled: false
    forceDestroy: true
    labels:
      test_label11: test_value11
      test_label12: test_value12
  storageClass: ARCHIVE
  lifecycleRule:
    - action:
        type: Delete
      condition:
        age: 7
        createdBefore: 2021-01-20
    - action:
        storageClass: COLDLINE
        type: SetStorageClass
      condition:
        age: 9
        createdBefore: 2137-01-20
    - action:
        type: SetStorageClass
        storageClass: STANDARD
      condition:
        age: 9
        matchesStorageClass:
          - COLDLINE
          - ARCHIVE
  domsdev-cpa-inspec-test-bucket-02:
    versioningEnabled: false
    deletionProtect: true
    bucketPolicyOnly: true
    labels:
      test_label11: test_value11
      test_label12: test_value12
    retentionPolicy:
      isLocked: true           # optional
      retentionPeriod: 86400   # required - min 1, do not use commas
```
location acceptable values are:
- US
- US-CENTRAL1
- US-EAST1
- US-EAST4
- US-WEST1
- US-WEST2
- US-WEST3
- US-WEST4
- NAM4

lifecycleRule action types acceptable values are:
- "Delete"
- "SetStorageClass"

lifecycleRule conditions:
- **age**:	integer	Age of an object (in days). This condition is satisfied when an object reaches the specified age.
- **createdBefore**:	date	A date in RFC 3339 format with only the date part (for instance, "2013-01-15"). This condition is satisfied when an object is created before midnight of the specified date in UTC.
- **withState**:	Match to live and/or archived objects. Unversioned buckets have only live objects. Supported values include: "LIVE", "ARCHIVED" or "ANY".
- **matchesStorageClass**:	list	Objects having any of the storage classes specified by this condition will be matched. Values include STANDARD, NEARLINE, COLDLINE, ARCHIVE, MULTI_REGIONAL, REGIONAL, and DURABLE_REDUCED_AVAILABILITY.
- **numNewerVersions**:	integer	Relevant only for versioned objects. If the value is N, this condition is satisfied when there are at least N versions (including the live version) newer than this version of the object.

storageClass allowed values:
- STANDARD
- NEARLINE
- COLDLINE
- ARCHIVE
- MULTI_REGIONAL
- REGIONAL
- DURABLE_REDUCED_AVAILABILITY.

**deletionProtect:** Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of storage buckets within git and kubernetes cluster will not delete storage buckets in Google.  This allows the storage buckets to become unmanaged from kcc without deleting the storage buckets in Google.

**forceDestroy:** Valid values are true or false. Applying the force-destroy annotation to the bucket and then deleting the bucket causes Config Connector to delete all of the objects within the bucket first, then deletes the bucket. Otherwise, Cloud Storage doesn't allow the deletion of a StorageBucket that contains objects. Cannot be used with deletionProtect.

**retentionPolicy:** Objects in a bucket with a retention policy can only be deleted or overwritten once their age is greater than the retention period. A retention policy retroactively applies to existing objects as well as new objects added to the bucket. Versioning must be disabled in order to set a retention policy.

 - **isLocked:** Optional, read carefully and use with caution. A retention policy can be locked to set it permanently on the bucket. Once a retention policy is locked, it cannot be removed or reduced (the retention period may be increased). The bucket cannot be deleted unless all objects within meet the retention period. **Use caution, locking a retention policy is irreversible.** Once locked, the entire bucket must be deleted to “remove” the policy.

 - **retentionPeriod:** Is in seconds. The following conversions apply:
    - A day is considered to be 86,400 seconds.
    - A month is considered to be 31 days, which is 2,678,400 seconds.
    - A year is considered to be 365.25 days, which is 31,557,600 seconds.
    - The maximum retention period is 3,155,760,000 seconds (100 years).

For more information about bucket lock and retention policies, please reference [Bucket Lock Documentation](https://cloud.google.com/storage/docs/bucket-lock)


**bucketPolicyOnly:** Also known as uniform bucket-level access. When uniform bucket-level access is enabled on a bucket, Access Control Lists (ACLs) are disabled, and only bucket-level Cloud Identity and Access Management (Cloud IAM) permissions grant access to that bucket and the objects it contains. All access granted by object ACLs and the ability to administrate permissions using bucket ACLs are revoked.

For more information about uniform bucket-level access, please reference [Google Uniform Bucket-Level Access](https://cloud.google.com/storage/docs/uniform-bucket-level-access)

### Storage Bucket Cloud IAM resource
For a complete understanding of storage ACLs vs storage cloud IAM, please reference [Google Bucket Access Documentation](https://cloud.google.com/storage/docs/uniform-bucket-level-access)

Storage buckets can have access control lists applied that can give five different member types one of two permissions allowed.  Members are broken up into one of the following types:
* users (email)
* groups (email)
* service accounts (email)
* primitive roles
  * viewers
  * editors
  * owners
* builtin Google groups
  * allUsers
  * allAuthenticatedUsers

Right now, only users, groups and service accounts are supported for Storage Bucket Cloud IAM.  Primitive roles and builtin Google groups may be added at a later time depending upon need.

The storage cloud IAM roles that can be assigned to these members are:
* storage.objectCreator
* storage.objectViewer
* storage.objectAdmin
* storage.admin
* storage.legacyObjectReader
* storage.legacyObjectOwner
* storage.legacyBucketReader
* storage.legacyBucketWriter
* storage.legacyBucketOwner

Assigning legacy roles using Storage Bucket Cloud IAM (permissions) is the same as assigning ACLs as shown below in the next section.

Other optional fields:
- **deletionProtect:**: Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of roles for a give member within git and kubernetes cluster will not delete the roles for the member in Google.  This allows the member-->roles binding to become unmanaged from kcc without deleting the member-->roles in Google.

For more information on Storage Bucket Cloud IAM, please reference [Google Bucket Access Controls Documentation](https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls)

Sample storage-buckets-iam.yml file
```yaml
---
storageBuckets:
  domsdev-cpa-test01-lle-bucket-04:
    permissions:
      usersByEmail:
        mark.doll@doms.com:
          deletionProtect: true
          roles:
          - storage.admin
        hamilton.hoover@doms.com:
          roles:
          - storage.legacyBucketOwner
          - storage.objectViewer
      groupsByEmail:
        gcp-iaas-govops-l3@doms.com:
          roles:
          - storage.objectViewer
      serviceAccountsByEmail:
        marks-sa@domsdev-cpa-test01-lle.iam.gserviceaccount.com:
          deletionProtect: false
          roles:
          - storage.legacyBucketOwner
```


### Storage Bucket ACL resource
For a complete understanding of storage ACLs vs storage cloud IAM, please reference [Google Bucket Access Documentation](https://cloud.google.com/storage/docs/uniform-bucket-level-access)

Storage buckets can have access control lists applied that can give five different member types one of two permissions allowed.  Members are broken up into one of the following types:
* users (email)
* groups (email)
* primitive roles
  * viewers
  * editors
  * owners
* builtin Google groups
  * allUsers
  * allAuthenticatedUsers

The permissions that can be assigned to these members are:
* OWNER
* WRITER
* READER

For more information on Storage Bucket Access Controls, please reference [Google Bucket Access Controls Documentation](https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls)

Sample storage-buckets-acl.yml file
```yaml
---
storageBuckets:
  domsdev-cpa-inspec-test-bucket-01:
    acls:
      usersByEmail:
        mark.doll@doms.com: OWNER
        hamilton.hoover@doms.com: READER
      groupsByEmail:
        gcp-iaas-cpa-devops-l3@doms.com: OWNER
      primitiveRoles:
        viewers: READER
        editors: OWNER
        owners: OWNER
      builtinGroups:
        allUsers: READER
        allAuthenticatedUsers: READER
  domsdev-cpa-inspec-test-bucket-02:
    acls:
      usersByEmail:
        pavel.leonovitch@doms.com: WRITER
```
### Storage Default Object ACL resource
For a complete understanding of storage ACLs vs storage cloud IAM, please reference [Google Bucket Access Documentation](https://cloud.google.com/storage/docs/uniform-bucket-level-access)

Storage buckets can have default object access control lists applied that can give five different member types one of two permissions allowed.  Members are broken up into one of the following types:
* users (email)
* groups (email)
* primitive roles
  * viewers
  * editors
  * owners
* builtin Google groups
  * allUsers
  * allAuthenticatedUsers

The permissions that can be assigned to these member are:
* OWNER
* READER

For more information on Storage Default Object ACLs, please reference [Google Storage Default Object ACL](https://cloud.google.com/storage/docs/json_api/v1/defaultObjectAccessControls)

Any number of users, groups, primitive roles and builtin Google groups can be defined.  None are mandatory.

Multiple storage buckets can have their default object ACLs defined within a file.

Sample storage-default-object-acls.yml file
```yaml
---
storageBuckets:
  domsdev-cpa-inspec-test-bucket-01:
    default_object_acls:
      usersByEmail:
        mark.doll@doms.com: OWNER
        hamilton.hoover@doms.com: READER
      groupsByEmail:
        gcp-iaas-cpa-devops-l3@doms.com: OWNER
      primitiveRoles:
        viewers: READER
        editors: OWNER
        owners: OWNER
      builtinGroups:
        allUsers: READER
        allAuthenticatedUsers: READER
  domsdev-cpa-inspec-test-bucket-02:
    default_object_acls:
      primitiveRoles:
        viewers: READER
```
## PubSub Topic resource
Multiple topics can be created in the same parameter file.  Permissions to the topic can be assigned by defining users, groups or service accounts with the role permission desired.  Pub/Sub specific roles are:
* pubsub.admin
* pubsub.editor
* pubsub.publisher
* pubsub.subscriber
* pubsub.viewer

Other optional fields:
- **deletionProtect:** Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of topics within git and kubernetes cluster will not delete topics in Google.  This allows the topics to become unmanaged from kcc without deleting the topics in Google.

In the sample below, the name of the topics to be created and/or managed would be *gitops.test.topic.one* and *gitops.test.topic.two*

Sample pub-sub-topics.yml file
```yaml
---
pubSubTopics:
  gitops.test.topic.one:                # required - name needs to be unique to project
    deletionProtect: true
    labels:                             # optional - labels are optional
      line-of-business: infra
      app-name:
    permissions:                        # optional - permissions applied at topic level are optional
      usersByEmail:                     # optional -
        mark.doll@doms.com:
          roles:
            - pubsub.admin
        hamilton.hoover@doms.com:
          roles:
            - pubsub.publisher
            - viewer
  gitops.test.topic.two:
    permissions:                        # optional -
      groupsByEmail:                    # optional -
        gcp-et-devops-l3@doms.com:
          roles:
            - pubsub.viewer
      serviceAccountsByEmail:           # optional
        gitops-example-1@domsdev-cpa-inspec.iam.gserviceaccount.com:
          roles:
            - pubsub.editor
```
For more information on Pub Sub roles, please reference [Google Pub/Sub Roles Documentation](https://cloud.google.com/iam/docs/understanding-roles#pubsub-roles)
## PubSub Subscription resource
Mulitple pubSubSubscriptions can be defined in the same parameter file.

Other optional fields:
- **deletionProtect:** Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of subscriptions within git and kubernetes cluster will not delete subscriptions in Google.  This allows the subscriptions to become unmanaged from kcc without deleting the subscriptions in Google.

Sample pub-sub-subscriptions.yml file
```yaml
---
pubSubSubscriptions:
  subscription.one:                     # required - name of subscription needs to be unique within project (no duplicates)
    labels:                             # optional - labels are optional
      labelone: value1                  # optional - only required if above labels: is defined
    topicName: gitops.test.topic.one    # required
    ackDeadlineSeconds: 15              # optional - default is 10
    messageRetentionDuration: 86400s    # optional - default is 86400s
    retainAckedMessages: false          # optional - default is false
    expirationPolicy:                   # optional - ttl default is 2678400s
      ttl: 300000.5s                    # optional - only required if above expirationPolicy: is defined

#   Push Configuration requires extra configuration - https://cloud.google.com/pubsub/docs/push#domain_ownership_validation
#   pushConfig:                         # optional - if block not defined then pull is delivery method
#     pushEndpoint: "https://example.com/push"  # optional - required if above pushConfig: is defined
#     attributes:                               # optional - required if above pushConfig: is defined
#       xGoogVersion: "v1"                      # optional - required if above pushConfig: is defined

  subscription.two:
    labels:
      labeltwo: value2
      abclable: value1
      zlabel: value2
    topicName: gitops.test.topic.one
    deletionProtect: true

  subscription.three:
    topicName: gitops.test.topic.two
    ackDeadlineSeconds: 15
    messageRetentionDuration: 600s
    retainAckedMessages: true
```
## Big Query Dataset resource

The following IAM roles are supported:
* owner
* editor
* viewer
* bigquery.admin
* bigquery.dataEditor
* bigquery.dataOwner
* bigquery.dataViewer
* bigquery.metadataViewer
* bigquery.user
* iam.securityReviewer

The following project fields are **optional**:
* **deletionProtect:** *Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of big query dataset within git and kubernetes cluster will not delete big query dataset in Google.  This allows the big query dataset to become unmanaged from kcc without deleting the big query dataset in Goolge.*

Sample big-query-dataset.yml file
```yaml
---
bigQueryDataset:
  name: gitopsbigquerydatasetexample                      # required - name needs to be unique
  friendlyName: gitops-bigquery-dataset-example           # optional - but highly recommended
  description: "GitOps Big Query Dataset Example"         # optional - but highly recommended
  defaultTableExpirationMs: 3600000                       # optional - minimum value 3600000
  defaultPartitionExpirationMs: 3600000                   # optional - if set Table Expiration is ignored
  deletionProtect: true                                   # optional - if set to true dataset will be unmanaged from kcc
  labels:                                                 # optional - labels are optional
    app-name: loyalty
  permissions:                                            # optional
    usersByEmail:                                         # optional - multiple roles per group can be defined
      hamilton.hoover@doms.com:
        roles:
          - bigquery.user
          - editor
    groupsByEmail:                                        # optional - multiple roles per group can be defined
      gcp-et-devops-l3@doms.com:
        roles:
          - bigquery.dataViewer
    serviceAccountsByEmail:                               # optiona; - multiple roles per service account can be defined
      gitops-example-1@domsdev-cpa-inspec.iam.gserviceaccount.com:
        roles:
          - biqquery.metadataViewer
```

To understand Biq Query Roles, please reference [Google Big Query Roles Documentation](https://cloud.google.com/iam/docs/understanding-roles#bigquery-roles)

## IAM Policy Subnets
IAM bindings are made for each member. Three types of members can be defined:
* users
* groups
* serviceAccounts

The following project fields are **optional**:
* **deletionProtect:** Valid values are true or false.  If field is not defined, default value is false.  When deletionProtect is set to true, deletion of IAM bindings within git and kubernetes cluster will not delete IAM bindings in Google.  This allows the IAM bindings to become unmanaged from kcc without deleting the IAM bindings in Google.

Sample IAMPolicySubnets.yml file.
```yaml
---
vpcs:
  {{VPC1}}:
    subnets:
      {{SUBNET1}}:
        deletionProtect: true
        permissions:
          usersByEmail:
          - usr1@doms.com
          - usr2@doms.com
          groupsByEmail:
          - gcp-devops@doms.com
          serviceAccountsByEmail:
          - gitops-example@domsdev-cpa-inspec.iam.gserviceaccount.com
```

For more information about IAM roles, please reference [Google IAM Policy Documentation](https://cloud.google.com/iam/docs/understanding-roles#compute-engine-roles)
