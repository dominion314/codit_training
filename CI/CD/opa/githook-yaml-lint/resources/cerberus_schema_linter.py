#!/usr/bin/env python3
# pylint: disable=W0703
"""
This is script that performs evaluation and validation of YAML content in
specified folder and sub-directories. Only files with extention yml or yaml
are being checked.
Content must pass all of the following checks:
 - must be valid YAML document
 - must be valid Cerberus schema (https://docs.python-cerberus.org/en/stable/)
"""
from __future__ import print_function
import sys
import os
import cerberus
import yaml

def main():
    """
    Main entry point
    """

    # check if parameter is passed
    if len(sys.argv) != 2:
        print('Incorrect invocation: "{} <schema_folder>"'.format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)

    schema_folder = sys.argv[1]
    if not os.path.isdir(schema_folder):
        print('Incorrect parameter: {} must be directory'.format(schema_folder),
              file=sys.stderr)
        sys.exit(1)

    # run validation
    is_failed, processing, errors = validate(schema_folder)

    # print processing results
    for item in processing:
        print(item)

    if is_failed is True:
        print("*** VALIDATION FAILED ***", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)
    else:
        print("*** VALIDATION SUCCESSFUL ***")

def validate(folder):
    """
    Validates that file content in folder and sub-folders to be valid cerberus schemas
    Content is expected to be in yml format
    Only files with .yml or .yaml extensions are checked
    """
    errors = list()
    processing = list()
    is_failed = False
    for root, _dirs, files in  os.walk(folder, topdown=True):
        for name in files:
            if name.upper().endswith('.YML') or name.upper().endswith('.YAML'):
                fpath = os.path.join(root, name)
                processing.append("Validating {}".format(fpath))
                try:
                    with open(fpath) as f_in:
                        in_data = yaml.load(f_in, Loader=yaml.FullLoader)
                        try:
                            _v = cerberus.Validator(in_data)
                        except cerberus.SchemaError as schema_error:
                            is_failed = True
                            message = ">>>>>> {} is INVALID Cerberus schema: {}"\
                                .format(fpath, schema_error)
                            errors.append(message)
                except yaml.YAMLError as error:
                    is_failed = True
                    message = ">>>>>> {}: INVALID YAML: {}".format(fpath, error)
                    errors.append(message)
                except BaseException as error:
                    is_failed = True
                    message = ">>>>>> {}: General problem with handling YAML: {}"\
                        .format(fpath, error)
                    errors.append(message)

    return is_failed, processing, errors
if __name__ == "__main__":
    main()
