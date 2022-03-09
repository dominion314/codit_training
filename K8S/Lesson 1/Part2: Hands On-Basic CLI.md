           __   ___  __        ___ ___  ___  __  
|__/ |  | |__) |__  |__) |\ | |__   |  |__  /__` 
|  \ \__/ |__) |___ |  \ | \| |___  |  |___ .__/ 
 __        __     __   __  
|__)  /\  /__` | /  ` /__` 
|__) /~~\ .__/ | \__, .__/ 
                           

PART 2: Hands On Engineering - Basic Command Line



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