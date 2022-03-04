#!/usr/bin/env python3
""" Script to run config validation of openshift-cluster-config extended with
check whether it affects configuration files generated for each of the
clusters. This script runs normal config validation with dumping of resources
enabled for pr branch. In background it also runs generation of configuration
files from master branch in order to compare it at the end of the process. If
configuration files for master and pr branch differ, this means that change
introduces changes to configuration files for given cluster.

"""

import argparse
import logging
import os
import shutil
import signal
import subprocess
import sys
from time import sleep

ENCODING = 'utf-8'
EXIT_SUCCESS = 0
EXIT_FAIL = 2
RESPONSE_TIME = '30'
DUMP_FOLDER_NAME = 'dump'
RELATIVE_CONFIG_VALIDATION_PATH = 'tests/config-validation'
VALIDATE_YAML_PATH = '{}/validate-config.yml'.format(
    RELATIVE_CONFIG_VALIDATION_PATH)
DUMP_PATH = '{}/{}/{}/'.format('{}', RELATIVE_CONFIG_VALIDATION_PATH,
                               DUMP_FOLDER_NAME)
NO_CHANGES = 'nothing to commit'
NULL_PATH = '/dev/null'
MASTER_BRANCH = 'master'

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)


def get_arguments():
    """ Gets arguments from command line.

    :return: populated arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--master_config_path',
                        help='Path to openshift-cluster-config repository '
                             'checked out on master.')
    parser.add_argument('--pr_config_path',
                        help='Path to openshift-cluster-config repository '
                             'checkoud out on non-master branch')
    parser.add_argument('--cluster_name', help='Name of the cluster')

    return parser.parse_args()


def prepare_ansible_resource_generation_command(config_path='', cluster_name=''):
    """ Prepares config validation command for openshift-cluster-config.

    :param config_path: path to openshift-cluster-config repository
    :param cluster_name: name of openshift cluster
    :return: command as a list of parameters to run
    """
    return ['ansible-playbook',
            '{}/{}'.format(config_path, VALIDATE_YAML_PATH),
            '-e', 'cluster_name={}'.format(cluster_name),
            '-e', 'dump_location={}'.format(DUMP_FOLDER_NAME),
            '-T', RESPONSE_TIME]


def run_parallel(commands):
    """ Runs bash commands in parallel in subprocesses. Stdout for master
    branch is suppressed in order to avoid littering output.

    :param commands: dict with names of the branches as a keys and command to
    run as an item
    :return: True if all run subprocesses finished with success, False when
    on of them failled
    """
    if commands is None:
        commands = []

    os.setpgrp()
    processes = {}

    for branch in commands:
        if branch == MASTER_BRANCH:
            with open(NULL_PATH, 'w') as dev_null_device:
                processes[branch] = subprocess.Popen(commands[branch],
                                                     stdout=dev_null_device)
        else:
            processes[branch] = subprocess.Popen(commands[branch])

    return poll_subprocesses(processes)


def poll_subprocesses(processes):
    """ Polls subprocesses to check return code. Returns false when any of the
    return codes is different than 0.

    :param processes: dict with names of the branches as keys and corresponding
    subprocess as an item
    :return: True if all run subprocesses finished with success, False when
    on of them failled
    """
    while True:
        sleep(1)
        return_codes = []
        for branch in processes:
            return_codes.append(processes[branch].poll())
            if return_codes[-1] and return_codes[-1] != EXIT_SUCCESS:
                logging.error('Subprocesses run on %s branch of '
                              'openshift-cluster-config failed with rc: %s.',
                              branch.upper(), str(return_codes[-1]))
                return False

        if all(rc == 0 for rc in return_codes):
            return True


def run_config_generation(args):
    """ Runs config generation for master and PR branch.

    :param args: arguments passed to script
    :return: True if all run subprocesses finished with success, False when
    on of them failled
    """
    master_command = prepare_ansible_resource_generation_command(
        config_path=args.master_config_path, cluster_name=args.cluster_name)
    pr_command = prepare_ansible_resource_generation_command(
        config_path=args.pr_config_path, cluster_name=args.cluster_name)

    return run_parallel({'pr': pr_command, MASTER_BRANCH: master_command})


def run_git_command(command, git_dir_path=''):
    """ Runs git command in subprocess and waits for it to finish.

    :param command: git command to run
    :param git_dir_path: path to .git directory
    :return: encoded output of run git command
    """
    if git_dir_path:
        command = 'git --git-dir {0}.git --work-tree {0} {1}'.format(git_dir_path,
                                                                     command)
    else:
        command = 'git {}'.format(command)

    process = subprocess.run(command.split(), stdout=subprocess.PIPE, check=True)
    return process.stdout.decode(ENCODING)


def git_init_master(path):
    """ Initializes git repository in given path and creates initial commit.

    :param path: path to the repository
    :return: None
    """
    run_git_command('config --global user.email config_validation')
    run_git_command('config --global user.name config_validation')
    run_git_command('init', path)
    run_git_command('add -A', path)
    run_git_command('commit -m initial', path)


def prepare_git(master_path, pr_path):
    """ Prepares git repository in master and pr paths by creating git
    repository in config generated from master and copying .git directory to
    config generated from pr branch.

    :param master_path: path to generated config from master branch
    :param pr_path: path to generated config from pr branch
    :return: None
    """
    git_init_master(master_path)
    shutil.copytree('{}.git'.format(master_path), '{}.git'.format(pr_path))


def compare_resources(pr_path):
    """ Compares config generated from master branch to config generated from
    pr branch.

    :param pr_path: path to config generated from pr
    :return: True if generated configs match, False otherwise
    """
    status = run_git_command('status', pr_path)
    if NO_CHANGES in status:
        logging.info('This PR doesnt affect configuration for this cluster')
        return True

    run_git_command('add -A', pr_path)
    logging.warning(run_git_command('diff --staged', pr_path))
    return False


def main():
    """ Main script logic. Exits with RCs:
    0   - config validation passed and no changes to cluster configuration
          files
    2   - config validation passed and changes to cluster configuration files
    137 - config validation failed

    :return: None
    """
    args = get_arguments()

    if run_config_generation(args):
        logging.info('Config validation passed')
        master_dump_path = DUMP_PATH.format(args.master_config_path)
        pr_dump_path = DUMP_PATH.format(args.pr_config_path)
        prepare_git(master_dump_path, pr_dump_path)
        if compare_resources(pr_dump_path):
            logging.info('Both config validation and configuration change '
                         'check passed successfully for cluster: %s',
                         args.cluster_name)
            sys.exit(EXIT_SUCCESS)
        else:
            logging.warning('This PR introduces changes for cluster: %s',
                            args.cluster_name)
            sys.exit(EXIT_FAIL)
    else:
        logging.error('Config Validation FAILED. Terminating all processes')
        os.killpg(0, signal.SIGKILL)


main()
