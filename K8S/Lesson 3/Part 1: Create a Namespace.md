Part 1: Namespaces

    ►  What is a Namespace?

    Namespace provides an additional qualification to a resource name or one word it used for isolation. This is helpful when multiple teams are using the same cluster and there is a potential of name collision. It can be as a virtual wall between multiple clusters. There is no “right” way to do namespaces, there’s only something that works for you. Use namespaces to have strict separation between resources and for RBAC where needed. Use separate namespaces to keep apart services that should be prevented from sharing the same configmaps/secrets, or that should be isolated from other services (with network policies - this can be done within the same namespace but requires more work than with namespaces).

    ►  4 Default Namespaces

    Default - The default namespace for objects with no other namespace
    Kube-node-lease - This namespace holds Lease objects associated with each node. Node leases allow the kubelet to send heartbeats so that the control plane can detect node failure.
    kube-public - his namespace is created automatically and is readable by all users (including those not authenticated). This namespace is mostly reserved for cluster usage, in case that some resources should be visible and readable publicly throughout the whole cluster. The public aspect of this namespace is only a convention, not a requirement.
    kube-system - The namespace for objects created by the Kubernetes system

    ►  Create a Namespace

apiVersion: v1
kind: Namespce
metadata
    name: doms-namespace

    ►  Why to use Namespaces? 4 Use Cases
    ►  Characteristics of Namespaces
    ►  Create Components in Namespaces

apiVersion: v1
kind: Service
metadata:
   name: elasticsearch
   namespace: elk
   labels:
      component: elasticsearch
spec:
   type: LoadBalancer
   selector:
      component: elasticsearch
   ports:
   - name: http
      port: 9200
      protocol: TCP
   - name: transport
      port: 9300
      protocol: TCP

    ►  Change Active Namespace

    kubectl create namespace doms-namespace
    kubectl config current-context
    kubectl config use-context doms-namespace 
    kubectl describe namespace doms-namespace

    🔗 Links:
    - Install Kubectx: https://github.com/ahmetb/kubectx#ins...
