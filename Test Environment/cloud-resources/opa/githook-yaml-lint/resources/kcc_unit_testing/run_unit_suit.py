"""
KCC Unit Test Processor.
it is intended to be executed from linter.
Prerequistes:
- gcloud must be authenticated with service account authorized to work with GKE clsuster
- GOOGLE_APPLICATION_CREDENTIALS environment must point to SA for inspec
"""
#pylint: disable=fixme,broad-except,too-many-arguments
import argparse
from datetime import datetime
import os
import logging
import sys
import subprocess
from subprocess import PIPE
import json
from time import sleep
import yaml

def safe_run(logger, *args, **kwargs):
    """
    Executes external command (python3)
    """
    result = subprocess.run(check=False, *args, **kwargs)
    if result.returncode:
        logger.error("Process exited with code {}".format(result.returncode))
    return result

def remove_files_in_folder(logger, folder, suffix=''):
    """
    Removes files in specified folder
    """
    logger.info("Removing files in folder %s", folder)
    flist = [item for item in os.listdir(folder) if item.endswith(suffix)]
    for item in flist:
        os.remove(os.path.join(folder, item))

def init_log(log_file):
    """
    initializes logger
    """
    logger = logging.getLogger(__name__)
    logger.propagate = False  # do not log to console
    formatter = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
    try:
        handler = logging.FileHandler(log_file, mode='a+')
        handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger
    except IOError as error:
        print("Warning: unable to set file handler for logger {}".format(str(error)))
        return None

def run_inspec_validation(logger, inspec_profile):
    """
    Runs inspec validation in pre-populated profile
    """

    logger.info("Running INSPEC Validation")
    command_list = ['inspec', 'exec', inspec_profile, '-t', 'gcp://']


    env = os.environ.copy()
    #todo: make this configurable
    env['HTTP_PROXY'] = 'http://proxy-gcp-central.doms.com:8080'
    env['HTTPS_PROXY'] = 'http://proxy-gcp-central.doms.com:8080'
    env['http_proxy'] = 'http://proxy-gcp-central.doms.com:8080'
    env['https_proxy'] = 'http://proxy-gcp-central.doms.com:8080'
    try:
        result = safe_run(logger=logger, args=command_list, env=env, stdout=PIPE, stderr=PIPE)
        logger.info(result.stdout)
        logger.info(result.stderr)
        if result.returncode:
            logger.error("Inspec validation failed")
            return False
        logger.info("Inspec validation passed")
        return True
    except BaseException as error:
        logger.error("Failed to execute inspec " + str(error))
        return False

def lookup_suite(suite_def, suite_name):
    """
    Returns unit test definition looked up by name
    """
    for item in suite_def['unitTestSuits']:
        if item['name'] == suite_name:
            return item
    return None

def acquire_creds_for_k8s(logger, project, zone, cluster):
    """
    Brings in credentials for specified cluster local kubectl environment
    """
    result = safe_run(logger, args=['gcloud', 'container', 'clusters', 'get-credentials',
                                    cluster, '--zone', zone, '--project', project],
                      stdout=PIPE, stderr=PIPE)
    if result.returncode != 0:
        logger.error("Failed to obtain credentials for cluster %s in project %s in zone %s",
                     cluster, project, zone)
        return False
    logger.info(result.stdout)
    logger.info(result.stderr)
    logger.info("Obtained credentials for cluster %s in project %s in zone %s",
                cluster, project, zone)
    return True

def render(logger, script_path, project_id, project_folder, unit_home,
           tests, inspec_profile, kcc_file, input_var_file, log_file):
    """
    Prepares kcc.yml, input.yml and inspec control files
    """
    #preventive clean up product files
    try:
        os.remove(kcc_file)
        os.remove(input_var_file)
    except OSError:
        pass

    # clean up any existing inspec contol files
    logging.info("Cleaning up inspec controls")
    inspec_controls = os.path.join(inspec_profile, 'controls')
    inspec_files = os.path.join(inspec_profile, 'files')
    remove_files_in_folder(logger, inspec_controls, '.rb')
    remove_files_in_folder(logger, inspec_files, '.yml')
    payload = {'project': {'name': project_id, 'folderId': project_folder}}
    payload_s = json.dumps(payload)
    result = safe_run(logger, args=['python3', script_path, '--log_file={}'.format(log_file),
                                    '--inject_data={}'.format(payload_s),
                                    '--unit_tests_home={}'.format(unit_home),
                                    '--unit_tests={}'.format(tests),
                                    '--result_input_var_file={}'.format(input_var_file),
                                    '--result_kcc_file={}'.format(kcc_file),
                                    '--result_inspec_controls_home={}'.format(inspec_controls)])
    if result.returncode:
        logger.error("Failed to render!")
        return False
    return True

def k8s_create_namespace(logger, kctl_bin, namespace, project_id):
    """
    creates namespace, annotates it with project
    """
    result = safe_run(logger, args=[kctl_bin, 'create', 'namespace', namespace], stdout=PIPE)
    if result.returncode:
        logger.error("Failed to create namespace")
        return False

    result = safe_run(logger, args=[kctl_bin, 'annotate', 'namespace', namespace,
                                    "cnrm.cloud.google.com/project-id={}".format(project_id)],
                      stdout=PIPE)
    if result.returncode:
        logger.error("Failed to annotate namespace!")
        return False

    logger.info("Created namespace %s with annotation for project %s", namespace, project_id)
    return True

def k8s_create_deployment(logger, kctl_bin, deployment):
    """
    Deploys to k8s
    """
    result = safe_run(logger, args=[kctl_bin, 'apply', '-f', deployment], stdout=PIPE)
    if result.returncode:
        logger.error("Failed to apply deployment {}".format(deployment))
        return False
    logger.info(result.stdout)
    logger.info("Applied %s to k8s", deployment)
    return True

def k8s_delete_deployment(logger, kctl_bin, deployment):
    """
    Delete from k8s
    """
    result = safe_run(logger, args=[kctl_bin, 'delete', '-f', deployment], stdout=PIPE)
    if result.returncode:
        logger.error("Failed to delete deployment {}".format(deployment))
        return False
    logger.info(result.stdout)
    logger.info("Deleted deployment %s from k8s", deployment)
    return True

def k8s_delete_namespace(logger, kctl_bin, namespace):
    """
    deletes namespace
    kubectl delete namespaces <name>
    """
    result = safe_run(logger, args=[kctl_bin, 'delete', 'namespaces', namespace], stdout=PIPE)
    if result.returncode:
        logger.error("Failed to delete namespace!")
        return False
    logger.info("Deleted namespace {}".format(namespace))
    return True


def get_unique_project_id(prefix):
    """
    Generates unique project name with specified prefix
    the format is going to be prefix-YYYMMMDDDHHMMSSSSS..
    """
    suffix = datetime.now().strftime("%Y%m%d%H%M%f")
    result = prefix+suffix
    if len(result) > 30:
        return None
    return result

def main():
    """
    Main method
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-file', action='store', dest='log_file', help='Log file')
    parser.add_argument('--unit-test-suite-definition', action='store', dest='unit_def',
                        help='File with YAML definition of unit test suits')
    parser.add_argument('--kubectl-binary', action='store', dest='kubectl_binary',
                        help='Kubectl binary path')
    parser.add_argument('--yq-binary', action='store', dest='yq_binary',
                        help='yq binary path')
    parser.add_argument('--suite-names', action='store', dest='suites_names',
                        help='Names of the test suits to execute(comma separated)')
    parser.add_argument('--result_kcc_file', action='store', dest='kcc_file',
                        help='Merged KCC file')
    parser.add_argument('--inspec-profile', action='store',
                        dest='inspec_profile',
                        help='Inspec profile path')
    parser.add_argument('--render-script-path', action='store',
                        dest='render_script_path',
                        help='render that renders materials for KCC and inspec')

    params = parser.parse_args()
    # inialize logging
    logger = init_log(params.log_file)
    if logger is None:
        sys.exit(1)
    logger.info("**** STARTED ****")

    suites = list()
    # load unit test definition
    with open(params.unit_def) as f_in:
        suite_def_dict = yaml.load(f_in, Loader=yaml.SafeLoader)

        suites_names_list = [item.strip() for item in params.suites_names.split(',')]
        if len(suites_names_list) < 1:
            logger.error("No test suites are requested...NOP")
            sys.exit(0)

        for item in suites_names_list:
            logger.info(" Looking up suite %s...", item)
            suite = lookup_suite(suite_def_dict, item)
            if suite is None:
                logger.error("Requested suite {} was not found in test suite definition! Aborting")
                sys.exit(1)
            else:
                suites.append(suite)

    # start unit testing cycle. Stop at first failure
    for suite in  suites:
        if not run_cycle(logger, suite, params):
            sys.exit(1)

    sys.exit(0)


def run_cycle(logger, suite, params):
    """
    Running one unit test suite
    """
    logger.info("Running Testing Cycle for Test suite {}".format(suite["name"]))
    logger.info("{}".format(suite))
    # acquire credentials for cluster
    if not acquire_creds_for_k8s(logger,
                                 project=suite['k8sCluster']['hostProject'],
                                 zone=suite['k8sCluster']['zone'],
                                 cluster=suite['k8sCluster']['clusterName']):
        logger.error("Failed to acquire credentials for cluster")
        return False

    # generate project name
    project_id = get_unique_project_id(prefix=suite['gcpProject']['prefix'])
    if project_id is None:
        logger.error("Unable to create appropriate project_id (generated id is too long)")
        return False

    # render materials
    input_file = os.path.join(params.inspec_profile, 'files', 'input.yml')
    kcc_file = params.kcc_file
    render_passed = False
    render_passed = render(logger=logger,
                           script_path=params.render_script_path,
                           project_id=project_id,
                           project_folder=suite['gcpProject']['homeFolderId'],
                           unit_home=suite['homeDir'],
                           tests=suite['cases'],
                           inspec_profile=params.inspec_profile,
                           kcc_file=kcc_file,
                           input_var_file=input_file,
                           log_file=params.log_file
                          )
    if not render_passed:
        logger.error("Rendering failed!")
        return False

    validation_passed = False
    namespace = suite['k8sCluster']['namespacePrefix']+project_id
    if k8s_create_namespace(logger,
                            params.kubectl_binary,
                            namespace=namespace,
                            project_id=project_id):
        if k8s_create_deployment(logger, params.kubectl_binary, kcc_file):
            # todo: made 'calculated' pause
            sleep(120)
            if run_inspec_validation(logger, params.inspec_profile):
                validation_passed = True

            if (validation_passed or \
                (not validation_passed and suite['gcpProject']['preserveOnFailure'] == "false")):
                logger.info("Removing deployment and namespace....")
                k8s_delete_deployment(logger, params.kubectl_binary, kcc_file)
                k8s_delete_namespace(logger, params.kubectl_binary, namespace=namespace)

            # log kcc and input
            logger.info("******* kcc.yml *******")
            with open(kcc_file) as f_in:
                content = f_in.read()
                logger.info(content)
            logger.info("******* input.yml ******")
            with open(input_file) as f_in:
                content = f_in.read()
                logger.info(content)
        else:
            logger.error("Failed to deploy to k8s!")
            return False
    else:
        logger.error("Failed create k8s namespace !")
        return False

    logger.info("Successfully Completed Testing Cycle for Test suite {}".format(suite["name"]))
    return True
if __name__ == "__main__":
    main()
    