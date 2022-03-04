1. Install gatekeeper in k8s cluster
2. kubectl apply -f bucket-constraint-template.yml
3. kubectl apply -f bucket-contstraint.yml
4. kubectl apply -f bucket-sample.yml

This sample requires gcp-kohlsdev-cpa-inspec namespace to be created with project-id annotation set to kohlsdev-cpa-inspec
Bucket creation will fail because the bucket versioning parameter needs to be true
Change bucket-sample.yml versioning parameter to true and rerun.  Bucket will be created.
