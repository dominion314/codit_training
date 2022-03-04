           __   ___  __        ___ ___  ___  __  
|__/ |  | |__) |__  |__) |\ | |__   |  |__  /__` 
|  \ \__/ |__) |___ |  \ | \| |___  |  |___ .__/ 
 __        __     __   __  
|__)  /\  /__` | /  ` /__` 
|__) /~~\ .__/ | \__, .__/ 
                                                                            

PART 1: Introduction
 
►  What is Kubernetes?

    Kubernetes is at its heart, a container orchestration tool. 

    It's responsible for allocating and scheduling containers, and then providing abstracted functionality like internal networking and file storage. It also includes monitoring the health of all of these elements and stepping in to repair or adjust them as necessary.

    In short, it's all about abstracting the how, when, and where containers are run, in our training specifically Docker containers.

►  What problems does Kubernetes solve?

    Providing an orchestration tool that maintains consistency, speed, and elastic horizontal scaling of resources.

    Lots of standardization, tooling, and vendor support from cloud providers for kubernetes.


K8S Need To Knows

►  Basic Components

    Container - Are often represented as container images in Docker to establish software or application requirements for a pod. 
    Pod - Smallest, most basic unit of kubernetes. It will encapsualte the running application and is ephemeral.
    Comprised of one or more containers and shares network/storage resources.
    Node - A pod "fleet" or pool of worker machines.
    Controllers – Define desired the state of the cluster. They're exposed as a workspace API object, which create and configure pods for you to maintain health. If the health or state of a pod changes, the controller responds. 
    Cluster - A Kubernetes cluster consists of the components that represent the control plane and multiple nodes. When you deploy Kubernetes, you get a cluster, which has atleast one worker node.

►  Services

    A resource (IP, DNS, Routing, LoadBalancing) you create to make a single, constant point of entry to a group of pods providing the same service. Each service has an IP address and port that never changes while the service exists. Clients can open connections to that IP and port, and those connections are then routed to one of the pods backing that service. This way, clients of a service don’t need to know the location of individual pods providing the service, allowing those pods to be moved around the cluster at any time.

►  ConfigMap

    Configmaps are for separating configuration from deployment. Without configmaps you'd have to download and redeploy your containers every time you wanted to change the configuration. This K8s primitive is intended for defining the configuration of the apps deployed to Kubernetes. Briefly, your config is a dictionary of settings represented by key-value pairs. They are stored in YAML, and a K8s resource called ConfigMap is responsible for handling them.

►  Volumes

    Kubernetes doesn't provide data persistence out of the box, which means when a pod is re-created, the data is gone. So, you need to create and configure the actual physical storage and manage it by yourself.

    The 1st component "Persistent Volume" is a cluster resource, like CPU or RAM, which is created and provisioned by administrators.

    The 2nd component "Persistent Volume Claim" on the other hand is a user's or pod's request for a persistent volume.

    With the 3rd component "Storage Class" you can dynamically provision Persistent Volume component and so automate the storage provisioning process.

►  ReplicaSet and Deployments

    ReplicaSets allow us to define number of replicas for a pod. Failed pods are replaced by replicas to maintain a healthy set.

    Deployments manage the rollout of ReplicaSets and control the transition of new pods running different versions.

  K8s Architecture 
►  Worker Nodes

    The worker node(s) host the Pods that are the components of the application workload. The control plane manages the worker nodes and the Pods in the cluster. This is the part of the cluster that actually executes the containers and applications on them.

►  Control Plane Node (Heart of the Cluster)

    Responsible for cluster management and for providing the API that is used to configure and manage resources within the Kubernetes cluster.  Implements functions for operations, monitoring, and is the access point for cluster administration. This is what CLI communicates with for operating the cluster.

►  Scheduler

    Responsible for managing the workloads throughout the cluster and assigning pods to nodes. Its main function is to assign newely created pods in the cluster to a feasible worker node as per the optimal resource requirements of the containers inside the pod. 

►  Controller Manager

    The Cloud Controller Manager can be described as three different things looking at it from a high level view:
        A binary
        A number of control loops
        Part of the glue between k8s and your cloud

►  etcd (Brain of the Cluster)

    Kuberenetes uses etcd to store all of its data – its configuration data, its state, and its metadata. Kubernetes is a distributed system, so it needs a distributed data store like etcd. Etcd lets any of the nodes in the Kubernetes cluster read and write data. It's a consistent and highly-available key value store used as Kubernetes' backing store for all cluster data.



PART 2: Hands On Engineering

►  What is minikube?

    Minikube is a tool that lets you run Kubernetes locally, with a single node on a cluster.

►  What is kubectl?

    The Kubernetes command-line tool, kubectl, allows you to run commands against Kubernetes clusters.

►  How do I install Minikube and Kubectl on GCP, AWS, Mac, or Linux?

    Create an instance for training in GCP/AWS or install directly to your laptop.
    Ensure you have the correct firewall rule in place for access
    Install docker on the VM or instance - https://tomroth.com.au/gcp-docker/
    Install minikube - https://minikube.sigs.k8s.io/docs/start/
        - Run the command "minikube start"
    Install kubectl - https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
        - Run the command "kubectl cluster-info" to verify

Commands and Output

►  Create a deployment (nginx server)

    kubectl create deployment nginx-test --image=nginx

        deployment.apps/nginx-test created

►  Get

    kubectl cluster-info

        Kubernetes control plane is running at https://192.168.49.2:8443
        CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

    kubectl get pods

        NAME                          READY   STATUS    RESTARTS   AGE
        nginx-test-84b478f9c5-b9zdv   1/1     Running   0          83s

    kubectl get nodes

        NAME       STATUS   ROLES                  AGE    VERSION
        minikube   Ready    control-plane,master   6h1m   v1.23.3

    kubectl get services

        NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
        kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   6h1m

    kubectl api-resources

        This should print out info for many things such as shortname, API version, kind, etc.

    kubectl get deployment nginx-test

        NAME         READY   UP-TO-DATE   AVAILABLE   AGE
        nginx-test   1/1     1            1           2m3s

    kubectl get replicaset

        NAME                    DESIRED   CURRENT   READY   AGE
        nginx-test-84b478f9c5   1         1         1       4m33

►  Describe/Logs

    kubectl describe deployment

        Name:                   nginx-test
        Namespace:              default
        CreationTimestamp:      Fri, 04 Mar 2022 03:19:41 +0000
        Labels:                 app=nginx-test
        Annotations:            deployment.kubernetes.io/revision: 1
        Selector:               app=nginx-test
        Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
        StrategyType:           RollingUpdate
        MinReadySeconds:        0
        RollingUpdateStrategy:  25% max unavailable, 25% max surge
        Pod Template:
        Labels:  app=nginx-test
        Containers:
        nginx:
            Image:        nginx
            Port:         <none>
            Host Port:    <none>
            Environment:  <none>
            Mounts:       <none>
        Volumes:        <none>
        Conditions:
        Type           Status  Reason
        ----           ------  ------
        Available      True    MinimumReplicasAvailable
        Progressing    True    NewReplicaSetAvailable
        OldReplicaSets:  <none>
        NewReplicaSet:   nginx-test-84b478f9c5 (1/1 replicas created)
        Events:
        Type    Reason             Age   From                   Message
        ----    ------             ----  ----                   -------
        Normal  ScalingReplicaSet  15m   deployment-controller  Scaled up replica set nginx-test-84b478f9c5 to 1

    kubectl logs nginx-test-84b478f9c5-b9zdv

        /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
        /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
        /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
        10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
        10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
        /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
        /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
        /docker-entrypoint.sh: Configuration complete; ready for start up
        2022/03/04 03:19:48 [notice] 1#1: using the "epoll" event method
        2022/03/04 03:19:48 [notice] 1#1: nginx/1.21.6
        2022/03/04 03:19:48 [notice] 1#1: built by gcc 10.2.1 20210110 (Debian 10.2.1-6) 
        2022/03/04 03:19:48 [notice] 1#1: OS: Linux 4.19.0-18-cloud-amd64
        2022/03/04 03:19:48 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
        2022/03/04 03:19:48 [notice] 1#1: start worker processes
        2022/03/04 03:19:48 [notice] 1#1: start worker process 31
        2022/03/04 03:19:48 [notice] 1#1: start worker process 32

►  Delete

    kubectl delete  pod nginx-test-84b478f9c5-b9zdv
        
        pod "nginx-test-84b478f9c5-b9zdv" deleted

    kubectl delete deployment nginx-test
        
        deployment.apps "nginx-test" deleted
  
        

PART 3: K8s YAML Configuration File

►  3 parts of a Kubernetes config file (metadata, specification, status)
►  format of configuration file
►  blueprint for pods (template)
►  connecting services to deployments and pods (label & selector & port)
►  demo

🔗 Links:
- Git repo link: https://bit.ly/2JBVyIk

 Demo Project 
►  Deploying MongoDB and Mongo Express
►  MongoDB Pod
►  Secret
►  MongoDB Internal Service
►  Deployment Service and Config Map
►  Mongo Express External Service

🔗 Links:
- Git repo link: https://bit.ly/3jY6lJp

  Organizing your components with K8s Namespaces 
►  What is a Namespace?
►  4 Default Namespaces
►  Create a Namespace
►  Why to use Namespaces? 4 Use Cases
►  Characteristics of Namespaces
►  Create Components in Namespaces
►  Change Active Namespace

🔗 Links:
- Install Kubectx: https://github.com/ahmetb/kubectx#ins...

  K8s Ingress explained 
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

  Helm - Package Manager 
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

  Persisting Data in K8s with Volumes 
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

  Deploying Stateful Apps with StatefulSet 
►  What is StatefulSet? Difference of stateless and stateful applications
►  Deployment of stateful and stateless apps
►  Deployment vs StatefulSet
►  Pod Identity
►  Scaling database applications: Master and Worker Pods
►  Pod state, Pod Identifier
►  2 Pod endpoints

  K8s Services 
►  What is a Service in K8s and when we need it?
►  ClusterIP Services
►  Service Communication
►  Multi-Port Services
►  Headless Services
►  NodePort Services
►  LoadBalancer Services