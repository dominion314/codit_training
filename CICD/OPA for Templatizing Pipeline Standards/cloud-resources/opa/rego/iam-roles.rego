package commonmerit.gitops.kcc.gcp_project.iam.roles
default allow = false

environment := replace(replace(replace(input.project.labels["environment-type"], "ops", "nonprd"), "hle", "nonprd"), "lle", "nonprd")

# users with associated IAM roles
users := input.iamPolicyMembers.usersByEmail
user_roles := [item | item := users[_].roles]
# make it a set
requested_user_roles[role] { role := user_roles[_][_] }
# all allowed user IAM roles in given environment
#allowed_user_roles_general := [role | item := data.iam.allowedRoles[environment].roles[index][role]; data.iam.allowedRoles[environment].roles[index][role].allowedForUsers==true ]
allowed_user_roles_general[role] { item := data.iam.allowedRoles[environment].roles[index][role]; data.iam.allowedRoles[environment].roles[index][role].allowedForUsers==true }

# groups with associated IAM roles
groups := input.iamPolicyMembers.groupsByEmail
group_roles := [item | item := groups[_].roles]
# make it a set
requested_group_roles[role] { role := group_roles[_][_] }
# all allowed group IAM roles in given environment
#allowed_group_roles_general := [role | item := data.iam.allowedRoles[environment].roles[index][role]; data.iam.allowedRoles[environment].roles[index][role].allowedForGroups==true ]
allowed_group_roles_general[role] { item := data.iam.allowedRoles[environment].roles[index][role]; data.iam.allowedRoles[environment].roles[index][role].allowedForGroups==true }

# Service Accounts with associated IAM roles
sas := input.iamPolicyMembers.serviceAccountsByEmail
sa_roles := [item | item := sas[_].roles]
# make it a set
requested_sa_roles[role] {role := sa_roles[_][_] }
# all allowed Service Account IAM roles in given environment
allowed_sa_roles_general[role] { item := data.iam.allowedRoles[environment].roles[index][role]; data.iam.allowedRoles[environment].roles[index][role].allowedForServiceAccounts==true }

# load project specific entitelements
project_id := input.project.name
allowed_user_roles_per_project[role] { item := data.iam.allowedRolesPerProject[project_id].roles[index][role]; data.iam.allowedRolesPerProject[project_id].roles[index][role].allowedForUsers==true }
allowed_group_roles_per_project[role] { item := data.iam.allowedRolesPerProject[project_id].roles[index][role]; data.iam.allowedRolesPerProject[project_id].roles[index][role].allowedForGroups==true }
allowed_sa_roles_per_project[role] { item := data.iam.allowedRolesPerProject[project_id].roles[index][role]; data.iam.allowedRolesPerProject[project_id].roles[index][role].allowedForServiceAccounts==true }

# create combined 'allowed' sets
allowed_user_roles = allowed_user_roles_general | allowed_user_roles_per_project
allowed_group_roles = allowed_group_roles_general | allowed_group_roles_per_project
allowed_sa_roles = allowed_sa_roles_general | allowed_sa_roles_per_project

# created denied sets
denied_user_roles := requested_user_roles - allowed_user_roles
denied_group_roles := requested_group_roles - allowed_group_roles
denied_sa_roles := requested_sa_roles - allowed_sa_roles

policy_violation := {{"Denied User Roles", denied_user_roles}, {"Denied Group Roles", denied_group_roles}, {"Denied Service Account Roles", denied_sa_roles}}

# Allow if all denied roles counts for users, groups and service accounts are 0
allow {
    denied_user_roles_count := count(denied_user_roles)
    denied_user_roles_count == 0

    denied_group_roles_count := count(denied_group_roles)
    denied_group_roles_count == 0

    denied_sa_roles_count := count(denied_sa_roles)
    denied_sa_roles_count == 0
}
