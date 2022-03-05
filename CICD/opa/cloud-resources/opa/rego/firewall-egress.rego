package kohls.gitops.kcc.gcp_project.firewall_egress.apis

default allow = true

allow = false {
	egress_rules
	is_null(egress_rules[_].rule.destinationRanges)
}

egress_rules[fwrules] {
	some fw
	fwrules := input.vpcs[_].firewallRules[fw]
	fwrules.direction == "EGRESS"
}
