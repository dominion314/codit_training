allowed = "['tcp:8300,tcp:8301,tcp:8302,tcp:8600']"

list = allowed.split(',')

new_list = []

for item in list:
    data = item.strip().replace("'",'').replace("[","").replace("]",'')
    new_list.append(data)

print(new_list)