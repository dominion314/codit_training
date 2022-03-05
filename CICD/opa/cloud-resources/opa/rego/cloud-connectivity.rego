package kohls.gitops.kcc.gcp_project.cloud_connectivity

default allow = true

#Deny subnets not in override list
allow = false {
	not_in_list(advertised_interconnectRouter_subnets[_], allowed_subnets)
}

#Deny subnets not in overrride list
allow = false {
	not_in_list(advertised_router_subnets[_], allowed_subnets)
}

#Deny more than 2 routers in central
allow = false {
	central
}

#Deny more than 2 routers in east
allow = false {
	east
}

#Creat list of requested interconnect subnets
advertised_interconnectRouter_subnets[isubnets] {
	some interconnectRoutes
	input.vpcs[_].interconnectRouterDef[_].advertiseMode != "DEFAULT"
	isubnets := input.vpcs[_].interconnectRouterDef[_].custom_advertised_ip_ranges.customIPList[interconnectRoutes]
}

#Create list of requested router subnets
advertised_router_subnets[subnets] {
	some routes
	input.vpcs[_].routerDef[_].advertiseMode != "DEFAULT"
	subnets := input.vpcs[_].routerDef[_].custom_advertised_ip_ranges.customIPList[routes]
}

#Create list of routerDef regions
regions1[region] {
  [_, value] := walk(input.vpcs[_].routerDef[_])
  region = value.region
}

#Create list of interconnect regions
regions2[region] {
  [_, value] := walk(input.vpcs[_].interconnectRouterDef[_])
  region = value.region
}

#Count the number of central matches and true if more than 2
central {
	number := [item | item := contains(regions1[_], "central") ]
    count(number) > 2
}

#Count the number of east matches and true if more than 2
east {
	number := [item | item := contains(regions1[_], "east") ]
    count(number) > 2
}

#Set VPC name as variable
vpc_name := [vpc | item := input.vpcs[vpc]]

#Create list of allowed subnets from the data file
allowed_subnets := [item | item := data.advertisedNetworks.subnets[vpc_name[0]][_]]

#Default general purpose functions below
not_in_list(item, list) {
	not in_list(item, list)
}

in_list(item, list) {
	list[_] = item
}
