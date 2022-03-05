#!/usr/bin/env python3
#pylint: skip-file
""" Script to run cerberus schema validation of input var files listed in
manifest. Requires predefined schema files.
"""

import argparse
import os
import sys
import yaml
import cerberus

EXIT_SUCCESS = 0
EXIT_FAIL = 1

def get_arguments():
    """ Gets arguments from command line.

    :return: populated arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',
                        help='Path to processed values folder')
    parser.add_argument('--schema_file',
                        help='Path to schema template yaml file')
    parser.add_argument('--report_file', action='store',
                        dest='report_file', help='Report file')
    parser.add_argument('--schema_config', action='store', dest='schema_config',
                        help='Config file for Schema validation')

    return parser.parse_args()

def check_against_schema(validator, yml_file, schema_file, report):
    """
    Validates yaml content presented in yml_file against cerberus schema presented
    in schema_file.

    :return: True if given input satisfies schema, False otherwise.
    """
    proj_temp = yml_file.split('/')
    proj_name = proj_temp[len(proj_temp)-2]
    report.write("-----------------------------------------------------------\n")
    report.write("Validating Schema for Project: {} \n".format(proj_name))

    with open(yml_file) as file:
        yml_input = yaml.load(file.read(), Loader=yaml.SafeLoader)
    with open(schema_file) as file:
        schema = yaml.load(file.read(), Loader=yaml.SafeLoader)

    try:
        if validator.validate(yml_input, schema):
            report.write("PASSED\n")
            report.write("-----------------------------------------------------------\n")
            return True

        report.write("Validation error:\n")

        ERR = validator.errors

        for key in ERR.keys():
            path = key
            if len(ERR[key]) > 1:
                report.write("{}:\n    ERROR-> {}\n".format(path,ERR[key][0]))
                recurKey(ERR[key][1], path, report)
            else:
                recurKey(ERR[key][0], path, report)
            report.write("--------\n")

        report.write("FAILED\n")
        report.write("-----------------------------------------------------------\n")
        return False
    except (IndexError, AttributeError) as FormatError:
        report.write("Issue with Format, Basic Validation Error:\n")
        report.write(yaml.dump(ERR, allow_unicode=True))
        report.write("\nFAILED\n")
        report.write("-----------------------------------------------------------\n")
        return False
    except cerberus.schema.SchemaError as error:
        report.write("Error in schema file {}: {}\n".format(schema_file, str(error)))
        return False

def recurKey(listOrDict, path, report): 
    for k,v in listOrDict.items():
        if isinstance(v[0], str):
            if len(v) > 1 and isinstance(v[1], str):
                report.write("{}.{}:\n    ERROR-> {}\n".format(path,k,v))
            else:
                report.write("{}.{}:\n    ERROR-> {}\n".format(path,k,v[0]))
                if len(v) > 1:
                    recurKey(v[1], "{}.{}".format(path,k), report)
        elif isinstance(v[0], dict):
            for k2,v2 in v[0].items():
                if isinstance(v2[0], dict):
                    recurKey(v2[0], "{}.{}.{}".format(path,k,k2), report)
                else:
                    if len(v2) > 1 and isinstance(v2[1], str):
                        report.write("{}.{}.{}:\n    ERROR-> {}\n".format(path,k,k2,v2))
                    else:
                        report.write("{}.{}.{}:\n    ERROR-> {}\n".format(path,k,k2,v2[0]))
                        if len(v2) > 1:
                            recurKey(v2[1], path+"."+k+"."+k2, report)

def main():
    """
    The script opens given manifest file and runs validation against each
    (input_yml_file, shchema_file) pair specified in it.
    """
    args = get_arguments()
    schema_file = args.schema_file
    report_f = open(args.report_file, 'a+')
    with open(args.schema_config) as f_in:
        schema_config = yaml.load(f_in, Loader=yaml.SafeLoader) #Unique
    project_paths = []
    project_list = []
    for project in os.scandir(args.input): #Unique
        if project.is_dir():
            project_list.append(project.path.split('/')[-1:])
            project_paths.append(project.path + '/processed_values.yml')

    if schema_config['enabled']:
        vld = cerberus.Validator()
        vld.allow_unknown = True

        report_f.write("Start of Schema Validation\n")

        checks = set()
        for proj in project_paths:
            checks.add(check_against_schema(vld, proj, schema_file, report_f))

        report_f.write("End of Schema Validation \n")

        if all(checks):
            sys.exit(EXIT_SUCCESS)
        else:
            sys.exit(EXIT_FAIL)
    else:
        report_f.write("Schema Validation is Turned Off\n")
        sys.exit(EXIT_SUCCESS)

if __name__ == "__main__":
    main()
