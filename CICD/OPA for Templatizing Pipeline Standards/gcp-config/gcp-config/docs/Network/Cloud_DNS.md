# Cloud DNS

The template cloud-dns.yml.j2 contains the operator CRs to create a Cloud DNS (`DNSManagedZone`) peering zone for a given VPC.

## Enabling Cloud DNS  

A new file should be created in the XPN project for the VPC, with the format below. If this file does not exist, or enable is false, Cloud DNS will not be enabled.

```yml
---
cloudDNSPeering:
  enable: true

```

This will enable Cloud DNS for all VPCs in the XPN project. To use Cloud DNS, your compute instances must reference your projects metadata servers for their DNS configuration.

At this time we offer forwaring for `.` which is a wildcard for all DNS records.

**Note:**
*The DNS API is enabled as part of the Cloud DNS template*

*You should NOT add the DNS API to your project file*

*Logging is required and enabled by default*
