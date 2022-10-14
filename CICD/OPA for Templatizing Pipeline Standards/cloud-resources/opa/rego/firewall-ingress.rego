package commonmerit.gitops.kcc.gcp_project.firewall_ingress

default allow = true

#deny 0.0.0.0/0 subnet
allow = false {
    sourceRanges := input.vpcs[_].firewallRules[_].rule.sourceRanges[_]
    sourceRange := split(sourceRanges, ",")[_]
    
    trim_space(sourceRange) == "0.0.0.0/0"
}

#deny for rules containing destination IPs
allow = false {
	ingress_rules
	is_array(ingress_rules[_].rule.destinationRanges)
}

#deny rules that are not priority 900 that are not whitelisted
allow = false {
	not_in_list(NonDefault_rules[_][_], Whitelisted_rules)
}

#deny disabled rules if there is not an exemption for it
allow = false {
	not_in_list(disabled_rules[_][_],disable_exemption)
}

#define list of rules that are ingress
ingress_rules[fwrules] {
	some fw
	fwrules := input.vpcs[_].firewallRules[fw]
	fwrules.direction == "INGRESS"
}

#define list of non 900 priority rules
NonDefault_rules[rname] {
	some j
	input.vpcs[_].firewallRules[j].priority != 900
	input.vpcs[_].firewallRules[j].direction == "INGRESS"
	rname := [item | item := {j: input.vpcs[_].firewallRules[j].priority}]
}

#define list of currently disabled rules
disabled_rules [drules] {
    input.vpcs[_].firewallRules[j].disabled == true
    drules := [ j | item := {j:input.vpcs[_].firewallRules[j]}]
}

#define list of whitelisted rules
Whitelisted_rules := [item | item := data.exemptedPriorities[vpc_name[0]][_]]

#define disabled exemption list
disable_exemption := data.disable_exception[vpc_name[0]]

#set VPC Name
vpc_name := [vpc | item := input.vpcs[vpc]]

#not in list function
not_in_list(item, list) {
	not in_list(item, list)
}

#in list function
in_list(item, list) {
	list[_] = item
}
