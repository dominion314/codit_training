# Elective FW rules

Within the netX codebase, instead of just populating global firewall rules by default in all projects, we have created an opt-in process for firewall rules that teams may require.  This keeps consistent with least privilege and allows customers to easily pick and choose which of these rules they may need and enable it with a few lines of code and a PR.

## Initial approval of all **NEW** Elective FW Rules
In order to maintain security standards and ease audit compliance reporting, we currently need to open a SNOW (ServiceNow) request for NEW Elective FW Rules (a link to the request form will be provided once this new form is finished).  Security will review this request and provide an approval that covers all future teams enabling this rule in their project.  To be clear, this SNOW request will only be required for the initial approval.  Once a rule is approved, the Elective FW Rule can be enabled via MR - no SNOW request required.

As part of the initial rule approval, create a MR and place it in draft status.  This will be used during the security review.  Cross-reference this MR in the SNOW request.  Once the security team approves the addition, your MR can be processed


## Available Elective FW Rules
Within the gcp-config repo, navigate to the "default-vars" folder and look for any yml files that begin with "elec" - these are the various elective rules that are available.  The remainder of the name should give a decent indication of what it is used for.  Within each file there is a top level key of "electiveRules" followed by a key that is used to describe the following rules in their entirety(in the example below it is "MySQLRules").  It is this name that you will need to put into your project files if you require the underlying rules.  In each firewall rule listed below this key, include a description referencing the ServiceNow Request number for cross-referencing.
```yml
---
electiveRules:
  MySQLRules:
    elec-mysql-fw-01:
      description: SNOW-16311 #Ingress to MySQL instances
      ...
    elec-mysql-fw-02:
      description: SNOW-16311 #Ingress to MySQL instances
      ...
```
## Enabling an Elective FW Rule in your VPC
Within the gcp-config repo, navigate to your project folder and open the {{ vpc_name }}-firewall.yml
Within this file, inside your VPC key add a new key : "electiveFWrules" (this is at the same level/indent as the "firewallRules" key)
Inside of electiveFWrules you now simply list the elective firewall rule names that you require
```yml
---
vpcs:
  platform-nx-lle:
    electiveFWrules:
    - MySQLRules
    - akamaiRules
    firewallRules:
      griddynamics-02-lle-ingress:
      griddynamics-03-lle-ingress:
```

Once merged to master with a valid MR, the elective rules will be implemented inside your project.

**Note:**
*Should you require elective rules that could be reused in numerous projects please contact Cloud Networking team*
