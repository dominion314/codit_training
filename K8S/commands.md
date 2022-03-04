
Get:

kubectl get ns
kubectl get all -n equinix-operator
kubectl get equinixInterconnect -n gcp-kohls-cpe-xpn-lle
kubectl get equinixInterconnect seed-nx-lle-c1-pi-rtr01-to-ch2-rtr1-eqx -n gcp-kohls-seed-xpn-lle
kubectl logs equinix-operator-controller-manager-75f785d556-2f95p manager -n equinix-operator -f
kubectl get EquinixInterconnect --all-namespaces -o=jsonpath='{range .items[*]}{@.metadata.namespace}{" "}{@.metadata.name}{" "}{@.kind}{" "}{@.status.interconnectDetail.portName}{" "}{@.status.interconnectDetail.status}{"\n"}{end}' | column -t
kubectl get EquinixInterconnect,ciscointerconnects -o=jsonpath='{range .items[*]}{.kind}~{.metadata.namespace}~{.metadata.name}~{.status.conditions[].reason}~{.status.conditions[].message}{"\n"}' --all-namespaces

Config:

kubectl config current-context
kubectl config get-contexts
kubectl config use-context gke_kohls-cpe-cne-lle_us-central1-c_kohls-cpe-cne-lle-01



Describe:

kubectl describe deployment -n equinix-operator
kubectl describe deployment –n 
kubectl describe gitopsconfig -n gcp-kohls-seed-xpn-lle

Pod info:

kubectl delete pod equinix-operator-controller-manager-75f785d556-dckmb -n equinix-operator
pod "equinix-operator-controller-manager-75f785d556-dckmb" deleted
kubectl get pods -A
kubectl get pods -n equinix-operator -o yaml
kubectl get pods -n equinix-operator -o yaml | grep operator

Useful Commands

$ kubectl config use-context gke_kohls-cpe-cne-lle_us-central1-c_kohls-cpe-cne-lle-01
$ kubectl get ns
$ kubectl cluster-info
$ kubectl get nodes
$ kubectl get nodes -o wide
$ kubectl get pods
$ kubectl get pods -n kube-system
$ kubectl get pods -n kube-system -o wide
$ kubectl get all --all-namespaces | more
$ kubectl api-resources | more
$ kubectl api-resources | grep pods
$ kubectl explain pod
$ kubectl explain pods.spec.containers
$ kubectl describe nodes gke-kohls-cpe-cne-ll-kohls-cpe-cne-ll-5f5475e8-adw7
$ kubectl -h

App Deployment Commands

$ k create deployment hello-world --image=gcr.io/google-samples/hello-app:1.0
$ k run hello-world-pod --image=gcr.io/google-samples/hello-app:1.0
$ k get pods
$ k get pods -o wide
$ k logs hello-world-pod
$ k exec -it hello-world-pod -- /bin/sh
$ k get deployment hello-world
$ kubectl get replicaset
$ k get pods
$ kribe deployment hello-world
$ kribe pod hello-world


Add a cluster :

gcloud container clusters get-credentials kohls-cpe-kcc-lle-01 --zone us-central1-a --project kohls-cpe-kcc-lle

Switch to cluster:

Devme or kubectl config use-context gke_kohls-cpe-kcc-lle_us-central1-a_kohls-cpe-kcc-lle-01

gke_kohls-cpe-cne-lle_us-central1-c_kohls-cpe-cne-lle-01
dev
gke_kohls-cpe-kcc-lle_us-central1-a_kohls-cpe-kcc-lle-01
qa


Add files to cluster:

kubectl apply -f eqxConnectivity.yml 
equinixinterconnect.cne.cpe.kohls.com/cpe1-xpn-lle-c1-pi-rtr01-to-ch2-rtr1-eqx created
ciscointerconnect.cne.cpe.kohls.com/cpe1-xpn-lle-c1-pi-rtr01-to-ch2-rtr1-cisco created

kubectl apply -f vpcPIRouter.yml 
computerouter.compute.cnrm.cloud.google.com/cpe1-xpn-lle-c1-pi-rtr01 created
computeinterconnectattachment.compute.cnrm.cloud.google.com/cpe1-xpn-lle-c1-pi-rtr01-to-ch2-rtr1 created

How many CR's in cluster:

kubectl api-resources --verbs=list --namespaced -o name \
  | xargs -n 1 kubectl get --show-kind --ignore-not-found -n <namespace>
kubectl get gcp -A | wc –l


How to look up GCP Objects:

kubectl get gcp -n gcp-kohls-cpa-xpn-lle  -o=custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,KIND:.kind,STATUS:.status.conditions[0].status,REASON:.status.conditions[0].reasongcp
kubectl get gcp –n gcp-kohls-cpe-xpn-lle -o=custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,KIND:.kind,STATUS:.status.conditions[0].status,REASON:.status.conditions[0].reason
