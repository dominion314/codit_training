▬▬▬▬▬▬ COURSE OVERVIEW 📚  ▬▬▬▬▬▬
🔥  What is Kubernetes 🔥 
►  What problems does Kubernetes solve?
►  What features do container orchestration tools offer?

🔥  Main K8s Components 🔥  
►  Node & Pod
►  Service & Ingress
►  ConfigMap & Secret
►  Volumes
►  Deployment & StatefulSet

🔥  K8s Architecture 🔥
►  Worker Nodes
►  Master Nodes
►  Api Server
►  Scheduler
►  Controller Manager
►  etcd - the cluster brain

🔥  Minikube and kubectl - Local Setup 🔥
►  What is minikube?
►  What is kubectl?
►   install minikube and kubectl
►  create and start a minikube cluster

🔗 Links:
- Install Minikube (Mac, Linux and Windows): https://bit.ly/38bLcJy 
- Install Kubectl: https://bit.ly/32bSI2Z
- Gitlab: If you are using Mac, you can follow along the commands. I listed them all here: https://bit.ly/3oZzuHY

🔥  Main Kubectl Commands - K8s CLI 🔥
►  Get status of different components
►  create a pod/deployment
►  layers of abstraction
►  change the pod/deployment
►  debugging pods
►  delete pod/deployment
►  CRUD by applying configuration file

🔗 Links: 
- Git repo link of all the commands: https://bit.ly/3oZzuHY

🔥  K8s YAML Configuration File 🔥
►  3 parts of a Kubernetes config file (metadata, specification, status)
►  format of configuration file
►  blueprint for pods (template)
►  connecting services to deployments and pods (label & selector & port)
►  demo

🔗 Links:
- Git repo link: https://bit.ly/2JBVyIk

<!-- 🔥 Demo Project 🔥 ## Something up with the secrets portion of this. Since we cant view the GUI in a gcp vm through minikube, we will exclude this exercise. 
►  Deploying MongoDB and Mongo Express
►  MongoDB Pod
►  Secret
►  MongoDB Internal Service
►  Deployment Service and Config Map
►  Mongo Express External Service

🔗 Links:
- Git repo link: https://bit.ly/3jY6lJp -->

🔥  Organizing your components with K8s Namespaces 🔥
►  What is a Namespace?
►  4 Default Namespaces
►  Create a Namespace
►  Why to use Namespaces? 4 Use Cases
►  Characteristics of Namespaces
►  Create Components in Namespaces
►  Change Active Namespace

🔗 Links:
- Install Kubectx: https://github.com/ahmetb/kubectx#ins...

🔥  K8s Ingress explained 🔥
►  What is Ingress? External Service vs. Ingress
►  Example YAML Config Files for External Service and Ingress
►  Internal Service Configuration for Ingress
►  How to configure Ingress in your cluster?
►  What is Ingress Controller?
►  Environment on which your cluster is running (Cloud provider or bare metal)
►  Demo: Configure Ingress in Minikube
►  Ingress Default Backend
►  Routing Use Cases
►  Configuring TLS Certificate

🔗 Links:
- Git Repo: https://bit.ly/3mJHVFc
- Ingress Controllers: https://bit.ly/32dfHe3
- Ingress Controller Bare Metal: https://bit.ly/3kYdmLB

🔥  Helm - Package Manager 🔥
►  Package Manager and Helm Charts
►  Templating Engine
►  Use Cases for Helm
►  Helm Chart Structure
►  Values injection into template files
►  Release Management / Tiller (Helm Version 2!)

🔗 Links:
- Helm hub: https://hub.helm.sh/
- Helm charts GitHub Project: https://github.com/helm/charts
- Install Helm: https://helm.sh/docs/intro/install/

🔥  Persisting Data in K8s with Volumes 🔥
►  The need for persistent storage & storage requirements
►  Persistent Volume (PV)
►  Local vs Remote Volume Types
►  Who creates the PV and when?
►  Persistent Volume Claim (PVC)
►  Levels of volume abstractions
►  ConfigMap and Secret as volume types
►  Storage Class (SC)

🔗 Links:
- Git Repo: https://bit.ly/2Gv3eLi

🔥  Deploying Stateful Apps with StatefulSet 🔥
►  What is StatefulSet? Difference of stateless and stateful applications
►  Deployment of stateful and stateless apps
►  Deployment vs StatefulSet
►  Pod Identity
►  Scaling database applications: Master and Worker Pods
►  Pod state, Pod Identifier
►  2 Pod endpoints

🔥  K8s Services 🔥
►   What is a Service in K8s and when we need it?
►  ClusterIP Services
►  Service Communication
►  Multi-Port Services
►  Headless Services
►  NodePort Services
►  LoadBalancer Services