# Pipelines and Processes Supporting GitOps/NetX

1. VPN Secrets Deployment with Jenkin's

## 1. VPN Secrets Deployment with Jenkin's

#### Summary
All project namespaces within the production/QA clusters should have a secret deployed within.  This secret is used for GCP resources to build VPNs.  

#### Jenkin's Job
https://iaas1-jenkins.doms.com:8443/job/Network/job/Public-Cloud/job/GCP/job/V1.0/job/gcp-netops-vault-to-gke/job/master/

#### Repo
https://gitlab.com/doms/infra/platform_enablement/platform-connectivity/NetOps/-/tree/master/ansible/vault-to-gke

#### Vault Secret Location
https://vault-us-central1-primary.doms.com:8200/ui/vault/secrets/kv-cpe/show/netinfaut/vpn
