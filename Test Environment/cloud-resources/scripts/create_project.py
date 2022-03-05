# pylint: disable=import-error,W1309
"""
This script needs to be invoked from python3 inside the scripts folder in the Templates repo.
"""



import sys
import os
import re
import random
import yaml
import ruamel.yaml


def project(data):
    """ Takes the vpc name and creates a template for the network yaml """
    if data.get("environment-type") == "prd":
        folder_id = "970875009337"
    else:
        folder_id = "778811484176"
    project_string = """
    billingDeptId: {billing}
    project:
        name: {name}
        managed: True
        deletionProtect: True
        folderId: {folderid}
        billingAccount: 00C36A-CD0BDB-E543D0
        labels:
            billing-dept-id: {billing}
            project-manager: {manager}
            devops-lead: {lead}
            environment-type: {env}
            line-of-business: {lob}
            project-requestor: {requestor}
    serviceAPIs: 
        cloudresourcemanager.googleapis.com:
        cloudasset.googleapis.com:
    """.format(
        billing=data.get("billing-dept-id"),
        name=data.get("name"),
        folderid=folder_id,
        manager=data.get("project-manager"),
        lead=data.get("devops-lead"),
        env=data.get("environment-type"),
        lob=data.get("line-of-business"),
        requestor=data.get("project-requestor"),
    )
    with open("project.yml", "w+") as file:
        yaml_data = ruamel.yaml.load(project_string, ruamel.yaml.RoundTripLoader)
        yaml_data = ruamel.yaml.dump(yaml_data, Dumper=ruamel.yaml.RoundTripDumper)
        file.write("---\n")
        file.write(yaml_data)


def network(data):
    """ Takes the vpc name and creates a template for the network yaml"""
    network_string = f"""
    vpcs:
        {data}:
            routingMode: GLOBAL
            autoCreateSubnets: False
    """
    with open(f"{data}-network.yml", "w+") as file:
        yaml_data = ruamel.yaml.load(network_string, ruamel.yaml.RoundTripLoader)
        yaml_data = ruamel.yaml.dump(yaml_data, Dumper=ruamel.yaml.RoundTripDumper)
        file.write("---\n")
        file.write(yaml_data)


def subnet(data):
    """ Takes the vpc name and creates a template for the subnet yaml"""
    subnet_string = f"""
    vpcs:
        {data}:
            subnets:
    """
    with open(f"{data}-subnetwork-std.yml", "w+") as file:
        yaml_data = ruamel.yaml.load(subnet_string, ruamel.yaml.RoundTripLoader)
        yaml_data = ruamel.yaml.dump(yaml_data, Dumper=ruamel.yaml.RoundTripDumper)
        file.write("---\n")
        file.write(yaml_data)


def firewall(data):
    """ Takes the vpc name and creates a template for the firewall yaml"""
    firewall_string = f"""
    vpcs:
        {data}:
            firewallRules:
    """
    with open(f"{data}-firewall.yml", "w+") as file:
        yaml_data = ruamel.yaml.load(firewall_string, ruamel.yaml.RoundTripLoader)
        yaml_data = ruamel.yaml.dump(yaml_data, Dumper=ruamel.yaml.RoundTripDumper)
        file.write("---\n")
        file.write(yaml_data)


def connect_gcp(data):
    """ Takes the vpc name and creates a template for the connect gcp yaml"""
    connect_gcp_string = f"""
    vpcs: 
        {data}: 
            routerDef: 
                {data}-c1-gcp-rtr01: 
                    region: us-central1
                    description: 
                    routerASN: 
                    advertiseMode: DEFAULT
                    custom_advertised_ip_ranges: 
                        includeSubnetDef: True
                        customIPList:  
                    ha_vpn_gateways_to_transit: 
                        {data}-c1-totransit: 
                            description: 
                            if0_peer_cidr: 
                                status: BLUECAT_ALLOC_BGP_30
                            if1_peer_cidr: 
                                status: BLUECAT_ALLOC_BGP_30
                {data}-e1-gcp-rtr01: 
                    region: us-east1
                    description: 
                    routerASN: 
                    advertiseMode: DEFAULT
                    custom_advertised_ip_ranges: 
                        includeSubnetDef: True
                        customIPList: 
                    ha_vpn_gateways_to_transit: 
                        {data}-e1-totransit: 
                            description: 
                            if0_peer_cidr: 
                                status: BLUECAT_ALLOC_BGP_30
                            if1_peer_cidr: 
                                status: BLUECAT_ALLOC_BGP_30
    """
    with open(f"{data}-connect-gcp.yml", "w+") as file:
        yaml_data = ruamel.yaml.load(connect_gcp_string, ruamel.yaml.RoundTripLoader)
        yaml_data = ruamel.yaml.dump(yaml_data, Dumper=ruamel.yaml.RoundTripDumper)
        file.write("---\n")
        file.write(yaml_data)


def connect_onprem(data, data1, data2, **kwargs):
    """ Takes the vpc name and creates a template for the connect onprem yaml"""
    connect_onprem_string_lle = f"""
    vpcs: 
        {data}: 
            interconnectRouterDef: 
                {data}-c1-pi-rtr01: 
                    region: us-central1
                    description:
                    advertiseMode: DEFAULT
                    custom_advertised_ip_ranges:
                        includeSubnetDef: True
                        customIPList:
                    partnerInterconnect:
                        description:
                        availabilityDomain: {kwargs.get('central')}
                        connectionSpeed: {data1}MB
                {data}-e1-pi-rtr01:
                    region: us-east1
                    description:
                    advertiseMode: DEFAULT
                    custom_advertised_ip_ranges:
                        includeSubnetDef: True
                        customIPList:
                    partnerInterconnect:
                        description:
                        availabilityDomain: {kwargs.get('east')}
                        connectionSpeed: {data1}MB
    """
    connect_onprem_string_prd = f"""
    vpcs: 
        {data}: 
            interconnectRouterDef: 
                {data}-c1-pi-rtr01: 
                    region: us-central1
                    description:
                    advertiseMode: DEFAULT
                    custom_advertised_ip_ranges:
                        includeSubnetDef: True
                        customIPList:
                    partnerInterconnect:
                        description:
                        availabilityDomain: 1
                        connectionSpeed: {data1}MB
                {data}-e1-pi-rtr01:
                    region: us-east1
                    description:
                    advertiseMode: DEFAULT
                    custom_advertised_ip_ranges:
                        includeSubnetDef: True
                        customIPList:
                    partnerInterconnect:
                        description:
                        availabilityDomain: 1
                        connectionSpeed: {data1}MB
                {data}-e1-pi-rtr02:
                    region: us-east1
                    description:
                    advertiseMode: DEFAULT
                    custom_advertised_ip_ranges:
                        includeSubnetDef: True
                        customIPList:
                    partnerInterconnect:
                        description:
                        availabilityDomain: 2
                        connectionSpeed: {data1}MB
    """

    # THIS CODE WAS REMOVED FROM THE ABOVE TEMPLATE DUE TO A BUG
    #                     {data}-c1-pi-rtr02:
    #                     region: us-central1
    #                     description:
    #                     advertiseMode: DEFAULT
    #                     custom_advertised_ip_ranges:
    #                         includeSubnetDef: True
    #                         customIPList:
    #                     partnerInterconnect:
    #                         description:
    #                         availabilityDomain: 2
    #                         connectionSpeed: {data1}MB

    with open(f"{data}-connect-onprem.yml", "w+") as file:
        if data2 == "prd":
            yaml_data = ruamel.yaml.load(
                connect_onprem_string_prd, ruamel.yaml.RoundTripLoader
            )
            yaml_data = ruamel.yaml.dump(yaml_data, Dumper=ruamel.yaml.RoundTripDumper)
            file.write("---\n")
            file.write(yaml_data)
        else:
            yaml_data = ruamel.yaml.load(
                connect_onprem_string_lle, ruamel.yaml.RoundTripLoader
            )
            yaml_data = ruamel.yaml.dump(yaml_data, Dumper=ruamel.yaml.RoundTripDumper)
            file.write("---\n")
            file.write(yaml_data)


def router_asn(data, data1):
    """ Takes the vpc name and creates a template for the network yaml"""
    # Read all the lines in the default router file
    with open("default-router-asn.yml", "r") as file:
        lines = file.readlines()

    # Delete the router asn file
    os.remove("default-router-asn.yml")

    # Create a list of comment lines
    comments, existing = [], []
    for line in lines:
        if "#" in line:
            comments.append(line)
        elif "---" not in line and line:
            existing.append(line)

    # Get last ASN number used
    asn = re.search(r"\d{4,}", comments[-1]).group()
    asn1 = int(asn) + 1
    asn2 = asn1 + 1

    with open("default-router-asn.yml", "a+") as file:
        file.write("---\n")
        for item in comments:
            file.write(item)
        file.write(f"# {asn1}: {data}-c1-gcp-rtr01\n")
        file.write(f"# {asn2}: {data}-e1-gcp-rtr01\n")
        for item in existing:
            file.write(item)
        file.write(f"  {data1}:\n")
        file.write(f"    {data}-c1-gcp-rtr01: {asn1}\n")
        file.write(f"    {data}-e1-gcp-rtr01: {asn2}\n")


def equinix_vlan(data, data1, **kwargs):
    """ Takes the vpc name and connection speed and creates a template for the network yaml """
    # Read all the lines in the default vlan file
    with open("default-equinix-vlan.yml", "r") as file:
        lines = file.readlines()

    # Delete the previous file
    os.remove("default-equinix-vlan.yml")

    # Separate data
    comments, info = [], """"""
    for line in lines:
        if "#" in line:
            comments.append(line)
        elif "---" not in line and line:
            info = info + "\n" + line

    # Turn vlan data into a dict
    dict_data = yaml.safe_load(info)

    # Find next VLANs to use
    central, east = 0, 0
    for zone in dict_data["interconnectVlans"]["central"].values():
        for value in zone.values():
            if value > central:
                central = value
    for zone in dict_data["interconnectVlans"]["east"].values():
        for value in zone.values():
            if value > east:
                east = value

    # Create new zone router objects
    if data1 == "prd":
        dict_data["interconnectVlans"]["central"]["zone1"][data + "-c1-pi-rtr01"] = (
            central + 1
        )
        # THIS CODE WAS REMOVED DUE TO A BUG, THIS WILL BE PUT BACK IN IN THE FUTURE
        # dict_data["interconnectVlans"]["central"]["zone2"][data + "-c1-pi-rtr02"] = (
        #     central + 2
        # )
        dict_data["interconnectVlans"]["east"]["zone1"][data + "-e1-pi-rtr01"] = (
            east + 1
        )
        dict_data["interconnectVlans"]["east"]["zone2"][data + "-e1-pi-rtr02"] = (
            east + 2
        )

    else:
        dict_data["interconnectVlans"]["central"]["zone" + kwargs.get("central")][
            data + "-c1-pi-rtr01"
        ] = (central + 1)
        dict_data["interconnectVlans"]["east"]["zone" + kwargs.get("east")][
            data + "-e1-pi-rtr01"
        ] = (east + 1)

    with open("default-equinix-vlan.yml", "a+") as file:
        file.write("---\n")
        for item in comments:
            file.write(item)
        file.write("\n")
        file.write(yaml.dump(dict_data, sort_keys=False))


def eunomia(path, data):
    """ Update the eunomia variables file """
    eunomia_path = path + "/eunomia_vars/doms-cpe-kcc-prd-01/vars"
    os.chdir(eunomia_path)
    with open("projects.yml", "a+") as file:
        file.write("- name: " + data.get("name") + "\n")
        file.write("  gitRef: master\n")


def default(path, data, **kwargs):
    """ Update the default variable files """
    default_var_path = path + "/default_vars"
    os.chdir(default_var_path)
    router_asn(data.get("vpcname"), data.get("name"))
    if data.get("environment-type") == "lle" or data.get("environment-type") == "hle":
        equinix_vlan(
            data.get("vpcname"),
            data.get("environment-type"),
            central=kwargs.get("lle1"),
            east=kwargs.get("lle2"),
        )
    elif data.get("environment-type") == "prd":
        equinix_vlan(data.get("vpcname"), data.get("environment-type"))
    else:
        print("An invalid environment type was supplied.")


def main():
    """ The main method which mainly handles folder navigation """
    # Open the file and get the project data
    with open("create_project_data.yml") as file:
        data = yaml.safe_load(file)
    for value in data.values():
        if value is None:
            sys.exit("Error --> A required value is missing.")
    # Create project folder
    try:
        os.chdir("../../gcp-config")
    except FileNotFoundError:
        print(
            """gcp-config folder navigation failed. Verify the Templates and
                Config repo are in the same upstream folder."""
        )
    # Create random numbers for lle env
    if data.get("environment-type") == "lle" or data.get("environment-type") == "hle":
        # lle1 = str(random.choice([1, 2]))
        # THIS CODE WAS REMOVED DUE TO A BUG, THIS WILL BE PUT BACK IN IN THE FUTURE
        lle1 = str(1)
        lle2 = str(random.choice([1, 2]))
    path = os.getcwd()
    project_path = os.getcwd() + "/project_vars"
    directory = data.get("name")
    directory_path = os.path.join(project_path, directory)
    try:
        os.mkdir(directory_path)
    except OSError:
        print(f"Could not create new folder.")
    else:
        print(f"Successfully created new project folder")
    # Navigate into created folder
    os.chdir(directory_path)
    # Create hierarchy file
    with open("hierarchy.lst", "w+") as file:
        file.write("../../default_vars\n")
        file.write("./\n")
    # Create project files
    project(data)
    network(data.get("vpcname"))
    subnet(data.get("vpcname"))
    firewall(data.get("vpcname"))
    connect_gcp(data.get("vpcname"))
    if "connection-speed" in data.keys():
        conspeed = data.get("connection-speed")
    else:
        conspeed = 50
    if data.get("environment-type") == "lle" or data.get("environment-type") == "hle":
        connect_onprem(
            data.get("vpcname"),
            conspeed,
            data.get("environment-type"),
            central=lle1,
            east=lle2,
        )
    else:
        connect_onprem(
            data.get("vpcname"),
            conspeed,
            data.get("environment-type"),
        )
    # Modify Euonima configuration file
    eunomia(path, data)
    # Modify default var files
    if data.get("environment-type") == "lle" or data.get("environment-type") == "hle":
        default(path, data, lle1=lle1, lle2=lle2)
    else:
        default(path, data)


if __name__ == "__main__":
    main()
