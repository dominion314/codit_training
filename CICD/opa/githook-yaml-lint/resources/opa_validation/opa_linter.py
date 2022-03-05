"""
OPA based policy  validation
"""
#disable pylint related to too many variables, too many branches, too many statements
#pylint: disable=R0914,W1202,C0103,W0511,R0913,W0703,C0301,R0801

import subprocess
from subprocess import PIPE
import sys
import argparse
import os
import logging
import tempfile
import yaml

def safe_run(logger, *args, **kwargs):
    """
    Executes external command
    Logs exit code in case of error
    """
    result = subprocess.run(check=False, *args, **kwargs)
    if result.returncode:
        logger.error("Exited with code {}".format(result.returncode))
    return result

def process_input(logger, project_folder):
    """
    Merges project vars and store the result in temp yml file
    """
    logger.info("Processing input data for {}".format(project_folder))
    yml_files = [file for file in os.listdir(project_folder) if file.endswith('.yml')]
    _, temp_file = tempfile.mkstemp(suffix='.yml', prefix="input_")

    if len(yml_files) == 1:
        cmd = "cp {} {}".format(os.path.join(project_folder, yml_files[0]), temp_file)
    else:
        cmd = "yq merge {}/*.yml > {}".format(project_folder, temp_file)

    os.system(cmd)
    return temp_file

def main():
    """
    Main entry point
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--opa_config', action='store', dest='opa_config',
                            help='Config file for OPA validation')
    arg_parser.add_argument('--opa_binary', action='store', dest='opa_binary', help='OPA binary')
    arg_parser.add_argument('--opa_runner', action='store', dest='opa_runner',
                            help='Python script that runs validation')
    arg_parser.add_argument('--opa_suite_definition', action='store', dest='opa_def',
                            help='OPA Suite definition file')
    arg_parser.add_argument('--log_file', action='store', dest='log_file', help='Log file')
    arg_parser.add_argument('--report_file', action='store', dest='report_file', help='Report file')
    args = arg_parser.parse_args()

    # initialze logging
    logger = logging.getLogger(__name__)
    logger.propagate = False  #do not log to console
    fmt = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
    try:
        log_handler = logging.FileHandler(args.log_file, mode='a')
        log_handler.setFormatter(fmt)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_handler)
    except IOError as error:
        print("Warning: unable to set file handler for logger {}".format(str(error)))

    report_f = open(args.report_file, 'a+')
    NOT_ALLOWED = False
    with open(args.opa_config) as f_in:
        opa_config = yaml.load(f_in, Loader=yaml.SafeLoader)
        logger.info("Loaded OPA validation config")
        if opa_config['enabled']:
            # load dir content, and go after each project
            # the projectVarFolder is relative path from the path of args.opa_config
            # ( root of config repo root )
            # we need to make it absolute before start using it.
            root_path = os.path.dirname(os.path.abspath(args.opa_config))
            project_folder_abs_path = os.path.join(root_path, opa_config['projectVarFolder'])
            project_list = os.listdir(project_folder_abs_path)
            for project in project_list:
                if ((not opa_config['validateAllProjects']) and (project in opa_config['validateProjects'])) or (opa_config['validateAllProjects']):
                    logger.info("Processing project data for {}".format(project))
                    input_var_file = process_input(logger, os.path.join(project_folder_abs_path,
                                                                        project))
                    arg_list = [
                        'python3',
                        args.opa_runner,
                        '--log_file={}'.format(args.log_file),
                        '--input={}'.format(input_var_file),
                        '--opa_binary={}'.format(args.opa_binary),
                        '--suite_definition={}'.format(args.opa_def),
                        '--report_file={}'.format(args.report_file)
                    ]
                    report_f.write("******* Validating policies for project {} *********\n".format(project))
                    report_f.flush()
                    result = safe_run(logger=logger, args=arg_list, stdout=PIPE, stderr=PIPE)
                    report_f.write("------------------------------------------------------------------------\n")
                    report_f.flush()
                    if result.returncode != 0:
                        NOT_ALLOWED = True

    if NOT_ALLOWED:
        logger.info("Some of policy checks were not OK")
        sys.exit(1)

    logger.info("All policy checks were OK ")
    sys.exit(0)

if __name__ == "__main__":
    main()
