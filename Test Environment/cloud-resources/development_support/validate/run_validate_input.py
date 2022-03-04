#pylint: disable=import-error,R1732
"""
Validation executor
"""
__version__ = 0.1
__author__ = "Pavel Leonovitch"
__copyright__ = "Copyright 2020, Kohls"

import argparse
import sys
import pprint
import os
from subprocess import Popen, PIPE
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound, TemplateSyntaxError #pylint: disable=import-error
import cerberus



def main(): # pylint: disable=R0914,R0912
    """
    Entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", "-im", help="input manifest file")
    args = parser.parse_args()
    if not args.input_manifest:
        sys.exit(1)

    # process validation manifest
    in_data = dict()
    with open(args.input_manifest) as file:
        try:
            in_data = yaml.load(file, Loader=yaml.FullLoader)
        except yaml.YAMLError as error:
            print(error)
            sys.exit(2)

    # go through list of input var files that need to be merged
    invalid_yaml_content = False
    var_files = list()
    for item in in_data['inputVars']:
        var_file = item['fileName']
        if 'schema' in item:
            schema_file = item['schema']
            result = yml_valid(var_file, schema_file)
            if result:
                var_files.append(item['fileName'])
            else:
                invalid_yaml_content = True
        else:
            var_files.append(item['fileName'])
    if invalid_yaml_content:
        print("Schema validation of yaml input vars failed")
        sys.exit(4)

    # prepare and execute yq 'merge' command
    command_list = ['/usr/local/bin/yq', 'm']
    command_list.extend(var_files)
    process = Popen(command_list, stdout=PIPE, stderr=PIPE)
    input_yml, err = process.communicate()
    if process.returncode != 0:
        print(err)
        sys.exit(3)

    #store yaml in artifacts
    with open(in_data['artifacts']['combined_var_yaml_file'], 'wb') as out:
        out.write(input_yml)
    input_yml_dict = yaml.load(input_yml)

    # render config connector templates
    render_errors = False
    with open(in_data['artifacts']['kcc_yaml_file'], "w+") as kcc_file:
        for item in in_data['kccJinjaTemplates']:
            out = render_template(template=item['fileName'], data=input_yml_dict)
            if out is None:
                render_errors = True
            else:
                kcc_file.write(out)
    if render_errors:
        print("There were some template rendering issues")
        sys.exit(4)


def yml_valid(yml_file, schema_file):
    """
    Validates yaml content presented in yml_file against cerberus schema presented
    in shema_file
    """

    with open(yml_file) as in_yml:
        content = yaml.load(in_yml.read(), Loader=yaml.SafeLoader)
    with open(schema_file) as in_schema:
        schema = yaml.load(in_schema.read(), Loader=yaml.SafeLoader)

    validator = cerberus.Validator()
    #v.allow_unknown = True
    try:
        if validator.validate(content, schema):
            pass
        else:
            print("Validation error for "+yml_file)
            pprint.pprint(validator.errors)
            return False
        return True
    except cerberus.schema.SchemaError as error:
        print("Error in schema file " + schema_file + str(error))
        return False


def render_template(template, data):
    """
    renderes template with data, returns rendered content back
    or None if error
    """
    t_file = os.path.basename(template)
    t_folder = os.path.dirname(template)
    try:
        env = Environment(loader=FileSystemLoader(t_folder))
        template = env.get_template(t_file)
        out = template.render(data)
        return out
    except TemplateNotFound:
        print("Unable to load template {}".format(template))
    except TemplateSyntaxError as e_bad_template:
        print("Error in template {}: {}".format(template, str(e_bad_template)))

    except BaseException as e_default: # pylint: disable=broad-except
        print("Failed to render template: {}".format(str(e_default)))
    return None

if __name__ == "__main__":
    main()
