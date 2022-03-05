#pylint: disable=C0301, C0103, C0114, E0401
# This script may be used to convert gcloud iam service account list to Kohl's gitops config
# Before executing this script;
#     Run gcloud iam service-accounts list --project doms-cpe-kcc-lle --format yaml > service-accounts.yml
#     where you change the --project parameter to whatever project you want the service account list
#     generated from.
# The service-accounts.yml file that is output from the gcloud command will be input into this script.
# Make sure you execute this script from the same directory where the service-accounts.yml file saved.
#
# The output of this script can be save as an iam-service-accounts.yml configuration file for gitops

import yaml

sa_config = {}
sa_config['iamServiceAccounts'] = {}

with open('service-accounts.yml') as f:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)

    for doc in docs:
        if doc['name'][-23:] == 'iam.gserviceaccount.com':
            sa_fqn = doc['name']
            sa_name = (sa_fqn.split('/', 4))[3]
            sa_short_name = (sa_name.split('@',2)[0])
            sa_display_name = doc['displayName']
            if 'description' in doc:
                sa_description = doc['description']
                sa_info = {'displayName' : sa_display_name, 'description' : sa_description}
            else:
                sa_info = {'displayName' : sa_display_name}
            sa_config['iamServiceAccounts'][sa_short_name] = sa_info
print("---")
print(yaml.dump(sa_config))
with open('iam-service-accounts.yml', 'w') as outfile:
    outfile.write("---\n")
    yaml.dump(sa_config, outfile, default_flow_style=False)
