# Installing OpenShift 4.x

To deploy an OpenShift 4.x cluster in GCP, there are various resources in GCP that have to be provisioned before you can deploy the cluster. These required resources are listed here.

## Host Project Resources

- Create subnetwork (make sure to allocate from [OpenShift Supernet, ref "Allocation Keyphrase"](../Network/IP_Address_Allocation.md))
- Grant xPaaS teams and service accounts access to subnetworks
- Create role bindings for service accounts and xPaaS teams
- Create firewall rules
- Enable Cloud DNS
- Share host project with service project

## Service Project Resources

- Enable Cloud APIs
- Create service accounts for the installer and various node types
- Create role bindings for service accounts and xPaaS teams
