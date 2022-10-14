package commonmerit.gitops.kcc.gcp_project.project
default allow = false

environment := replace(replace(replace(input.project.labels["environment-type"], "ops", "nonprd"), "hle", "nonprd"), "lle", "nonprd")
cluster := data.cluster

domain := input.project.labels["product-domain"]
has_domain = true{
	domain
} else = false

billing_Id = {format_int(input.billingDeptId, 10)} {
    is_number(input.billingDeptId)
} else = {input.billingDeptId}
billing_Id_label = {format_int(input.project.labels["billing-dept-id"], 10)} {
    is_number(input.project.labels["billing-dept-id"])
} else = {input.project.labels["billing-dept-id"]}

has_billing_IDs = true{
        billing_Id
        billing_Id_label
    } else = false

requested_environment_per_FolderID = {format_int(input.project.folderId, 10)} {
    is_number(input.project.folderId)
} else = {input.project.folderId}

allowed_environment_per_FolderID[item] { item := data.project[cluster].allowedFolderId[environment][_][_] }
allowed_environment_per_FolderID_Legacy[item] { item := data.project[cluster].allowedFolderIdLegacy[environment][_] }
allowed_environment_per_FolderID_List[item] { item := data.project[cluster].allowedFolderId[environment][_] }

allowed_environment_per_FolderID_Domain = {data.project[cluster].allowedFolderId[environment][_][domain]}{
    has_domain
}else = {"Product Domain is Invalid or Not Given per Environment"}

requests_legacy_FolderID = true  {
    requests_legacy_FolderID_number := allowed_environment_per_FolderID_Legacy - requested_environment_per_FolderID
    requests_legacy_FolderID_true := count(allowed_environment_per_FolderID_Legacy) == count(requests_legacy_FolderID_number)
    requests_legacy_FolderID_true == false
    has_domain == false
}else = false

denied_environment_per_FolderID = requested_environment_per_FolderID - allowed_environment_per_FolderID_Domain{
	has_domain
}else = requested_environment_per_FolderID - allowed_environment_per_FolderID_Legacy - allowed_environment_per_FolderID

write_ID_error_without_domain = true{
	has_domain == false
    denied_environment_per_FolderID_count_policy = count(denied_environment_per_FolderID)
    denied_environment_per_FolderID_count_policy != 0
} else = false

write_ID_error_with_domain = true{
	has_domain == true
    denied_environment_per_FolderID_count_policy_domain = count(denied_environment_per_FolderID)
    denied_environment_per_FolderID_count_policy_domain != 0
} else = false

write_billing_match_error = true{
    has_billing_IDs == true
    billing_Id != billing_Id_label
} else = false

policy_violation := {{"Denied Environment Type with FolderID, Allowed FolderIDs", allowed_environment_per_FolderID_List, write_ID_error_without_domain},
					{"Denied Environment Type with FolderID and Product Domain, Allowed FolderID", allowed_environment_per_FolderID_Domain, write_ID_error_with_domain},
                    {"Denied Billing Department ID, billingDeptId and billing-dept-id must match.", write_billing_match_error},
                    {"Warning. You are using a legacy FolderID. Please update your FolderID to the current standards from the following",
                    allowed_environment_per_FolderID_List, requests_legacy_FolderID}}

allow {
    denied_environment_perID_count := count(denied_environment_per_FolderID)
    denied_environment_perID_count == 0
    write_billing_match_error == false
}