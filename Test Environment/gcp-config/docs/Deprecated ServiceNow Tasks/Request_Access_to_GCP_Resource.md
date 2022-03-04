# Request Access to GCP Resource

You can request access to a GCP Resource for service level items like Bigquery Data Sets, Pub Sub Topics/Subscriptions and Storage Buckets Iam.
## File Location(s):
Access to service level items are defined within the big-query-dataset.yml, pub-sub-topics.yml, or storage-buckets-iam.yml files located in their respective project folder in project_vars.
For example:
gcp-config/project_vars/{your-project]}/big-query-dataset.yml
gcp-config/project_vars/{your-project]}/pub-sub-topics.yml
gcp-config/project_vars/{your-project]}/storage-buckets-iam.yml
Structure/Samples
Big-query-dataset.yml 

Structure Below:
```yaml
---
bigQueryDatasets:
  {{ big query dataset name 1 }}:
    friendlyName: "{{ friendly name }}"
    description: "{{ description }}"
    defaultTableExpirationMs: {{ default table expiration ms }}
    permissions:
      usersByEmail:
        {{ user by email 1 }}:
          roles:
            - {{ role 1 }}
      groupsByEmail:
        {{ group by email 1 }}:
          roles:
            - {{ role 2 }}
      serviceAccountsByEmail:
        {{ service account by email 1 }}:
          roles:
            - {{ role 3 }}
```
Big-query-dataset.yml Sample Below:
```yaml
---
bigQueryDatasets:
  analytics:
    friendlyName: analytics
    description: "Analytics dataset created for product users in EDA team"
    deletionProtect: true
    permissions:
      groupsByEmail:
        gcp-bda-gcp-labs-user@kohls.com:
          roles:
          - bigquery.dataEditor
        gcp-bda-gcp-labs-superuser@kohls.com:
          roles:
          - bigquery.dataEditor
          - bigquery.dataViewer
        gcp-bda-softwareengineer-l3@kohls.com:
          roles:
          - bigquery.dataViewer
```
Pub-sub-topics.yml Structure Below:
```yaml
---
pubSubTopics:
  {{ topic name 1 }}:
    labels:
      {{ label key 1 }}: "{{ label value 1 }}"
      {{ label key 2 }}: "{{ label value 2 }}"
    permissions:
      usersByEmail:
        {{ user by email 1 }}:
          roles:
            - {{ role 1 }}
        {{ users by email 2 }}:
          roles:
            - {{ role 2 }}
            - {{ role 3 }}
  {{ topic name 2 }}:
    permissions:
      groupsByEmail:
        {{ group by email 1 }}:
          roles:
            - {{ role 4 }}
      serviceAccountsByEmail:
        {{ service account by email 1 }}:
          roles:
            - {{ role 5 }}
```
Pub-sub-topics.yml Sample Below:
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
        mark.doll@kohls.com:
          roles:
            - pubsub.subscriber
        hamilton.hoover@kohls.com:
          roles:
            - pubsub.publisher
```

Storage-buckets-iam.yml Structure Below:
```yaml
---
storageBuckets:
  {{bucket name 1}}:
    permissions:
      usersByEmail:
        {{user by email 1}}:
          deletionProtect: {{boolean}}
          roles:
          - {{role 1}}
          - {{role 2}}
      groupsByEmail:
        {{group by email 1}}:
          deletionProtect: false
          roles:
          - {{role 3}}
          - {{role 4}}
      serviceAccountsByEmail:
        {{service account by email 1}}:
          deletionProtect: {{boolean}}
          roles:
          - {{role 5}}
          - {{role 6}}
  {{bucket name 2}}:
```
Storage-buckets-iam.yml Sample Below:
```yaml
---
# Good Storage Buckets Iam
storageBuckets:
  kohlsdev-test-bucket-01:
    permissions:
      usersByEmail:
        bryce.mcmurtry@kohls.com:
          deletionProtect: true
          roles:
          - storage.legacyBucketReader
      groupsByEmail:
        hamilton.hoover@kohls.com:
          deletionProtect: false
          roles:
          - storage.legacyBucketWriter
      serviceAccountsByEmail:
        mark.doll.gserviceaccount.com:
          deletionProtect: true
          roles:
          - storage.legacyBucketReader
          - storage.legacyBucketWriter
```
## Modifying Roles:
For each {{role}} in the above examples can be filled in with the roles granted that are described below that will allow access to accounts at service level.
## Big Query Dataset:
This catalog item is used to request reader/writer role for the members of the BQ Dataset(s) selected.

### Roles Granted:
Read - bigquery.dataViewer\
Write - bigquery.dataEditor

## Pub Sub Topics:
This catalog is used to request  IAM needs to only service accounts on pub/sub topic/s and subscription/s but not meant to create any new topics or subscriptions. Currently this workflow "does not" support cross project needs.

Select either a topic or a subscription or both but it's not mandatory to select both.

### Roles Granted:
Topic - pubsub.publisher\
Subscription - pubsub.subscriber

## Storage Buckets Iam:
This catalog item is used to request read or write access for the GCP project’s Service Accounts and/or a GCP Group to the GCS Bucket selected.

### Roles Granted:
Read - storage.legacyBucketReader\
Write - storage.legacyBucketWriter

