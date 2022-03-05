package doms.gitops.kcc.gcp_project.limit_bandwidth.apis

default allow = false

vpc_name := [ vpc | item:=input.vpcs[vpc] ]
requested_speeds := [item | item := input.vpcs[_].interconnectRouterDef[_].partnerInterconnect.connectionSpeed]
allowed_value := [item | item:= data.bandwidth.allowedRates[vpc_name[0]][_]]
default_value := [item | item:= data.bandwidth.allowedRates.anybody[_]]

allow {
	all_in(requested_speeds, allowed_value)
}

allow {
	all_in(requested_speeds, default_value)
}

all_in( items, list) {
  not_any_not_in(items, list)
}

not_any_not_in(items, list) {
  l = [item | item := not_in_list(items[index], list)]
  count(l) == 0
}

not_in_list(item, list) {
  not in_list(item, list)
}

in_list(item, list) {
	list[_] = item
}
