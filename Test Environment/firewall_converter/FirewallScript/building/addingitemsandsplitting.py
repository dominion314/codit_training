import json

#the file they want to load must be local. This file is read only, thus the r.
with open('openshift_hle - openshift_hle.json','r') as file:
    data = json.load(file) #Load the file in JSON and read

    for item in data:

        target_tags = item['targetTags'].split(',') #python has a module called split that will split on a specific character, in this case a comma. 
        
        print(target_tags)
        exit()

        
        structured_data = {
             "vpcs": {
                item['name']: {
                    "firewallRules": {
                        item["Networks"]: {
                        "priority": item['priority'],
                        "direction": item['direction'],
                        "description": "", #TODO not included in template
                        "disabled": item['disabled'],
                        "logging": False,
                        "rule": {
                            "destinationRanges": destination_Ranges,
                            "targetServiceAccounts": None,
                            "targetTags": target_tags, ##created a list here.
                            "sourceRanges": source_Ranges,
                            "sourceServiceAccounts": None,
                            "sourceTags": source_Tags,
                            "allow": allowed_data
                        }
                        }
                    }
                }
            }
        }