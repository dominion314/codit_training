Download sdk
https://cloud.google.com/sdk/docs/install#linux

set account 
gcloud config set account dominickhrndz314@gmail.com

login via browser to authenticate
gcloud auth login

Choose Project
gcloud container clusters get-credentials autopilot-cluster-1 --region us-east1 --project sandbox-io-289003