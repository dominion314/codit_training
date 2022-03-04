#pylint: skip-file
import yaml
import sys
import logging
from yaml.parser import ParserError
import click

@click.command()
@click.argument('filename')
@click.option('--check-asn/--no-check-asn', default=True)
@click.option('--check-vlan/--no-check-vlan', default=True)
@click.pass_obj
def check(ctx_obj, filename, check_asn, check_vlan):
    ''' Main function '''
    success = True
    
    #Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./integrity_check.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # Import YAML formatted file for input
    project_input, success = readFile(filename)

    if check_asn:
    # ASN check
        success = asnCheck(project_input)
    
    if check_vlan:
    # VLAN check
        success = vlanCheck(project_input)

    if not success:
        sys.exit(1)

def vlanCheck(data) -> bool:
    """
    Check the yaml dict for duplicate vlans using a set

    Input:
        data - the yaml dict that is being checked
    Output:
        True - if no vlans are duplicated
        False - if there are matches
                Will also print the name and port of the vlan that was duplicated
    """
    logging.debug("Init VLAN Check on Data")
    vlanCheckingSet = set()
    # traverse the yaml and check if a duplicate is added
    if data.get("interconnectVlans"):
        for region in data["interconnectVlans"].values():
            for zone in region.values():
                for vlan, port in zone.items():
                    # check for duplicates with a length check
                    length = len(vlanCheckingSet)
                    vlanCheckingSet.add(port)
                    if length + 1 != len(vlanCheckingSet):
                        logging.error("Found Duplicate VLAN: {} {}".format(vlan, str(port)))
                        logging.error("VLAN Check has FAILED")
                        return False
        logging.info("VLAN Check has Passed")

    return True

def asnCheck(data) -> bool:
    """
    Check the yaml dict for duplicate asns using a set
    Input:
        data - the yaml dict that is being checked
    Output:
        True - if no duplicates are found
        False - if a duplicate is found, done using a set. Will also print
                the name and value of the asn that was found to be duplicated
    """

    asnCheckingSet = set()
    logging.debug("Init ASN Check on Data")
    if data.get("ha_vpn_to_global_transit_asn"):
        for group in data["ha_vpn_to_global_transit_asn"].values():
            for asnName, asnValue in group.items():
                # use a length check to see if the item is a duplicate
                length = len(asnCheckingSet)
                asnCheckingSet.add(asnValue)

                if length + 1 != len(asnCheckingSet):
                    logging.error("Duplicate ASN Found: {} {}".format(asnName, str(asnValue)))
                    logging.error("ASN Check has FAILED")
                    return False
        logging.info("ASN Check has Passed")

    return True



def readFile(inFile) -> tuple:
    '''read and import file specified in args'''
    try:
        with open(inFile, 'r') as file:
            return (yaml.load(file.read(), Loader=yaml.Loader), True)
    except FileNotFoundError:
        logging.error("Error with input file: Not Found!")
        sys.exit(1)
    except ParserError as exc:
        logging.error("Problem Parsing YAML")
        logging.error(exc.problem)
        logging.error(exc.context_mark)
        sys.exit(1)
    except yaml.YAMLError as exc:
        logging.error("Unknown YAML error")
        logging.error(exc.args)
        sys.exit(1)

    # if earlier return isn't complete, fail check
    return '', False


if __name__ == "__main__":
    check()
