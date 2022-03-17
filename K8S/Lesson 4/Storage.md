Volumes


Why do we need Volumes?

Storage volumes or persistent storage are needed because there’s no data persistence within Kubernetes. If you delete a pod, the data is lost. You must setup storage that doesn't depend on the pod life-cycle. This way, new pods can pick up where the old one left off and storage will be available to the node for access. Volumes are managed at the node level. 

► Persistent Volume (PV)

The PV is the "U-Stor-It" storage locker - where the data actually resides. This is the actual storage that defines the size, usage, readwrite permissions, and reclaimPolicy.










► Persistent Volume Claim(PVC)

A PVC is the form you fill out at the U-Haul store that requests to rent a storage unit. Its defines the resources needed for a pod to stake claim to storage, memory and CPU of a persistent volume. Understand that this is a claim, not a guarantee. 

Reclaim Mode – Defines what to do after a use is done with their volume
	
	Retain – policy allows for manual reclamation of the resource. 	The storage is considered ‘released’, but not available for 	another claim.

	Deleted – removes the PV from Kubernetes and the external 	storage asset -AWS EBS, GCE, Azure Disk,etc


Access Mode - Volume claims also define access modes which define permissions for your volume:

ReadWriteOnce – Only a single pod can read and write data. 
ReadOnlyMany – Many nodes can read data.
ReadWriteMany – Many nodes can read and write data.














► Storage Classes

A PVC is either administered or dynamically provisioned using storage classes. Storage classes are storage options that are available to a business. For more traditional businesses, they may want to connect to their storage area network (SAN) using iSCSI as their connection to the cloud. Or they may use a network file system (NFS) for distributed storage to employees within a company. 

Most modern cloud deployments look something like this when connecting to their cloud provider:  













https://kubernetes.io/docs/concepts/storage/storage-classes/




► Local Volumes

Local volumes are a quick solution for data persistence that simply creates a volumes on a node within your cluster. Its a convenient method, however they are not tied to one specific node and they do not survive cluster crashes. Configmaps and secrets are considered local volumes within Kubernetes. 











Summary

► Who creates the Persistent Volumes?

As Kubernetes admins, your job is to setup and maintain  clusters and also to ensure users have the resources they need. If customers or users, deploy applications into a cluster you’ve created for them, typically it’s your job to manage storage requirements. Therefore, storage is managed by administrators.

► Order of Operations to Select a Volume

1. First the pod requests a volume with the the volume claim.
2. The claim then tries to find a volume in the cluster, that meets   the claims requests.
3. Once a volume is found it then accesses the actual storage back end (Cloud, NFS, etc).








Hands On – Configure a Pod to use a Persistent Volume

I. Setup your node

We first need to create a directory on our node that will point us to our volume. In order to this we need to ssh into our node, which in this case is minikube.



Create the directory and an index.html within it as an anchor. After this successful, exit your shell.

https://explainshell.com/







II. Create a Persistent Volume (local)

 


	This configuration file specifies that   	the volume is at mnt/data and that its 	looking for 20MB with and access mode 	of ReadWriteOnce. 

 	The storageClasssName is set to manual 	which means the PV and PVC will be 	bound together. 



Begin by creating the file above and then apply the deployment to the cluster. 

















View your new PV.



III. Create a Persistent Volume Claim

Pods use the PVC to request physical storage.



	

	This claim is grants ReadWriteOnce 	access and requests 3MBs of storage 	space.

Create the claim, verify its configuration, and then apply it to the cluster. Once finished verify that it exists.




IV. Create a Pod and Attach the Claim

This is the last step and often most difficult. Not only are we creating an Nginx pod, but we’re also attaching the PV, PVC, and the file path. 




	

	This pod create an Nginx 	server with port 80 open. It 	also shows the storage volume 	we will need, along with the 	volume claim we will be 	requesting.









Create the pod, verify its configuration, apply it to the cluster, and then make sure its working.



To verify that our storage is setup correctly, we need to SSH into the new Pod with the following command: 

kubectl exec -it doms-pv-pod -- /bin/bash



Once we’re in, we need to do a quick update using the command apt update.

We then need to install a tool call ‘curl’ using the apt install curl command. Curl is a basic bash tool that allows us to test the transfer of data between two ends. In this case we are using curl http://localhost to test our connection from the pod we’ve created to the Persistent Volume. 

If you receive the message:

‘Hello from Kubernetes storage’

You have successfully completed this lesson!







https://www.youtube.com/watch?v=ZxC6FwEc9WQ 530-11 min

