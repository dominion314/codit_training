#!/usr/bin/env python3
""" Script to run cerberus schema validation of input var files listed in
manifest. Requires predefined schema files.
"""

import argparse
import os
import sys
import json
import re
import yaml
import cerberus

EXIT_SUCCESS = 0
EXIT_FAIL = 1

def get_arguments():
    """ Gets arguments from command line.

    :return: populated arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest_file',
                        help='Path to json file with input_file<->schema '
                             'mapping.')
    parser.add_argument('--schemas_directory',
                        help='Path to directory with schemas.')

    return parser.parse_args()

def check_against_schema(validator, yml_file, schema_file):
    """
    Validates yaml content presented in yml_file against cerberus schema presented
    in schema_file.

    :return: True if given input satisfies schema, False otherwise.
    """

    print("\nValidating config input {} against {} schema".format(yml_file, schema_file))

    with open(yml_file) as file:
        yml_input = yaml.load(file.read(), Loader=yaml.SafeLoader)
    with open(schema_file) as file:
        schema = yaml.load(file.read(), Loader=yaml.SafeLoader)

    try:
        if validator.validate(yml_input, schema):
            print("PASSED")
            return True
        print("Validation error: \n{} \nFAILED".format(validator.errors))
        return False
    except cerberus.schema.SchemaError as error:
        print("Error in schema file {}: {}".format(schema_file, str(error)))
        return False

def main():
    """
    The script opens given manifest file and runs validation against each
    (input_yml_file, shchema_file) pair specified in it.
    """
    args = get_arguments()
    manifest_directory = re.sub('/[^/]*$', '', args.manifest_file)

    vld = cerberus.Validator()
    vld.allow_unknown = True

    checks = set()
    with open(args.manifest_file) as file:
        manifest = json.load(file)
        for item in manifest['items']:
            yml_file = os.path.join(manifest_directory, item['input_yml_file'])
            schema_file = os.path.join(args.schemas_directory, item['schema_file'])
            checks.add(check_against_schema(vld, yml_file, schema_file))
    if all(checks):
        sys.exit(EXIT_SUCCESS)
    else:
        sys.exit(EXIT_FAIL)

if __name__ == "__main__":
    main()
