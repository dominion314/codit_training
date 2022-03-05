# kcc export
This document explains how to setup gcloud and the config connector export tool so that current configurations in gcp can be exported using gcloud asset export and converted to kcc custom resources using config connector exporter tool.

Either of these files, the gcloud asset export json or the config connector export custom resource yaml are valuable data to help customers create the gitops config to manage existing gcp resources.

## Prerequisites
1. Install latest gcloud sdk.
2. Download kcc-export service account key from Vault - https://vault-us-central1-primary.doms.com:8200/ui/vault/secrets/kv-iaas/show/cloud-architect/kcc/prd.  Use KCC_EXPORT_JSON_KEY.
3. Setup gcloud to use kcc-export@doms-cpe-cpa-lle.iam.gserviceaccount.com service account key downloaded in Step 2 for authentication.
4. Install config-connector export application - https://cloud.google.com/config-connector/docs/how-to/import-export/overview#installing_config-connector.

## Export gcp configuration using gcloud asset export

### For resources:
1. Replace {{project-name}} in command below with the project name whose iam bindings need to be exported
2. Replace {{asset-type}} in command below with a comma delimited list of asset types that need to be exported.  As an example, use compute.googleapis.com/Firewall to export firewalls.
3. Replace {{suffix}} in command below to add context to the type of assets being exported.

Link to assest-types - https://cloud.google.com/asset-inventory/docs/supported-asset-types?hl=it

```gcloud asset export  --content-type resource  --project {{project-name}  --asset-types {{asset-type}}   --output-path "gs://kcc-export/{{project-name}}-{{suffix}}.json"```

### For iam policy:
1. Replace {{project-name}} in command below with the project name whose iam bindings need to be exported.  {{suffix}} is set to iam for this use case.

```gcloud asset export --content-type iam-policy --asset-types=cloudresourcemanager.googleapis.com/Project --project {{project-name}} --output-path "gs://kcc-export/{{project-name}}-iam.json"```

## Download cloud asset json file from bucket
The cloud asset json file can be used as input into config connector export tool to identify which gcp resources should be converted to kcc custom resources.
1. Replace {{project-name}} and {{suffix}} in command below with the project name whose assets were exported to the file format used above.

```gsutil gs://kcc-export/{{project-name}}-{{suffix}}.json"```

## Create config connector custom resources from cloud asset export file
The output of the config connector export tool are custom resource definitions for the gcp resources that have been input into the tool using the file dowloaded above.  The output can be one big yaml file with all custom resources defined in it or directory with individual custom resource yamls for each resource.

### For resources
1. Replace {{project-name}} and {{suffix}} in command below.  This should match the cloud asset json file name downloaded from bucket above.
2.  Command below will create separate custom resource yamls in the directory specified in --output.  If a file name is given instead of a directory in the --output paramater, one single file with all customer resources defined with in it will be output instead of multiple files in a directory.

```config-connector bulk-export --input {{project-name}}-{{suffix}}.json --output {{project-name}}-{{suffix}}/ --on-error continue```

### For IAM policy
1. Replace {{project-name}} in command below.  This should match the cloud asset json file name downloaded from bucket above.
2. The command below will create separate custom resource yamls for each iam binding with --iam-format set to policymember.  To create a single a binding customer resource file, set --iam-format to policy instead of policymember.

```config-connector bulk-export --input {{project-name}}-iam.json --output {{project-name}}-iam/ --on-error continue --iam-format policymember```
