package kohls.gitops.kcc.gcp_project.big.query.datasets
default allow = false

required_roles[item] { item := data.bigQueryDatasets.requiredRoles[_] }
datasets = [name | value := input.bigQueryDatasets[name]]
denied_datasets := [dataset | dataset := datasets[_]
				  is_missing_required_roles(dataset)]

is_missing_required_roles(dataset){
    groups := [item | item := input.bigQueryDatasets[dataset].permissions.groupsByEmail]
	group_roles := [item | item := groups[_][_].roles]
    requested_group_roles := {role | role := group_roles[_][_] } # make it a set

	users := [item | item := input.bigQueryDatasets[dataset].permissions.usersByEmail]
	users_roles := [item | item := users[_][_].roles]
    requested_users_roles := {role | role := users_roles[_][_] } # make it a set

	service_accounts := [item | item := input.bigQueryDatasets[dataset].permissions.serviceAccountsByEmail]
	service_accounts_roles := [item | item := service_accounts[_][_].roles]
    requested_service_accounts_roles := {role | role := service_accounts_roles[_][_] } # make it a set

	missing_required_roles := required_roles - requested_group_roles - requested_users_roles - requested_service_accounts_roles
	counting := count(requested_group_roles) + count(requested_users_roles) + count(requested_service_accounts_roles)

	emptyRoles_or_missing(counting,missing_required_roles)
}

emptyRoles_or_missing(counting,missing_required_roles) = false{
	counting == 0
} else{
	count(missing_required_roles) > 0
}

policy_violation := {{concat(" ",{"Following Datasets Denied, Missing All Required Roles -"} | required_roles), denied_datasets}}

allow{
	count(denied_datasets) == 0
}

