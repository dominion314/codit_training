Part 1: Namespaces

►  What is a Namespace?

    Namespace provides an additional qualification to a resource name or one word it used for isolation. This is helpful when multiple teams are using the same cluster and there is a potential of name collision. It can be as a virtual wall between multiple clusters. There is no “right” way to do namespaces, there’s only something that works for you. Use namespaces to have strict separation between resources and for RBAC where needed. Use separate namespaces to keep apart services that should be prevented from sharing the same configmaps/secrets, or that should be isolated from other services (with network policies - this can be done within the same namespace but requires more work than with namespaces). Virtual cluster within a cluster.

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

►  Why to use Namespaces? 3 Use Cases

Roles and Responsibilities in an Enterprise - A typical enterprise contains multiple business/technology entities that operate independently of each other with some form of overarching layer of controls managed by the enterprise itself.

Using Namespaces to partition development landscapes -Software development teams customarily partition their development pipelines into discrete units. These units take various forms and use various labels but will tend to result in a discrete dev environment, a testing|QA environment, possibly a staging environment and finally a production environment. 

Partitioning of your Customers - If you are, for example, a consulting company that wishes to manage separate applications for each of your customers, the partitioning provided by Namespaces aligns well. You could create a separate Namespace for each customer, customer project or customer business unit to keep these distinct while not needing to worry about reusing the same names for resources across projects.



►  Characteristics of Namespaces - Isolated and doesnt allow you to use the most of the saem resources between namepsaces without a congimap. The confimap my refference the service or resource within a secific namespace.

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
      name: http
      port: 9200
      protocol: TCP
      name: transport
      port: 9300
      protocol: TCP

►  Commands

    kubectl create namespace doms-namespace
    kubectl config current-context
    kubectl config use-context doms-namespace 
    kubectl describe namespace doms-namespace

https://www.youtube.com/watch?v=K3jNo4z5Jx8 - 11:26 configmap for namespaces.
