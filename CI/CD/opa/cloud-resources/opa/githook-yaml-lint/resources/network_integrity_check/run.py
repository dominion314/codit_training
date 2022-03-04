"""
This script will accept formatted YAML files to check
the structure and values for duplicates.
"""
import sys
import yaml
#disable some of pylint parandoid complains
#pylint: disable=C0103,R0801,C0121

def parseYaml(vlanFilename, asnFilename):
    """
    Parses the yaml functions and returns them as dictionaries.

    Input:
        vlanFilename - The filename of the yaml file containing vlans
        asnFilename - The filename of the yaml file containing asns
    Output:
        vlanData - The vlan yaml as a dictionary
        asnData - The asn yaml as a dictionary
    """

    yaml.preserve_quotes = True
    yaml.explicit_start = True

    # load yaml files
    with open(vlanFilename) as in_file:
        vlanData = yaml.load(in_file, Loader=yaml.FullLoader)
    with open(asnFilename) as in_file:
        asnData = yaml.load(in_file, Loader=yaml.FullLoader)

    return vlanData, asnData



def vlanCheck(data):
    """
    Check the yaml dict for duplicate vlans using a set

    Input:
        filename - The name of the yaml file
        data - the yaml dict that is being checked
    Output:
        True - if no vlans are duplicated
        False - if there are matches
                Will also print the name and port of the vlan that was duplicated
    """

    vlanCheckingSet = set()
    # traverse the yaml and check if a duplicate is added
    if "interconnectVlans" in data and data["interconnectVlans"] != None:
        for region in data["interconnectVlans"].values():
            for zone in region.values():
                for vlan, port in zone.items():
                    # check for duplicates with a length check
                    length = len(vlanCheckingSet)
                    vlanCheckingSet.add(port)

                    if length + 1 != len(vlanCheckingSet):
                        print("Duplicate at:", vlan, port)
                        return False
        print("passed the vlan check")

    return True


def asnCheck(data):
    """
    Check the yaml dict for duplicate asns using a set
    Input:
        filename - the name of the file that is being checked
        data - the yaml dict that is being checked
    Output:
        True - if no duplicates are found
        False - if a duplicate is found, done using a set. Will also print
                the name and value of the asn that was found to be duplicated
    """

    asnCheckingSet = set()
    # check asn's
    if "ha_vpn_to_global_transit_asn" in data and data["ha_vpn_to_global_transit_asn"] != None:
        for group in data["ha_vpn_to_global_transit_asn"].values():
            for asnName, asnValue in group.items():
                # use a length check to see if the item is a duplicate
                length = len(asnCheckingSet)
                asnCheckingSet.add(asnValue)

                if length + 1 != len(asnCheckingSet):
                    print("Duplicate at:", asnName, asnValue)
                    return False
        print("passed the asn check")

    return True


def main():
    """
    Accepts the arguments, calls parsing, and makes call to the checks.

    Input:
        sys.argv[1] - The first argument passed must be the vlan filename
        sys.argv[2] - The second argument passed must be the asn filename
    Output:
        exit(0) - If the checks passed
        exit(1) - If the checks failed
    """
    vlanFilename = sys.argv[1]
    asnFilename = sys.argv[2]

    # call the yaml parser on the files that have been passed in
    vlanData, asnData = parseYaml(vlanFilename, asnFilename)

    final = vlanCheck(vlanData) and asnCheck(asnData)
    # exit 0 if tests passed, exit 1 if they failed
    if not final:
        sys.exit(1)

if __name__ == "__main__":
    main()
