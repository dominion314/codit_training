#!/usr/bin/env python3
""" Script to run declarative pipeline validation. Script takes username,
password, jenkins url and working directory as an input. Finds all jenkinsfiles
in working directory and runs query to jenkins to validate pipeline.

"""

import argparse
import os
import logging
import sys
import re
import requests
from requests.auth import HTTPBasicAuth
import urllib3


JENKINSFILE_NAME = 'Jenkinsfile'
JENKINSFILE_FOLDER = 'Jenkinsfiles'
PIPELINE_REG_PATTERN = "pipeline\\s*{"
VALIDATE_URL = "{}pipeline-model-converter/validate"
SUCCESSFUL_VALIDATION = 'Jenkinsfile successfully validated.'
EXIT_FAIL = 1
EXIT_SUCCESS = 0
HTTP_OK_STATUS = 200


def set_logging():
    """ Sets logging.

    :return: None
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    logging.getLogger().setLevel(logging.INFO)


def disable_insecure_url_warnings():
    """ Disable cert warnings.

    :return: None
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_arguments():
    """ Gets arguments from command line.

    :return: populated namespace with arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True,
                        help='Jenkins username', )
    parser.add_argument('-p', '--password', required=True,
                        help='Password of jenkins user')
    parser.add_argument('-j', '--jenkins_url', required=True,
                        help='URL to jenkins instance')
    parser.add_argument('-w', '--work_directory', required=True,
                        help='Path to working directory')

    return parser.parse_args()


def find_jenkinsfiles(work_directory):
    """ Finds jenkinsfiles in specified directory by checking looking for files
    with 'Jenkinsfile' name or by finding directory with name 'Jenkinsfiles'.

    :param work_directory: path to working directory
    :return: list of paths to jenkinsfiles
    """
    jenkinsfiles_paths = []
    for dir_path, _, filenames in os.walk(work_directory):
        for filename in filenames:
            if JENKINSFILE_NAME in filename or JENKINSFILE_FOLDER in dir_path:
                jenkinsfiles_paths.append(os.path.join(dir_path, filename))
    return jenkinsfiles_paths


def filter_declarative_pipelines(jenkinsfile_paths):
    """ Determines whether jenkinsfile is written declarativly.

    :param jenkinsfile_paths: list of paths to jenkinsfiles
    :return: list of paths to declarative jenkinsfiles
    """
    declarative_pipelines = []
    for jenkinsfile in jenkinsfile_paths:
        with open(jenkinsfile, 'r') as contents:
            if re.search(PIPELINE_REG_PATTERN, contents.read()):
                declarative_pipelines.append(jenkinsfile)
    return declarative_pipelines


def get_declarative_pipelines(work_directory):
    """ Finds and returns all declarative pipelines in specified directory.

    :param work_directory: string with directory to search in
    :return: list of paths to declarative pipelines
    """
    jenkinsfile_paths = find_jenkinsfiles(work_directory)
    return filter_declarative_pipelines(jenkinsfile_paths)


def validate_pipeline(pipeline_path, args):
    """ Sends pipeline definition to jenkins server in order to validate it.

    :param pipeline_path: path to declarative jenkinsfile
    :param args: arguments passed to script
    :return: Boolean based on the validation
    """
    with open(pipeline_path, 'r') as contents:
        files = {'jenkinsfile': (None, contents.read())}

    response = requests.post(url=VALIDATE_URL.format(args.jenkins_url),
                             files=files,
                             verify=False,
                             auth=HTTPBasicAuth(args.username,
                                                args.password))

    if response.status_code == HTTP_OK_STATUS and SUCCESSFUL_VALIDATION \
            in response.text:
        logging.info("Jenkinsfile: %s validation passed.", pipeline_path)
        return False

    logging.warning("Jenkinsfile: %s validation failed.\n%s", pipeline_path,
                    response.text)
    return True


def run_linting(args):
    """ Runs linter.

    :param args: arguments passed to script
    :return: None
    """
    results = []
    for pipeline in get_declarative_pipelines(args.work_directory):
        results.append(validate_pipeline(pipeline, args))

    if any(results):
        logging.error("Declarative Jenkinsfile Validation failed")
        sys.exit(EXIT_FAIL)

    sys.exit(EXIT_SUCCESS)


def main():
    """ Main script logic. Exits with RCs:
    0   - declarative pipeline validation passed successfully or jenkinsfile
        not found in the directory
    1   - validation of jenkinsfile not passed

    :return: None
    """
    args = get_arguments()
    disable_insecure_url_warnings()
    set_logging()
    run_linting(args)


main()
