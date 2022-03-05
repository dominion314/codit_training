"""
This is used to convert JSON firewall dumps from to GCP or AWS to the appropriate YAML format for push requests.

Created on May 2019

@author: dominickhernandez

"""

import json
import yaml

def parse_allowed_values(allowed):
    """This function controls the input of the allowed values."""
    if allowed == "":
        return None
    list_data = allowed.split(",")
    # Clean the data.
    new_data = []
    for item in list_data:
        data = item.strip().replace("'", "").replace("[", "").replace("]", "")
        new_data.append(data)
    # This will iterate through ports, protocols, and icmp.
    values = []
    tcp_ports = {"protocol": "tcp", "ports": []}
    udp_ports = {"protocol": "upd", "ports": []}
    icmp = {"protocol": "icmp"}
    # This loop iterates through all tcp, udp, and icmp values then appends the port numbers.
    for item in new_data:
        if item == "icmp":
            values.append(icmp)
        if ":" in item:
            data = item.split(":")
            protocol = data[0]
            port = data[1]
            if protocol == "tcp":
                tcp_ports["ports"].append(port)
            elif protocol == "udp":
                udp_ports["ports"].append(port)
    # If TCP port doesn't equal an empty list, we will append values for the tcp/udp port.
    if tcp_ports["ports"] != []:
        values.append(tcp_ports)
    if udp_ports["ports"] != []:
        values.append(udp_ports)
    # Extract and return variables.
    return values

def main():
    """This is where you create/remove variables"""
    with open("doms-firewall-rules.json", "r") as file:
        data = json.load(file)
    for item in data:
        target_tags = item["targetTags"].split(",")
        source_ranges = item["sourceRanges"].split(",")
        source_tags = item["sourceTags"].split(",")
        destination_ranges = item["destinationRanges"]
        if destination_ranges == "":
            destination_ranges = []
        else:
            destination_ranges = destination_ranges.split(",")
        allowed_data = parse_allowed_values(item["allowed"])
        # These are the different variables you will bring into your structured data.
        # You can add or remove new key value pairs as needed.
        # Be sure to add new items to the structured data below if you create a new variable.
        structured_data = {
            "vpcs": {
                item["name"]: {
                    "firewallrules": {
                        item["Networks"]: {
                            "name": item["name"],
                            "priority": item["priority"],
                            "direction": item["direction"],
                            "description": "",
                            "disabled": item["disabled"],
                            "rule": {
                                "destinationRanges": destination_ranges,
                                "targettags": target_tags,
                                "sourceranges": source_ranges,
                                "sourcetags": source_tags,
                                "allow": allowed_data,
                            },
                        }
                    }
                }
            }
        }
        data = yaml.dump(structured_data, allow_unicode=True)
        print(data)


if __name__ == "__main__":
    main()
