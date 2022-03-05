package kohls.gitops.kcc.gcp_project.single.vpc

default allow = false

#Allow a single VPC with autoConnectSubnet false
allow {
	one_vpc
	auto_create_false
}

#Allow a single VPC with autoConnectSubnet true with override file
allow {
	one_vpc
	all_in(vpc_name, autocreate_allowed)
}

#Allow projects with no VPC/subnets to pass check
allow {
	vpc_name == []
}

#Validate there is only 1 VPC
one_vpc {
	count(input.vpcs) == 1
}

#Verify autoCreateSubnets is false
auto_create_false {
	input.vpcs[_].autoCreateSubnets == false
}

#Set VPC Name
vpc_name := [vpc | item := input.vpcs[vpc]]
#Create list of allowed autoCreateSubnets Override Projects
autocreate_allowed := [item | item:= data.autoCreateAllowed[_]]

#Base functions
all_in(items, list) {
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
