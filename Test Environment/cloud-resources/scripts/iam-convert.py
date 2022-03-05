#pylint: disable=C0301, C0303, C0103, C0114, E0401
# This script may be used to convert gcloud iam service account list to Kohl's gitops config
# Before executing this script;
#     Run gcloud projects get-iam-policy doms-cpe-cpa-lle --format yaml > iam-bindings.yml
#     where you replace doms-cpe-cpa-lle with the project that you want to export iam bindings from.
# The iam-bindings.yml file that is output from the gcloud command will be input into this script.
# Make sure you execute this script from the same directory where the iam-bindings.yml file is saved.
#
# Output of this script is displayed in the shell console and is saved as a gitops configuration
# file named iam-policy-members.yml
import yaml

with open('iam-bindings.yml') as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.FullLoader)

iam_config = {}
iam_config['iamPolicyMembersV2'] = {}
iam_config['iamPolicyMembersV2']['usersByEmail'] = {}
iam_config['iamPolicyMembersV2']['groupsByEmail'] = {}
iam_config['iamPolicyMembersV2']['serviceAccountsByEmail'] = {}
for bindings in data['bindings']:
    members = bindings['members']
    fqn_role = bindings['role']
    #print(fqn_role)
    if fqn_role[:13] == 'organizations':
        custom_role = True
        org_id = (fqn_role.split('/', 3))[1]
        role = (fqn_role.split('/', 3))[3]
        #print(org_id, role)
    elif fqn_role[:8] == 'projects':
        custom_role = True
        print('GitOps process currently does not support project level custom roles')
    else:
        custom_role = False
        role = (fqn_role.split('/', 1))[1]
        #print(role)
    for member in members:
        fqn_member = member.split(':', 1)
        member_type = fqn_member[0]
        member_name = fqn_member[1]
        #print(member_name)
        if member_type == "user":
            member_type = "usersByEmail"
        elif member_type == "group":
            member_type = "groupsByEmail"
        elif member_type == "serviceAccount":
            member_type = "serviceAccountsByEmail"
        else:
            member_type = "unsupported"
        if member_type == "unsupported":
            print("Skipping unsupported member: " + member)
        else:
            if member_name not in iam_config['iamPolicyMembersV2'][member_type].keys():
                iam_config['iamPolicyMembersV2'][member_type][member_name] = []
            if custom_role:
                test = {'role' : role, 'OrgId' : org_id}
                iam_config['iamPolicyMembersV2'][member_type][member_name].append(test)
            else:
                test = {'role' : role}
                iam_config['iamPolicyMembersV2'][member_type][member_name].append(test)

print(yaml.dump(iam_config))
with open('iam-policy-members.yml', 'w') as outfile:
    outfile.write("---\n")
    yaml.dump(iam_config, outfile, default_flow_style=False)
