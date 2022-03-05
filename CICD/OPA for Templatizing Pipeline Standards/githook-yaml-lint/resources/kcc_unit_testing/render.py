"""
Renderer of unit test materials
"""
#disable pylint related to too many variables, too many branches, too many statements
#pylint: disable=R0914,R0912,R0915

import argparse
import json
import logging
import tempfile
import os
from subprocess import Popen, PIPE
import sys
from shutil import copyfile
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound, TemplateSyntaxError
import ansible_filters_ipaddr
import ansible_filters_regex_search

YQ_BINARY = 'yq'
COMMON_VARS_DIR = '_common_vars'

def  load_kcc_files(definition, kcc_files):
    """
    Loads definition, follows references to KCC tempaltes, populates kcc_files list
    """
    with open(definition) as file_in:
        def_dict = yaml.load(file_in, Loader=yaml.SafeLoader)
        for item in def_dict['kccTemplates']:
            path = os.path.join(os.path.dirname(definition), item)
            kcc_files.append(path)


def load_inspec_files(definition, inspec_files):
    """
    Loads definition, follows references to KCC tempaltes, populates inspec_files list
    """
    with open(definition) as file_in:
        def_dict = yaml.load(file_in, Loader=yaml.SafeLoader)
        for item in def_dict['inspecControls']:
            path = os.path.join(os.path.dirname(definition), item)
            inspec_files.append(path)


def render_data(args, logger):
    """
    Renders input vars and kcc files
    Stages inspec control files in proper place
    """
    # process inject data:
    inject_data = json.loads(args.inject_data_json)
    # process unit tests:
    # yml_files - will contain list of files with yaml content that will need to be
    # merged to produce combined input yml that will 'feed' KCC templates and inspec tests
    yml_files = list()
    temp_files = list()
    kcc_template_files = list()
    inspec_files = list()

    # create yml file with injected data
    _, temp_file = tempfile.mkstemp(suffix='.yml', prefix='inject')
    logger.info("Created file {} to store injected data".format(temp_file))
    with open(temp_file, 'w') as outfile:
        yaml.dump(inject_data, outfile, default_flow_style=False)
    yml_files.append(temp_file)
    temp_files.append(temp_file)

    # now walk through unit tests, render and merge input data for unit tests
    base_dir = args.unit_tests_home
    unit_tests = [x.strip() for x in args.unit_tests.split(',')]
    # check for special case ( all unit cases )
    if unit_tests[0].lower() == 'all':
        unit_tests = list_all_unit_tests(base_dir)
    logger.info("Processing input data for unit tests...")
    for item in unit_tests:
        logger.info(">>>> Unit Test {}".format(item))
        load_kcc_files(os.path.join(base_dir, item, "definition.yml"), kcc_template_files)
        load_inspec_files(os.path.join(base_dir, item, "definition.yml"), inspec_files)
        data_dir = os.path.join(base_dir, item, "data/")
        logger.info("Reading files from folder {}".format(data_dir))

        for file in os.listdir(data_dir):
            logger.info(">>{}".format(file))
            if file.endswith('.j2'):
                logger.info("Performing Jinja rendering for {}".format(file))
                rendered_data = render_template(logger,
                                                os.path.join(base_dir, item, "data/", file),
                                                inject_data)
                _, temp_yml_file = tempfile.mkstemp(suffix='.yml', prefix=item)
                with open(temp_yml_file, 'w') as yml_outfile:
                    yml_outfile.write(rendered_data)
                yml_files.append(temp_yml_file)
                temp_files.append(temp_yml_file)
                logger.info("Storing rendered content in temporarily file {}".format(temp_yml_file))
            else:
                yml_files.append(os.path.join(base_dir, item, "data/", file))

    # add content of _common_vars to yml_files
    common_vars = get_common_vars_files(logger, args.unit_tests_home)
    yml_files.extend(common_vars)

    # exclude possible duplicates
    kcc_template_files = set(kcc_template_files)
    inspec_files = set(inspec_files)

    # perform merge of yaml data
    command_list = [YQ_BINARY, 'm']
    logger.info("Executing yq binary {}".format(command_list[0]))
    #command_list = ['/usr/local/bin/yq', 'm']
    command_list.extend(yml_files)
    pipe = Popen(command_list, stdout=PIPE, stderr=PIPE)
    merged_yml, err = pipe.communicate()
    if pipe.returncode != 0:
        logger.error("YQ merge failed: {}".format(err))
        sys.exit(1)
    logger.info("Performed merge of input yaml")
    # store result
    with open(args.input_var_file, 'wb') as outfile:
        outfile.write(merged_yml)
    logger.info("Stored input yaml in {} file".format(args.input_var_file))

    # load merged yml into dictionary
    # now render KCC templates
    input_yml_dict = yaml.load(merged_yml, Loader=yaml.SafeLoader)
    kcc_render_errors = False
    with open(args.kcc_file, "w+") as kcc_file:
        for item in kcc_template_files:
            logger.info("Rendering KCC template {}".format(item))
            out = render_template(logger=logger, template=item, data=input_yml_dict)
            if out is None:
                kcc_render_errors = True
            else:
                kcc_file.write(out)
    if kcc_render_errors:
        logger.error("There were some template rendering issues")
        sys.exit(1)

    # copy relevant inspec files into proper folder
    # commented out python3 version
    #os.makedirs(args.inspec_controls_folder, exist_ok=True)
    if not os.path.exists(args.inspec_controls_folder):
        os.makedirs(args.inspec_controls_folder)

    for item in inspec_files:
        logger.info("Copying inspec conrol file {} to {}".format(item, args.inspec_controls_folder))
        copyfile(item, os.path.join(args.inspec_controls_folder, os.path.basename(item)))


    # remove temporarily files created
    for item in temp_files:
        logger.info("Removing temp file {}".format(item))
        os.remove(item)

def render_template(logger, template, data):
    """
    renders Jinka tempalte in template file name with data
    """
    t_file = os.path.basename(template)
    t_folder = os.path.dirname(template)
    try:
        env = Environment(loader=FileSystemLoader(t_folder))
        env.filters['regex_search'] = ansible_filters_regex_search.regex_search
        env.filters['ipaddr'] = ansible_filters_ipaddr.ipaddr
        template = env.get_template(t_file)
        out = template.render(data)
        return out
    except TemplateNotFound:
        logger.error("Unable to load template {}".format(template))
    except TemplateSyntaxError as e_bad_template:
        logger.error("Error in template {}: {}".format(template, str(e_bad_template)))
    return None

def list_all_unit_tests(base_dir):
    """
    Returns list of unit tests in base_dir
    """
    result = list()
    files = os.listdir(base_dir)
    for item in files:
        if os.path.isdir(os.path.join(base_dir, item))  and item[0] != '_':
            result.append(item)
    return result

def get_common_vars_files(logger, base_dir):
    """
    Returns list of yml files that contains common vars
    """
    result = list()
    files = os.listdir(os.path.join(base_dir, COMMON_VARS_DIR))
    for item in files:
        if os.path.isfile(os.path.join(base_dir, COMMON_VARS_DIR, item))  and item.endswith('.yml'):
            logger.info("Found common vars file {}".format(item))
            result.append(os.path.join(base_dir, COMMON_VARS_DIR, item))
    return result

def main():
    """
    Main method
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_file', action='store', dest='log_file', help='Log file')
    parser.add_argument('--inject_data', action='store', dest='inject_data_json',
                        help='Injection JSON data')
    parser.add_argument('--unit_tests_home', action='store', dest='unit_tests_home',
                        help='Home directory for unit tests definitions')
    parser.add_argument('--unit_tests', action='store', dest='unit_tests',
                        help='List of unit tests')
    parser.add_argument('--result_input_var_file', action='store', dest='input_var_file',
                        help='Merged input var file')
    parser.add_argument('--result_kcc_file', action='store', dest='kcc_file',
                        help='Merged KCC file')
    parser.add_argument('--result_inspec_controls_home', action='store',
                        dest='inspec_controls_folder',
                        help='Folder that stores inspec control files')
    result = parser.parse_args()

    # initialze logging
    logger = logging.getLogger(__name__)
    logger.propagate = False  #do not log to console
    formatter = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
    try:
        handler = logging.FileHandler(result.log_file, mode='a+')
        handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    except IOError as error:
        print("Warning: unable to set file handler for logger {}".format(str(error)))

    logger.info("**** Rendering *****")
    render_data(args=result, logger=logger)
    logger.info("**** Rendering completed")
    sys.exit(0)

if __name__ == "__main__":
    main()
