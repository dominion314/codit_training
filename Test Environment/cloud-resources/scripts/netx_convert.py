#!/usr/bin/env python3
#pylint: disable=invalid-name,missing-module-docstring
import argparse
import os
import sys
import yaml #pylint: disable=import-error

try:
    from pprint import pprint
    from googleapiclient import discovery
    from oauth2client.client import GoogleCredentials
except ImportError as e:
    print("Failed to import.\n{}".format(e))
    sys.exit(1)

# Script to parse the Google API
# Gather a VPC's subnetwork and Firewall information and rewrite the information
# to YAML formats for Kohl's GitOps.

def gatherEnvType(projectOrVpc: str) -> str:
    """ Parse out any known environment types from the given string. """
    envronTypes = ['-prd', '-lle', '-hle', '-ops', '-sbx']
    for env in envronTypes:
        if projectOrVpc.find(env) != -1:
            return env.replace('-', '')
    return 'ops'

# Given a GCP discovery service, parse all subnetworks for
# a given project, vpc, and region.
# Append to existing result structure if given, otherwise
# create a new one.
def gatherNetworks(service: dict,
                   project: str,
                   vpc: str,
                   regions: list = None,
                   result: dict = None) -> dict:
    """ Given a GCP discovery service, parse all subnetworks for
        a given project, vpc, and region.
        Append to existing result structure if given, otherwise
        create a new one.
    """
    # Init variables if empty
    if regions is None:
        regions = []
    if result is None:
        regions = {}

    for region in regions:
        # Gather Subnet list for region
        requestSubList = service.subnetworks().list(
            project=project, region=region)

        while requestSubList is not None:
            response = requestSubList.execute()
            # Process each subnet
            for network in response['items']:
                vpcItem = network['network'].rsplit('/', 1)[-1]
                if vpc is not None and vpc != vpcItem:
                    continue
                # for subnet element, gather IAM bindings
                requestIAM = service.subnetworks().getIamPolicy(
                    project=project, region=region, resource=network['id'])
                responseIAM = requestIAM.execute()

                # Update result dict with information about subnet
                # If VPC not found, create it with network element and IAM
                if vpcItem not in result.keys():
                    result.update({vpcItem: {'subnetwork': {network['name']: network}}})
                    result[vpcItem]['subnetwork'][network['name']].update({'iam': responseIAM})

                # If VPC is found, update existing VPC key, but add subnetwork key if not found.
                else:
                    if 'subnetwork' not in result[vpcItem].keys():
                        result[vpcItem].update(
                            {'subnetwork': {network['name']: network}})
                    else:
                        result[vpcItem]['subnetwork'].update({network['name']: network})

                    result[vpcItem]['subnetwork'][network['name']].update(
                        {'iam': responseIAM})

            requestSubList = service.subnetworks().list_next(
                previous_request=requestSubList, previous_response=response)
    return result

def gatherFirewall(service: dict, project: str, vpc: str, result: dict = None) -> dict:
    """ Given a GCP discovery service, parse all firewall rules for
    a given project, and vpc.
    Append to existing result structure if given, otherwise
    create a new one.
    """
    # Init result if none imported
    if result is None:
        result = {}

    # Gather Firewall Rule Names
    requestFirewallList = service.firewalls().list(
        project=project)

    while requestFirewallList is not None:
        response = requestFirewallList.execute()
        # Process Each Firewall Rule
        for firewall in response['items']:
            vpcItem = firewall['network'].rsplit('/', 1)[-1]
            if vpc is not None and vpc != vpcItem:
                continue

            # Update result dict with information about firewall rule
            # If VPC not found, create it with Firewall Rule
            if vpcItem not in result.keys():
                result[vpcItem] = {'firewall': {firewall['name']: firewall}}

            # If VPC is found, update existing VPC key but add firewall key if not found.
            else:
                if 'firewall' not in result[vpcItem].keys():
                    result[vpcItem].update(
                        {'firewall': {firewall['name']: firewall}})
                else:
                    result[vpcItem]['firewall'].update({firewall['name']: firewall})

            # Final structure does not use IPProtocol as a dict key.  Convert Port
            # portion of the structure to use 'protocol' instead of 'IPProtocol'
            if result[vpcItem]['firewall'][firewall['name']].get('allowed') is not None:
                for ports in result[vpcItem]['firewall'][firewall['name']].get('allowed'):
                    ports['protocol'] = ports.pop('IPProtocol')
            if result[vpcItem]['firewall'][firewall['name']].get('denied') is not None:
                for ports in result[vpcItem]['firewall'][firewall['name']].get('denied'):
                    ports['protocol'] = ports.pop('IPProtocol')

        requestFirewallList = service.subnetworks().list_next(
            previous_request=requestFirewallList, previous_response=response)

    return result

def exportToFile(data: dict, fileName: str, folderName: str = None):
    """ export Dict Structure to YAML document """
    if folderName is None:
        folderName = ''
    filePath = "./{}/{}".format(folderName, fileName)
    folderPath = "./{}".format(folderName)

    os.makedirs(folderPath, exist_ok=True)

    with open(filePath, 'w') as fileexport:
        documents = yaml.dump(data, fileexport)

    return documents


def writeGitOpsFile(data: dict, vpc: str, destination: str = None) -> None:
    """ Take the structured data pulled from GCP discovery and rewrite it
        in Kohl's GCP GitOps formatted YAML files
        """
    if destination is None:
        destination = ''
    # Init the dictionaries
    subnet_results = {'vpcs': {vpc: {'subnets':{}}}}
    firewall_results = {'vpcs': {vpc: {'firewallRules':{}}}}
#   Unknown IAM structure for subnetwork permissions
#   iam_results = {}

    for vpc_name, vpc_data in data.items():
        if vpc_data.get('subnetwork') is not None:
            for subnet_name, subnet_data in vpc_data.get('subnetwork').items():
                new_name = subnet_name.replace(vpc_name + '-', 'convert-').\
                    replace('doms-', 'convert-')
                subn_size = subnet_data['ipCidrRange'].rsplit('/', 1)[-1]
                subn_region = subnet_data['region'].rsplit('/', 1)[-1]
# Add logic for secondary Ranges
# Add logic for GKE
                subnet_results['vpcs'][vpc]['subnets'].update({new_name: {
                    'advertiseRoutes': True,
                    'region': subn_region,
                    'network': {'state': bluecatCode('gcp',
                                                     subn_region,
                                                     subn_size,
                                                     gatherEnvType(vpc_name))}
                }})

        if vpc_data.get('firewall') is not None:
            for firewall_name, firewall_data in vpc_data.get('firewall').items():
                if 'dflt' in firewall_name:
                    continue
                firewall_results['vpcs'][vpc]['firewallRules'].update({firewall_name: {
                    'priority': firewall_data.get('priority'),
                    'direction': firewall_data.get('direction'),
                    'description': firewall_data.get('description'),
                    'disabled': firewall_data.get('disabled'),
                    'logging': False,
                    'rule': {
                        'destinationRanges': firewall_data.get('destinationRanges')
                                             if firewall_data.get('destinationRanges') is not None
                                             else[],
                        'sourceRanges': firewall_data.get('sourceRanges')
                                        if firewall_data.get('sourceRanges') is not None
                                        else [],
                        'targetTags': firewall_data.get('targetTags')
                                      if firewall_data.get('targetTags') is not None
                                      else [],
                        'sourceTags': firewall_data.get('sourceTags')
                                      if firewall_data.get('sourceTags') is not None
                                      else [],
                        'targetServiceAccounts': firewall_data.get('targetServiceAccounts')
                                                 if firewall_data.get('targetServiceAccounts')
                                                 is not None
                                                 else [],
                        'sourceServiceAccounts': firewall_data.get('sourceServiceAccounts')
                                                 if firewall_data.get('sourceServiceAccounts')
                                                 is not None
                                                 else [],
                        'allow': firewall_data.get('allowed')
                                 if firewall_data.get('allowed') is not None
                                 else [],
                        'deny': firewall_data.get('denied')
                                if firewall_data.get('denied') is not None
                                else []
                    }
                }})

    exportToFile(subnet_results,
                 "{}-subnetwork-import.yml".format(vpc), destination)
    exportToFile(firewall_results,
                 "{}-firewall-import.yml".format(vpc), destination)

def bluecatCode(subnetType, region, size, envType) -> str:
    """ Return the appropriate Bluecat Code to be injected to gitops parameters """
    regionCode = ''
    if subnetType == 'gcp':
        if envType == 'prd':
            if 'central' in region:
                regionCode = 'CPRD'
            else:
                regionCode = 'EPRD'
        elif envType in ('hle', 'lle'):
            if 'central' in region:
                regionCode = 'CNPD'
            else:
                regionCode = 'ENPD'
        else:
            if 'central' in region:
                regionCode = 'CTEST'
            else:
                regionCode = 'ETEST'
    # Implement Other Subnet Types

    return 'BLUECAT_ALLOC_{}_{}_{}'.format(subnetType.upper(), regionCode, str(size))

def main(project, target_vpc, source_vpc, debugFile, debugScreen) -> None:
    """ main function. Login to GCP discovery """
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    projectDetail = gatherNetworks(
        service,
        project,
        source_vpc,
        ["us-central1", "us-east1"],
        gatherFirewall(service, project, source_vpc)
        )
    if debugScreen:
        pprint(projectDetail)
    if debugFile:
        exportToFile(projectDetail, project+'.yml', project)

    writeGitOpsFile(projectDetail, target_vpc, project)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('target_vpc', help='This is the NetX VPC.')
    parser.add_argument(
        '--source_vpc',
        default=None,
        help='Pick a single Legacy VPC to process.  No Input will process all VPCs')
    parser.add_argument(
        '--debugFile',
        action='store_true',
        help='Export Parsed File.'
    )
    parser.add_argument(
        '--debugScreen',
        action='store_true',
        help='Display variables to screen'
    )

    args = parser.parse_args()

    main(args.project_id, args.target_vpc, args.source_vpc, args.debugFile, args.debugScreen)
