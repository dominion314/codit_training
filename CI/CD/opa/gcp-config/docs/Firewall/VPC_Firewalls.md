# vpcFirewalls.yml.j2

The `vpcFirewall.yml.j2` template pulls information from the gcp-config repo file `{{ VPC_NAME }}-firewall.yml` and `default-firewall.yml` definitions in the `default` portion of the hierarchy. The structure of the VPC specific file is as follows.

```yaml
vpcs:
  {{ VPC_NAME }}:

    firewallRules:
      {{ FW_RULE_NAME }}:
        priority: 900                 #1-2000
        direction: (INGRESS|EGRESS)
        description: {{ RULE_DESC }}  # Often SCTASK ID
        disabled: (true | false)      # Will Disable Rule
        logging: (true | false)       # Keep as False
        rule:
          destinationRanges:          # List of IP Ranges
          targetServiceAccounts:      # List of Service Accts.
          targetTags:                 # List of Tags
          sourceRanges:               # List of IP Ranges
          sourceServiceAccounts:      # List of Service Accts.
          sourceTags:                 # List of Tags
          deny:
            - protocol:               # String: TCP|UDP|ICMP
              ports:                  # List of Port Numbers
          allow:
            - protocol:               # String: TCP|UDP|ICMP
              ports:                  # List of Port Numbers
```
| Parameters                 | Notes                                                             |
|----------------------------|-------------------------------------------------------------------|
| FW_Rule_Name               | Google naming standards.  See Naming standards                    |
| priority                   | Required. Lower is higher priority.  Keep at 900 unless necessary |
| direction                  | Required. INGRESS or EGRESS.                                      |
| Description                | Optional. Often SCTASK                                            |
| disabled                   | Required. Create the rule but disable it. Keep as false           |
| logging                    | Required. Leave as False. Extremely expensive                     |
| rule                       | Section is Required                                               |
| rule.destinationRanges     | TBD                                                                  |
| rule.targetServiceAccounts | TBD                                                                  |
| rule.targetTags            | TBD                                                                 |
| rule.sourceRanges          | TBD                                                                  |
| rule.sourceServiceAccounts | TBD                                                                  |
| sourceTags                 | TBD                                                                  |
| rule.deny                  | If denying traffic section accepts a list of protocol and port    |
| rule.allow                 | If allowing traffic, section accepts a list of protocol and port  |