import json

#the file they want to load must be local. This file is read only, thus the r.
with open('openshift_hle - openshift_hle.json','r') as file:
    data = json.load(file) #Load the file in JSON and read

    print(data)
    