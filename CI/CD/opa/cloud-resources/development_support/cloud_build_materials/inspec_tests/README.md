
# Recommendations on using Cloud Build for running inspec tests
## Custom image containing inspec binaries 
Custom image could be build using Cloud Build process and stored in Cloud Registry.
Content in **image_builds/inspec** shows example of such process

##  Managing inspec service account
Because running inspec requires providing proper GCP service account credentials, managing service account key requires proper considerations. Cloud Build allows easy integration with KMS service for this purpose.
The following is basic steps you can use KMS for the purpose of securing service account:
- Enable KMS API in GCP project with CB
- Create KMS key ring
- Create key in key ring
- Grant Clound Build service account access to key in key ring
- Place SA key in key in key ring


## Example of CB pipeline
### Portion of pipeline that decrypts SA key stored in cloud-build-kcc-cpa-dev ring
```
#Handle SA key
- name: 'gcr.io/cloud-builders/gcloud'  
  id: 'Decrypt inspec service account key'
  args:
  - kms
  - decrypt
  - --ciphertext-file=development_support/sample/inspec-sa-key.json.enc
  - --plaintext-file=inspec-sa-key.json
  - --location=global
  - --keyring=cloud-build-kcc-cpa-dev
  - --key=inspec-sa-key
```

### Portion of pipeline that runs inspec tests relying on the SA key (notice custom image inspecgcp-cloudbuild)
```
#Run inspec checks with json output
- name: 'gcr.io/$PROJECT_ID/inspecgcp-cloudbuild'  
  id: 'Run inspec validation (store results in JSON file)'
  entrypoint: 'inspec'
  args: ['exec', '.', '-t', 'gcp://', '--reporter', 'json:/workspace/artifacts/inspec_validation_result.json']
  #args: ['exec', '.', '-t', 'gcp://' ]
  dir: 'inspec_profile'
  env:
  - 'CHEF_LICENSE=accept-silent'
  - 'GOOGLE_APPLICATION_CREDENTIALS=/workspace/inspec-sa-key.json'
```

## References
- https://cloud.google.com/cloud-build/docs/securing-builds/use-encrypted-secrets-credentials

