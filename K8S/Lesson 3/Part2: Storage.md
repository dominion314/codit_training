Lesson 3

Persisting Data in K8s with Volumes

►  The need for persistent storage & storage requirements
   
   There is no data persistence within Kubernetes, so if you delete a pod the data is lost. You must setup storagge that doesnt depend on the pod lifecycle. This way new pods can pick up where the old one left off. Therefore, storage must be available to all nodes in order for the pods to have access.   

►  Persistent Volume (PV)

  The PV is the "U-Stor-It" storage locker - where the stuff actually resides. The PVC is the contract that gives you the right to use it, for now.
  A persistent volume is a piece of storage in a cluster that an administrator has provisioned. It is a resource in the cluster, just as a node is a cluster resource. A persistent volume is a volume plug-in that has a lifecycle independent of any individual pod that uses the persistent volume.

►  Local vs Remote Volume Types

Local volume types are not tied to one specifci node and do not survive cluster crashes. However, local volumes are a quick solution for data persistence when the administrator only needs to save data to the local drive.

Remote is almost always preferable for data persistence as it will remain regardless of cluster health.  


►  Who creates the PV and when?

K8S admins setup and maintain the clusters and also makes sure it has enough resrouces. Users deploy applications to the cluster. Therfore, storage is managed by the admin and can include bare metal storage or cloud storage.


►  Persistent Volume Claim (PVC)

The YAML files in kubernetes deployments have to specifically specify what storage the cluster is attaached to. The applications has to claim the PVC. That claim may look something like this:

apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"


►  Order of Operations to Select a Volume

First the pod requests the volume the the PV claim
The claim then tries to find a volume in the cluster
Once found the volume then access the actuall storage backend

Note that claims must exist within the same namespace!

After the pod finds the volume, it is mounted to the container and then it is mounted to the pod.

apiVersion: v1
kind: Pod
metadata:
  name: test-ebs
spec:
  containers:
   image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-ebs
      name: test-volume
  volumes:
   name: test-volume
    # This AWS EBS volume must already exist.
    awsElasticBlockStore:
      volumeID: "<volume id>"
      fsType: ext4

Now the pod/s will have access to the same storage.

►  ConfigMap and Secret as volume types

Configmaps and secrets are considered local volumes within kubernetes.

►  Storage Class (SC)

Creates or provisiones PV dynamically. Different classes might map to quality-of-service levels, or to backup policies, or to arbitrary policies determined by the cluster administrators. 

apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
reclaimPolicy: Retain
allowVolumeExpansion: true
mountOptions:
   debug
volumeBindingMode: Immediate
