import json

#the file they want to load must be local. This file is read only, thus the r.
with open('openshift_hle - openshift_hle.json','r') as file:
    data = json.load(file) #Load the file in JSON and read

    for item in data:
        
        structured_data = {
            "vpcs": {
                item['name']
            }
        }

        print(structured_data)
        exit()


# {
#                 "vpcs": {
#                 item['name']: {
#                     "firewallRules": {
#                         item["Networks"]: {
#                         "priority": item['priority'],
#                         "direction": item['direction'],
#                         "description": "",
#                         "disabled": item['disabled'],
#                         "logging": False,
#                         "rule": {
#                             "destinationRanges": destination_Ranges,
#                             "targetServiceAccounts": None,
#                             "targetTags": target_tags,
#                             "sourceRanges": source_Ranges,
#                             "sourceServiceAccounts": None,
#                             "sourceTags": source_Tags,
#                             "allow": allowed_data
#                         }
#                         }
#                     }
#                 }
#             }
#         }