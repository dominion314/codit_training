package kohls.gitops.kcc.gcp_project.service.apis
default allow = false

environment := replace(replace(replace(input.project.labels["environment-type"], "ops", "nonprd"), "hle", "nonprd"), "lle", "nonprd")

# requested_service_apis := [ api | item:=input.serviceAPIs[api] ]
requested_service_apis[api] { item:=input.serviceAPIs[api] }

# allowed_service_apis_per_env := [item | item := data.service.allowedAPIs[environment][_] ]
allowed_service_apis_per_env[item] { item := data.service.allowedAPIs[environment][_] }

project_id := input.project.name
# allowed_service_apis_per_project := [ item | item := data.service.allowedAPIsPerProject[project_id][index] ]
allowed_service_apis_per_project[item] { item := data.service.allowedAPIsPerProject[project_id][index] }

# allowed_service_apis = merge(allowed_service_apis_per_env, allowed_service_apis_per_project)
allowed_service_apis = allowed_service_apis_per_env | allowed_service_apis_per_project

denied_service_apis = requested_service_apis - allowed_service_apis

policy_violation := {{"Denied Service Apis", denied_service_apis}}

allow {
    denied_service_apis_count := count(denied_service_apis)
    denied_service_apis_count == 0
}
