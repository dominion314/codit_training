PART 2: K8S Object Configuration



►  A Config File (YAML, labels, metadata, specification, status, ports, services, selectors)

    YAML files are used to define individual objects and then inject them into the k8s API. Each of these object types (YAML files) has a piece of code responsible for managing its lifecycle and orchestrates the system as a whole. Objects are independent, meaning you don't have to define your service(ie network) and your deployment(nginx pod) at the same time. 
    
    They're completely separate objects that know nothing about each other, their only connection is that a service will try to find pods based on label selectors you define. The most comman YAML schema models are pod, replica set, deployment, service, and config map. 

        This is the minimum requirements for all schemas:

            apiVersion:
            kind:
            metadata:
            spec:

        Schemas will differ by their spec:

            apiVersion: v1
            kind: Pod
            metadata:
                name: nginx
            spec: ##This object is a pod running an nginx server.
                containers:
                - name: nginx
                    image: nginx:1.14.2
                    ports:
                    - containerPort: 80

    Labels are a mechanism for one object to reference another object through a process of selection.

    Metadata is data that helps uniquely identify the object, including a name string, UID, and optional namespace.

    Specification is a complete description of the desired state, including configuration settings provided by the user, default values expanded by the system, and properties initialized or otherwise changed after creation by other ecosystem components (e.g., schedulers, auto-scalers), and is persisted in stable storage with the API object. If the specification is deleted, the object will be purged from the system.

    Status describes the current state of the object, supplied and updated by the Kubernetes system and its components. 

    Ports expose Kubernetes to a service within the cluster. 

    Services are a resource you create to make a single, constant point of entry to a group of pods providing the same service. Each service has an IP address and port that never change while the service exists. Clients can open connections to that IP and port, and those connections are then routed to one of the pods backing that service. 

    Selectors identify labels that the user configures to create objects. The label selector is the core grouping primitive in Kubernetes. It identifies the key-value pairs of the your YAML file to build the object.