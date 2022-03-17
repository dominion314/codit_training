# VPC Peering

VPC Peering is achieved with the template `vpcPeering.yml.j2`  This template requires a parameter file formated as `{{ VPC_NAME }}-networkpeering.yml`  The format of the parameters is as follows:

```yaml
---
vpcs:
  {{ VPC_NAME }}:
    vpcPeering:

      {{ VPC_PEER_NAME }}:
        remoteProject: {{ REMOTE_PROJECT_ID }}
        remoteVPC: {{ REMOTE_PROJECT_VPC }}
```

The peering configuration will need to be completed on BOTH sides of the peer, each referencing the other project and VPC

Ensure that a user configuring this setting understands the limitations of VPC peering two VPCs together.  [Google Documentation](https://cloud.google.com/vpc/docs/vpc-peering)
