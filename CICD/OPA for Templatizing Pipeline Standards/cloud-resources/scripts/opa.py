#pylint: skip-file
"""
This is a script that runs OPA evaluation of 'input' data using manifest file to obtain additional
information about policy data and REGO file.
"""
import logging
import sys
import os
import argparse
import subprocess
import tempfile
from itertools import repeat
import json
import yaml
import hiyapyco

logger = logging.getLogger(__name__)
OPA_VIOLATION_VALUE = 'policy_violation'

def writeout_report(r, project, suite):
    """
    Format of Report.  Write to report, tuple of variables stored in r
    """
    warning = False
    result_allowed = True
    result = []

    for policy in r[1]:
        policy_name = str(policy[1]['result'][0]['expressions'][0]['text'])
        with open(suite) as suite_f:
            suite_enforces = yaml.load(suite_f, Loader=yaml.SafeLoader)
            for item in suite_enforces["policies"]:
                if item['package'] == policy_name[5:]:
                    if item['enforce']:
                        enforced = True
                    else:
                        enforced = False

        result.append(policy_name)
        if policy[0]:
            result.append(" --> Allowed: True\n".rjust(80-len(policy_name)))
        elif not policy[0] and not enforced:
            result.append(" --> Allowed: Not Enforced - False\n".rjust(80-len(policy_name)+16))
        else:
            result.append(" --> Allowed: False\n".rjust(80-len(policy_name)+1))

        try:
            violations = policy[1]['result'][0]['expressions'][0]['value'][OPA_VIOLATION_VALUE]
            if isinstance(violations[0], list):
                for violation in violations:
                    if len(violation) == 3: # For String(Problem Explanation), List(Correction), List(Violations)
                        if isinstance(violation[2], list):
                            if len(violation[2]) > 0:
                                result.append("- " + str(violation[0]) + ": ----> " + ", ".join(violation[1]) + "\n")

                                warning = True
                                if enforced and not policy[0]:
                                    result_allowed = False
                        elif violation[2]: # For String(Problem Explanation), List/Dict(Correction), Boolean(Violation - T/F)
                                if isinstance(violation[1][0], dict): #Used for Allowed ProjectID List
                                    processed_correction = []
                                    for current_dict in violation[1]:
                                        processed_correction.append(":".join(list(current_dict.items())[0]))
                                    result.append("- " + str(violation[0]) + ": ----> " + ", ".join(processed_correction) + "\n")
                                else:
                                    result.append("- " + str(violation[0]) + ": ----> " + ", ".join(violation[1]) + "\n")

                                warning = True
                                if enforced and not policy[0]:
                                    result_allowed = False
                    else:
                        if isinstance(violation[1], bool): # For boolean(Problem Explanation), Boolean(Violation - T/F)
                            if violation[1]:
                                result.append("- " + str(violation[0]) + "\n")
                                warning = True
                                if enforced and not policy[0]:
                                    result_allowed = False
                        elif len(violation[1]) > 0: # For String(Problem Explanation), List(Violations)
                            result.append("- " + str(violation[0]) + ": ----> " + ", ".join(violation[1]) + "\n")
                            warning = True
                            if enforced and not policy[0]:
                                result_allowed = False

            else:
                result.append("- Cause of Policy Violation: " + ", ".join(violations) + "\n")
                if enforced and not policy[0]:
                    result_allowed = False

        except LookupError:
            if not policy[0]:
                result.append("- Violating resources are not available.\n")
                if enforced:
                    result_allowed = False
    result.append("-------------------------------\n")

    if not result_allowed and not r[0]:
        result.insert(0, "******* Validating Policies for Project {} *********\n".format(project))
        result.insert(1, "Overall Policy Result --> Not Allowed\n")
        result.insert(2, ">>> VALIDATING POLICY DETAIL <<<\n")
    else:
        result.insert(0, "******* Evaluated Policies for Project {} *********\n".format(project))
        result.insert(1, "Overall Policy Result --> Allowed with Warning\n")
        result.insert(2, ">>> POLICY DETAIL <<<\n")

    return result, warning, result_allowed

def yml_files_to_json_file(yml_files, prefix='', cluster=''):
    """
    Loads yaml from file, convers to JSON and stores in temp file
    """
    _, temp_file = tempfile.mkstemp(suffix='.json', prefix=prefix)
    # merge yml files into one without overwrite
    merged_yml = hiyapyco.load(yml_files, method=hiyapyco.METHOD_MERGE)
    if cluster != '':
        merged_yml["cluster"] = cluster
    with open(temp_file, 'w') as outfile:
        outfile.write(json.dumps(merged_yml))
    return temp_file

def is_opa_allowed(input_file, policy_data_file, rego_file, package, args):
    """
    Runs OPA evaluation with given data, parses and interprets result
    """
    arg_list = [args.opa_binary, 'eval', '-i', input_file, '-d', policy_data_file,
                '-d', rego_file, "data.{}".format(package)]
    result = subprocess.run(' '.join(arg_list),
                            shell=True, stdout=subprocess.PIPE)
    if result.returncode:
        logger.error("Process exited with code {}".format(result.returncode))
    if result.returncode == 0:
        logger.info("OPA evaluation compeleted\nResult set. START\n{}\nResult set. END".format(result.stdout.decode('utf-8')))
        try:
            r_parsed = json.loads(result.stdout)
            #todo: make sure that parsing is reliable
            allowed = r_parsed['result'][0]['expressions'][0]['value']['allow']
            return allowed, r_parsed
        except BaseException:
            logger.error("Failed to parse result set!")
            return False, {}
    else:
        logger.error("OPA evaluation failed!{}".format(result.stderr))
        return False, {}


def process_opa(processed_yml, args):
    """
    Process OPA on temp file
    """
    if '-qa' in args.cluster_environment:
        input_cluster = 'qa_cluster'
    else:
        input_cluster = 'prd_cluster'
    input_data_file = yml_files_to_json_file(
        yml_files=[processed_yml], prefix="input_")
    return_tuples = []
    project_return_status = True
    with open(args.suite) as suite_f:
        suites = yaml.load(suite_f, Loader=yaml.SafeLoader)
        return_tuples = []
        for item in suites["policies"]:
            if item['active']:
                #load policy data
                policy_yml_files = item['policyDataFiles']
                policy_data_file = yml_files_to_json_file(
                    yml_files=policy_yml_files,
                    prefix="policy_",
                    cluster=input_cluster
                )
                rego_file = item["policyRegoFile"]
                package = item["package"]
                allowed, result = is_opa_allowed(
                    input_file=input_data_file,
                    policy_data_file=policy_data_file,
                    rego_file=rego_file,
                    package=package,
                    args=args
                )
                if not allowed:
                    project_return_status = False
                return_tuples.append((allowed, result))
                try:
                    os.remove(policy_data_file)
                except BaseException:
                    pass

    if return_tuples:
        return project_return_status, return_tuples
    return True, None

def main():
    """
    Main entry point
    """
    # Import Args
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store', dest='input', help='Folder containing each of the projects.')
    parser.add_argument('--suite_definition', action='store', dest='suite',
                        help='File defining policy suite definition')
    parser.add_argument('--log_file', action='store', dest='log_file', help='Log file')
    parser.add_argument('--report_file', action='store', dest='report_file', help='Report file')
    parser.add_argument('--opa_binary', action='store', dest='opa_binary', help='OPA binary')
    parser.add_argument('--cluster_environment', action='store', dest='cluster_environment', help='Cluster Environment')
    args = parser.parse_args()

    # init logging
    logger.propagate = False  # do not log to console
    fmt = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
    try:
        log_handler = logging.FileHandler('{}'.format(args.log_file), mode='a')
        log_handler.setFormatter(fmt)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_handler)
    except IOError as error:
        print("Warning: unable to set file handler for logger {}".format(str(error)))
    report_f = open(args.report_file, 'a+') #Unique
    project_paths = []
    project_list = []
    for project in os.scandir(args.input):
        if project.is_dir():
            project_list.append(project.path.split('/')[-1:])
            project_paths.append(project.path + '/processed_values.yml')

    reports = map(process_opa, project_paths, repeat(args))

    #Writes Report File
    allowed_projects = []
    denied_reports = []
    policies = []
    policies_found = False
    i = 0
    for report in reports:
        current_report, warning, result_allowed = writeout_report(report, "".join(project_list[i]), args.suite)
        if not result_allowed:
            denied_reports.append(current_report)
        elif warning:
            denied_reports.append(current_report)
            allowed_projects.append("".join(project_list[i]))
        else:
            allowed_projects.append("".join(project_list[i]))
            if not policies_found:
                for policy in report[1]:
                    policies.append(str(policy[1]['result'][0]['expressions'][0]['text']))
                policies_found = True
        i += 1

    allowed_projects_num = len(allowed_projects)
    projects_num = len(project_list)
    if (projects_num > 1):
        report_f.write("********* " + str(allowed_projects_num) + "/" + str(projects_num) + " Projects Allowed *********\n")

        if (allowed_projects_num > 0):
            report_f.write("Project(s) Allowed --> \n")

            for i in range(allowed_projects_num):
                report_f.write(allowed_projects[i])

                if (i + 1) % 4 == 0 or i + 1 == allowed_projects_num:
                    report_f.write("\n")
                else:
                    report_f.write("," + " " * (31 - len(allowed_projects[i])))

    elif (allowed_projects_num == 1):
        report_f.write("********* One Project Change: " + "".join(project_list[0]) + " --> Allowed *********\n")
    else:
        report_f.write("********* One Project Change: " + "".join(project_list[0]) + " --> Not Allowed *********\n")

    for report in denied_reports:
        for line in report:
            report_f.write(line)

    if allowed_projects_num == projects_num:
        if len(denied_reports) == 0:
            report_f.write(">>> OVERALL POLICY DETAILS <<<\n")
            for policy in policies:
                report_f.write(policy + " --> Allowed: True\n".rjust(80-len(policy)))

        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()
