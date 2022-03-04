# GKE cluster build process

## Summary

> Warning: Communication to your GKE master comes with caveats as it is exposed to Kohl's over a VPC peer link.  Communicate to the master nodes are only available from OnPrem, and from the same NetX VPC that the GKE cluster is deployed to.  Access to the master from all other networks will require a jump box or a proxy instance to receive and re-source the traffic to the destination.

> Warning: Communication to GKE clusters in the East region may not be functional from OnPrem due to regional ILB limitations.  

The project parameters will require the following updates to create a functional GKE cluster:
1. Prerequisites
2. GKE Subnet Deployment
3. Cluster Service API Enablement
4. Container SA permissions for Host Project
5. Cluster and NodePool Definitions
6. Advertise GKE Master range to OnPrem.

## 1. Prerequisites

The environment housing your GKE cluster can only be deployed in the GitOps/NetX configuration.  Both the host project and the service project must be managed by GitOps tooling.

## 2. GKE Subnet Deployment

Create a GKE subnet `yml` file within the context of your host project.  Follow GKE subnet deployment guidelines found in this document: `vpcNetworksAndSubnetworks.md`.  Special attention will be needed to determine subnet sizing as this cannot be modified when the subnetwork is created.  Both the subnet and the cluster will have to be destroyed to modify your cluster sizing.

> Note: In rare cases, you will be permitted to deploy  RFC-1918 subnet space for pod and service ranges.  Staff creating IP subnets will need to choose non-RFC 1918 addresses to use.  Consult with with Network Engineering to understand if routeable IP space is required or if non-routeable IP space is sufficent. 

> Please consult Google documentation on [IP addressing for GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/alias-ips#cluster_sizing).  

After deploying your GKE subnet information, the result should be similar to this:

```yaml
# demo-nx-lle

---
vpcs:
  demo-nx-lle:
    subnets:

      demo-nx-lle-samplesubnet-c1-gke01:
        advertiseRoutes: true
        region: us-central1
        network:
          ip: 10.255.1.1/26
          bluecat-id: 1491253
        gke:
        - podNetwork:
            name: cpe-nx-lle-gitops-c1-pod01
            ip: 240.0.0.0/22
          serviceNetwork:
            name: cpe-nx-lle-gitops-c1-svc01
            ip: 241.0.0.0/27
          masterNetwork:
            ip: 10.120.254.240/28
            bluecat-id: 1491267
        permissions:
          groupsByEmail:
          - gcp-demo-devops-admin@kohls.com
          - gcp-demo-devops-l3@kohls.com
```

## 3. Cluster Service API Enablement

GKE clusters require staff to enable the API in the `project.yml` file that is in your service project.

```yaml
serviceAPIs:
  compute.googleapis.com:
  oslogin.googleapis.com:
  cloudresourcemanager.googleapis.com:
  storage-component.googleapis.com:
  storage-api.googleapis.com:
  stackdriver.googleapis.com:
  logging.googleapis.com:
  monitoring.googleapis.com:
  cloudasset.googleapis.com:
  container.googleapis.com:  #<------------
```

## 4. Container SA permissions for Host Project

A PR may be required at this point to activate the container API in your service project.  Doing so should create some service accounts automatically.  These service accounts need to be used to grant permissions in the host project to use subnetwork and compute resources.

The following lines are needed in the IAM Policy Members `yaml` document in the host project

```yaml
---
iamPolicyMembers:
  serviceAccountsByEmail:
    service-XXXXXXXX@container-engine-robot.iam.gserviceaccount.com:
      roles:
        - container.hostServiceAgentUser
        - compute.networkUser
    XXXXXXXX-compute@developer.gserviceaccount.com:
      roles:
        - compute.networkUser
    XXXXXXXX@cloudservices.gserviceaccount.com:
      roles:
        - compute.networkUser
```
>Note: XXXXXXXX denotes your project number.  To find this reference your service project summary page.  The roles should be listed exactly as they are.

## 5. Cluster and NodePool Definitions

A `cluster.yml` file should be created in your service project folder.  This file should include the following information.  Follow notations commented below.

```yaml
---
clusters:
- name: kohls-demo-lle-01
  xpnProjectName: kohls-demo-lle
  displayName: kohls-demo-lle-01
  initialNodeCount: 1
  location: us-central1-c
  masterIpv4CidrBlock: 10.120.255.80/28  # Pulled from Subnetwork Object
  network: projects/kohls-cpe-xpn-lle/global/networks/cpe-nx-lle #API path to VPC name
  externalNetwork: true
  subnetwork: projects/kohls-cpe-xpn-lle/regions/us-central1/subnetworks/cpe-nx-lle-demo-c1-gke01 # API path to Subnetwork object name
  externalSubnetwork: true
  podSubnetwork: cpe-nx-lle-demo-c1-pod01  # name of secondary range for pods
  serviceSubnetwork: cpe-nx-lle-demo-c1-svc01 # name of secondary range for services
  cloudrunConfig:
    disabled: true
  horizontalPodAutoscaling:
    disabled: false
  httpLoadBalancing:
    disabled: false
  istioConfig:
    disabled: true
  networkPolicyConfig:
    disabled: false
  nodePools:
  - name: kohls-demo-lle-01-nodepool
    machineType: n1-standard-1
    maxPodsPerNode: 16
    maxNodeCount: 7
    minNodeCount: 1
    location: us-central1-c
    oauthScopes:
    - https://www.googleapis.com/auth/devstorage.read_only
    - https://www.googleapis.com/auth/logging.write
    - https://www.googleapis.com/auth/monitoring
    - https://www.googleapis.com/auth/servicecontrol
    - https://www.googleapis.com/auth/service.management.readonly
    - https://www.googleapis.com/auth/trace.append
```

## 6. Advertise GKE Master range to OnPrem.

> NOTE:  All VPN and/or Interconnect related tasks should be validated or performed by Network Engineering staff at Kohl's.  Attempts to push your own updates to routes, router, interconnect, or VPN objects in Google may impact network connectivity within your project and possibly workloads in Cloud environments and on-prem locations such as stores. 

With the previously listed steps, the GKE cluster would be build and functional.  However, master ranges are not found in the VPC and are instead advertised over a VPC Peer link.  In order to ensure that onPrem users can reach the master range, staff must manually advertise the master ranges out of their onprem cloud routers.  To do this, modifications to theri onprem cloud router will look like this.

```yaml
---
vpcs:
  demo-nx-lle:

    interconnectRouterDef:
      demo-nx-lle-c1-pi-rtr01:
        region: us-central1
        description:
        advertiseMode: CUSTOM  # Change from DEFAULT to CUSTOM
        custom_advertised_ip_ranges:
          includeSubnetDef: true
          customIPList:
          - 10.120.254.240/28 # Master Subnet as defined in your GKE definition.
        partnerInterconnect:
          description: 
          availabilityDomain: 1
          vlanId:
          connectionSpeed: 50MB
```
