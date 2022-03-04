# How to Enable Mongo Atlas in a Project

**PLEASE NOTE**: If you are using the Openshift platform, this has already been done for you.  This process only applies to standalone projects.

In order to enable conectivity to Mongo Atlas for your project, follow the steps below.  

## Enabling an Elective FW Rule in your VPC
Within the gcp-config repo, navigate to your project folder and open the {{ vpc_name }}-firewall.yml
Within this file, inside your VPC key add a new key : "electiveFWrules" (this is at the same level/indent as the "firewallRules" key)
Inside of electiveFWrules you now simply list the elective firewall rule names that you require.
```yml
---
vpcs:
  platform-nx-lle:
    electiveFWrules:
    - mongoAtlasRules
    firewallRules:
      griddynamics-02-lle-ingress:
```

## Enable NAT Gateway
This is a one-time configuration that will only need to be performed the first time you enable connectivity to Mongo Atlas.  This is performed in the {{vpc_name}}-connect-gcp.yml file that is located in the host project (xpn) repo for your project.  Within this file, inside your Cloud Router key ( "{{vpc_name}}-c1-gcp-rtr01:" ), add a new key: "cloudNat" (this is indented one level/indent from your region's Cloud Router key).  You will need to do this for each region you would like to enable access to Mongo Atlas from.  Inside of cloudNat, you now list the configuration as shown in the example below, but updating "{{vpc_name}}" with your actual VPC name.

```yml
---
  demo-nx-lle:
    routerDef:
      {{vpc_name}}-c1-gcp-rtr01: # "c1" indicates this is the Central region Cloud Router
        cloudNat:
          name: {{vpc_name}}-c1-nat-gateway #create NAT gateway for Central region
          logConfig:
            enable: true
            filter: ERRORS_ONLY
          manualAddresses: 2
          min_ports_per_vm: 1024

      {{vpc_name}}-e1-gcp-rtr01: # "e1" indicates this is the East region Cloud Router
        cloudNat:
          name: {{vpc_name}}-e1-nat-gateway #create NAT gateway for East region
          logConfig:
            enable: true
            filter: ERRORS_ONLY
          manualAddresses: 2
          min_ports_per_vm: 1024
```

## Enable access on Specific Subnets
This configuration is performed to enable any desired subnets to utilize the new NAT Gateway, thereby providing Mongo Atlas connectivity.  This is performed in the {{vpc_name}}-subnetwork-std.yml file that is located in the host project (xpn) repo for your project.  Within this file, inside your Subnet key (ex - "{{vpc_name}}-some_app-c1-prv01" ), add a new key: "natRouter" and give it the value of the corresponding region's router specified in the step above.

```yml
      {{vpc_name}}-openshift-c1-prv01: #Central region subnet name
        natRouter: {{vpc_name}}-c1-gcp-rtr01 #Central region Cloud Router name

      {{vpc_name}}-openshift-e1-prv01: #East region subnet name
        natRouter: {{vpc_name}}-e1-gcp-rtr01 #East region Cloud Router name
```