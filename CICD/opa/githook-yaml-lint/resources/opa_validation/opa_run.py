"""
This is a script that runs OPA evaluation of 'input' data using manifest file to obtain additional
information about policy data and REGO file.
"""
#disable some of pylint parandoid complains
#pylint: disable=W0511,R0913,W0703,C0103,R0801,E0401
import os
import sys
import tempfile
import argparse
import logging
#import to support external process execution
import subprocess
from subprocess import PIPE
import json
import yaml
import hiyapyco


def yml_files_to_json_file(yml_files, prefix=''):
    """
    Loads yaml from file, convers to JSON and stores in temp file
    """
    _, temp_file = tempfile.mkstemp(suffix='.json', prefix=prefix)
    # merge yml files into one without overwrite
    merged_yml = hiyapyco.load(yml_files, method=hiyapyco.METHOD_MERGE)
    with open(temp_file, 'w') as outfile:
        outfile.write(json.dumps(merged_yml))

    return temp_file


def safe_exec(log, *args, **kwargs):
    """
    Executes external command with arguments
    In case of error logs exit code
    """

    exec_result = subprocess.run(check=False, *args, **kwargs)

    if exec_result.returncode:
        log.error("Process exited with code {}".format(exec_result.returncode))

    return exec_result

def is_opa_allowed(logger, opa_binary, input_file, policy_data_file, rego_file, package):
    """
    Runs OPA evaluation with given data, parses and interprets result
    """
    arg_list = [opa_binary, 'eval', '-i', input_file, '-d', policy_data_file,
                '-d', rego_file, "data.{}".format(package)]
    result = safe_exec(log=logger, args=arg_list, stdout=PIPE, stderr=PIPE)
    if result.returncode == 0:
        logger.info("OPA evaluation compeleted")
        logger.info("Result set. START")
        logger.info(result.stdout.decode('utf-8'))
        logger.info("Result set. END")
        try:
            r_parsed = json.loads(result.stdout)
            #print(r_parsed)
            #todo: make sure that parsing is reliable
            allowed = r_parsed['result'][0]['expressions'][0]['value']['allow']
            return allowed
        except BaseException:
            logger.info("Failed to parse result set!")
            return False
    else:
        logger.error("OPA evaluation failed!{}".format(result.stderr))
        return False

def run(logger, report, args):
    """
    Processor
    """
    # Store input data
    input_data_file = yml_files_to_json_file(yml_files=[args.input], prefix="input_")

    NOT_ALLOWED = False
    with open(args.suite) as suite_f:
        suites = yaml.load(suite_f, Loader=yaml.SafeLoader)
        for item in suites["policies"]:
            if item['active']:
                logger.info("Processing policy '{}'".format(item['name']))
                #load policy data
                policy_yml_files = item['policyDataFiles']
                policy_data_file = yml_files_to_json_file(
                                        yml_files=policy_yml_files,
                                        prefix="policy_"
                                        )
                rego_file = item["policyRegoFile"]
                package = item["package"]
                allowed = is_opa_allowed(
                                        logger=logger,
                                        opa_binary=args.opa_binary,
                                        input_file=input_data_file,
                                        policy_data_file=policy_data_file,
                                        rego_file=rego_file,
                                        package=package
                                        )
                try:
                    os.remove(policy_data_file)
                except BaseException:
                    pass

                if not allowed:
                    logger.error(">>>>>>>> '{}' NOT ALLOWED".format(item['name']))
                    NOT_ALLOWED = True
                    report.write("Policy '{}' ---> FAILED\n".format(item['name']))
                    report.flush()
                else:
                    logger.info(">>>>>>>>> '{}' ALLOWED".format(item['name']))
                    report.write("Policy '{}' ---> passed\n".format(item['name']))
                    report.flush()
    try:
        os.remove(input_data_file)
    except BaseException:
        pass

    if NOT_ALLOWED:
        return False

    return True

def main():
    """
    Main method
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store', dest='input', help='input data to be validated')
    parser.add_argument('--suite_definition', action='store', dest='suite',
                        help='File defining policy suite definition')
    parser.add_argument('--log_file', action='store', dest='log_file', help='Log file')
    parser.add_argument('--report_file', action='store', dest='report_file', help='Report file')
    parser.add_argument('--opa_binary', action='store', dest='opa_binary', help='OPA binary')
    args = parser.parse_args()

    # initialze logging
    log = logging.getLogger(__name__)
    log.propagate = False  #do not log to console
    formatter = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
    try:
        handler = logging.FileHandler(args.log_file, mode='a')
        handler.setFormatter(formatter)
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)
    except IOError as error:
        print("Warning: unable to set file handler for logger {}".format(str(error)))

    # open report file
    report_f = open(args.report_file, 'a+')
    allowed = run(log, report_f, args)
    if allowed:
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
