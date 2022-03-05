# Development and Testing Setup (Draft)

Development and Testing of the K8s Config Connector is done with a combination of MiniKube (local Kubernetes cluster) with KCC configured within, and deployments should be targeted to dev.doms.com.

## Software Requirements

-----

At this time, development is supported on macOS.  You will need the following resources on your macOS workstation.

- Homebrew
- Minikube
- virtualbox
- kubectl

### 1. Homebrew

Kohl's macOS workstations should come with this preloaded.  If it is not installed visit the [Homebrew website](https://brew.sh/) and follow install instructions.

### 2. Virtualbox

Kohl's offers a Virtualbox installation in self-service.  Open JAMF self-service on your mac and search for virtualbox there.

### 3. kubectl

Now that you have homebrew installed, install kubectl via homebrew with the command in your terminal window

```sh
brew install kubectl
```

### 4. Minikube

Full minikube instructions for installation or upgrades can be found [here](https://minikube.sigs.k8s.io/docs/start/macos/).  The command to use homebrew to install this is as follows.

```sh
brew cask install minikube
```

### 4b. Kind

Running minikube on the Kohl's VPN is very challenging. An alternative to minikube is [Kind](https://github.com/kubernetes-sigs/kind) (Kubernetes In Docker).
See the README.md for the installation documentation, but if you have Docker installed, you should be able to get Kind running with a simple `kind create cluster`.

*NOTE: When starting the cluster, you need the kind node image from dockerhub. If the create cluster command seems to be taking a long time, you can pull the image*
*before running `kind create cluster` and it will use the one you have locally rather than trying to pull it.*

## Minikube and Environment Setup

-----

### Minikube configuration

For some Minikube may work "out of box".  Others may need to configure it to get it working properly.  We recommend that virtualbox be used to virtualize the cluster, however sometimes Minikube may not do this.  To fix this, run the following

```sh
minikube config set vm-driver virtualbox
```

You may also run into an issue where after starting minkube you'll get proxy errors and your `kubectl` commmands won't work.  The minikube cluster requires direct communication to the following IP ranges.

- 192.168.99.0/24
- 192.168.39.0/24
- 10.96.0.0/12

These IP ranges should be added to your environment variables `NO_PROXY` and `no_proxy`.  Comma seperate them and append to whatever else might be in that variable

An example `no_proxy` configuration for doms would be as follows.

```bash
no_proxy=localhost,127.0.0.1,*.cp.ad.doms.com,*.st.ad.doms.com,*.googleapis.com,*.cnrm-system.svc,10.96.0.0/12,192.168.99.0/24,192.168.39.0/24,192.169.99.100

NO_PROXY=$no_proxy
```

See [minikube documentation](https://minikube.sigs.k8s.io/docs/reference/networking/proxy/) for more information on HTTP Proxy settings.

### KCC namespace and SA credentials

Ref: [Google Config Connector Installation Docs](https://cloud.google.com/config-connector/docs/how-to/install-upgrade-uninstall).

Work with internal Kohl's teams to obtain a service account with appropriate access for development work.  The key file provided should be renamed to `key.json` if it isn't named this already.

First create the kube namespace in which KCC will operate.

```sh
kubectl create namespace cnrm-system
```

Next, install the key into the namespace.

```sh
kubectl create secret generic gcp-key --from-file key.json --namespace cnrm-system
```

Remove the key for security

```sh
rm key.json
```

### Install Config Connector

You can download the config connector with the following curl command.

```sh
curl -X GET -sLO \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
--location-trusted \
https://us-central1-cnrm-eap.cloudfunctions.net/download/latest/infra/install-bundle.tar.gz
```

Extract

```sh
tar zxvf install-bundle.tar.gz
```

Apply to the config connector namespace

```sh
kubectl apply -f install-bundle/
```

To verify that config connector is running appropriately, run the following

```sh
kubectl wait -n cnrm-system \
 --for=condition=Initialized pod \
 cnrm-controller-manager-0
```

The response should include:

```sh
pod/cnrm-controller-manager-0 condition met
```

### Testing resources and provisioning with KCC

**WARNING: IF YOU DELETE A KUBERNETES OBJECT THAT CONFIG CONNECTOR IS MANAGING, IT WILL ATTEMPT TO DELETE
THAT RESOURCE IN GCP.**

**When you are cleaning up your dev environment, ensure to delete the minikube cluster
rather than trying to cleanup the resources.**

By default, Config Connector assumes the namespace name is the name of the GCP project it is managing.
Our templated resources are setup to follow the naming standard `gcp-${GCP_PROJECT}`. To get around this,
you can add the annotation `cnrm.cloud.google.com/project-id` to your namespace with the value being the
real name of your GCP project. For example:
```
kubectl create namespace gcp-doms-fake-project-lle
kubectl annotate namespace gcp-doms-fake-project-lle cnrm.cloud.google.com/project-id=doms-fake-project-lle
```

Once you have your namespaces setup, you will need to merge your different vars files for a given project.
You can either include the vars all in a single yaml file, or you can use yq to merge all of your yaml files
in a project directory. For example:

```
yq merge --allow-empty test_vars/gcp_project/doms-dev-cne-demo2-lle/*.yml > test_vars/gcp_project/merged.yml
```

This will provide you a yaml file with all of your merged variables. Once you have your variables, you
can then populate the various Jinja templates with your variables to create your different Kubernetes
objects. If you want to generate all of them at the same time, you can use the following command:

```
find templates/gcp-project/*.yml.j2 -exec sh -c "j2 -f yaml {} test_vars/gcp_project/merged.yml | cat >> bundled-resources.yml
```

This will generate a `bundled-resources.yml` containing all of the resources that have been defined. You
should review these to make sure they are what you are expecting. In addition, you should perform a dry run
of applying the file to ensure it is provisioning what you expect.

```
kubectl apply -f bundled-resources.yml --dry-run
```

Once the resources are added into your minikube cluster, you can see the status of the resources by checking
the events of any resource.

### Handling cross project dependencies

Sometimes when you are provisioning a resource, you need to reference an object in a different GCP project.
A good example of this is a network in an XPN project. For KCC to understand these references, you need to
have both resources present in your Kubernetes cluster.

For example, if you are provisioning a GKE cluster in the `doms-paas-ops` project which has it's network
created in the `doms-paas-xpn-lle` project, you would need to have the following in your Kubernetes cluster:

In the namespace managing the `doms-paas-ops` project:
- The `ContainerCluster` resource defined with the network and subnetwork references

In the namespace managing the `doms-paas-xpn-lle` project:
- The `ComputeNetwork` resource
- The `ComputeSubnetwork` resource

*Note: In config connector version 1.0.0-rc, you will receive an error message when you try to provision
the `ContainerCluster` saying `networkRef` and `subnetworkRef` are invalid fields until they are created
in the Kubernetes cluster.*
