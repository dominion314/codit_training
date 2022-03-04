#pylint: skip-file
"""
This is a script that runs OPA evaluation of 'input' data using manifest file to obtain additional
information about policy data and REGO file.

## In this file, verbose comments that start with '##', were added to the original code to more fully
##  explain what the code does.  Original comments were left intact.

"""

## Import code from other packages, modules, and methods

import logging  	## package to log messages.
import sys  		## module to access Python interpreter functions and settings.
import os  			## module to access operating system specific functions and settings.
import argparse  	## module to get command arguments from the user.
import subprocess  	## module to spawn child processes, and grab their output.
import tempfile  	## module to create/delete temporary files and directories.

from itertools import repeat  	## method that outputs its given input during each loop iteration.

import json  	## module for JSON data encoding and decoding.
import yaml  	## external package to parse or emit YAML formatted data.

import hiyapyco  ## external package for hierarchical overlay or merge of multiple config files
                 ##   in YAML syntax.

logger = logging.getLogger(__name__)  ## This creates a Python logging object named '__main__', 

OPA_VIOLATION_VALUE = 'policy_violation'  ## sets a string global variable


## This defines function writeout_report().
def writeout_report(r, project, suite):  
    """
    Format of Report.  Write to report, tuple of variables stored in r
    """
    
    warning = False  		## Initialize warning to False
    result_allowed = True 	## Initialize result_allowed to True
    result = []  			## Initialize empty list

    ## From the second item in the given 'r' data-structure, Loop through its elements as 'policy'.
    ##    Get the policy name from the second item in the 'policy' data-structure, by traversing it down to 'text'.
    ##    In a 'with' code block, open the file specified as 'suite' as an object named 'suite_f'.
    ##        - Read the yaml data from 'suite_f' and transform into variable 'suite_enforces'.
    ##            - Note that: yaml.SafeLoader is a form of security protection against malicious 
    ##              yaml files from an untrustworthy source.
    ##        - Loop through 'suite_enforces' 'policies' getting each as 'item':
    ##            If all but the first 5 characters of of 'policy_name' equals the the package string within item:
    ##               then if item has an 'enforce' variable, then set a local variable 'enforced' to True.
    ##               Otherwise, set 'enforced' to False.
    ##        - The file will be closed when 'with' block execution has concluded.
    ##        
    ##       Append the found 'policy_name' to the 'result' list.
    ##        
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

        ## If there is any value in 'policy' at location [0], then 
        ##     - Append to the 'result' list a right justified left padded string with a length of
        ##       80 minus the length of the current 'policy_name' string, like:
        ##       "                                          -> Allowed: True\n"
        ## Else If thre is no value in policy[0], and 'enforced' is False:       
        ##     - Append to the 'result' list a right justified left padded string with a length of
        ##       80 minus the length of the current 'policy_name' string plus 16, like:
        ##       "                                        --> Allowed: Not Enforced - False\n"
        ## Else 
        ##     - Append to the 'result' list a right justified left padded string with a length of
        ##       80 minus the length of the current 'policy_name' string plus 1, like:
        ##       "                                         -> Allowed: False\n"
        ##            
        ##
        if policy[0]:
            result.append(" --> Allowed: True\n".rjust(80-len(policy_name)))
        elif not policy[0] and not enforced:
            result.append(" --> Allowed: Not Enforced - False\n".rjust(80-len(policy_name)+16))
        else:
            result.append(" --> Allowed: False\n".rjust(80-len(policy_name)+1))


        ## This is a try/except code block with no 'finally' clause specified.  The purpose of using try/except
        ## is to prevent program failure if a lookupError is encountered while examing the 'policy' data-structure.
        ## In multiple places isinstance() is used to verify the data type of a target variable, and
        ## is used as a condition for access to those variables, and to know how to access them.
        ## 
        try:
            ## Frist get 'violations' from traversing the 'policy' data-structure. 
            violations = policy[1]['result'][0]['expressions'][0]['value'][OPA_VIOLATION_VALUE]

            ## if element 0 of violations is a list:
            if isinstance(violations[0], list):
                for violation in violations:  ## Loop through the violations and for each 'violation'

                    ## If 'violation' length is 3:
                    if len(violation) == 3: # For String(Problem Explanation), List(Correction), List(Violations)

                        ## If a list is found in the 3rd element of 'violation':
                        if isinstance(violation[2], list):
                            if len(violation[2]) > 0:  ## if there is at least 1 item in the list:
                                ## append a string to the result list.  In the following line the str() function is
                                ## used to add the contents of violation[0] to the string as a string.  The (", ".join()) 
                                ## will produce a string using ", " as a delimiter between the elements of the given list.
                                ## The + signs simply add each of the strings together into one string.
                                result.append("- " + str(violation[0]) + ": ----> " + ", ".join(violation[1]) + "\n")

                                warning = True  ## Initialize warngin to True.

                                ## If the value of enforced is True and element 0 of policy is False:
                                if enforced and not policy[0]:
                                    result_allowed = False  ## set result_allowed to False.

                        ## Else If the 3rd  element of violation is set:
                        elif violation[2]: # For String(Problem Explanation), List/Dict(Correction), Boolean(Violation - T/F)

                                ## if element #0 of element #1 in 'violation' is of data type dictionary:
                                if isinstance(violation[1][0], dict): #Used for Allowed ProjectID List
                                    processed_correction = []  ## Initialize an empty list.

                                    ## Loop through elements of element #1 of 'violation', iteratively setting current_dict:
                                    for current_dict in violation[1]:
                                        ## Create a string containing only the first dict item of current_dict.  That will have
                                        ## a key_name and a value. The code will produce a colon delimited string containing
                                        ## 'KEY:VALUE'.  Append the string to the processed_correction list.
                                        processed_correction.append(":".join(list(current_dict.items())[0]))

                                    ## Append a single string to the result list containing a comma separated list of processed correction:
                                    ##  "- VIOLATION_0: ----> PROCESSED_CORRECTION, PROCESSED_CORRECTION\n"
                                    result.append("- " + str(violation[0]) + ": ----> " + ", ".join(processed_correction) + "\n")
                                else:
                                    ## Append a single string to the result list containing:
                                    ##  "- VIOLATION_0: ----> VIOLATION, VIOLATION\n"
                                    result.append("- " + str(violation[0]) + ": ----> " + ", ".join(violation[1]) + "\n")

                                warning = True  ## Initialize warning to True

                                ## If the value of enforced is True and element 0 of policy is False:
                                if enforced and not policy[0]:
                                    result_allowed = False  ## set result_allowed to False

                    ## Else because the length of 'violation' is not 3:
                    else:
                        ## If the data type of item #1 of violation is a boolean:
                        if isinstance(violation[1], bool): # For boolean(Problem Explanation), Boolean(Violation - T/F)

                            if violation[1]:  ## if violation[1] is True
                                result.append("- " + str(violation[0]) + "\n")  ## Append '- violation[0]\n' to the result list.
                                warning = True  ## Initialize warning to True

                                ## If the value of enforced is True and element 0 of policy is False:
                                if enforced and not policy[0]:
                                    result_allowed = False  ## set result_allowed to False

                        ## Else if the length of violation[1] is greater than 0:
                        elif len(violation[1]) > 0: # For String(Problem Explanation), List(Violations)
                            ## append a string to the result list containing:
                            ## ("- VIOLATION_0: ----> VIOLATION, VIOLATION\n")
                            result.append("- " + str(violation[0]) + ": ----> " + ", ".join(violation[1]) + "\n")
                            warning = True  ## Initialize warning to True

                            ## If the value of enforced is True and element 0 of policy is False:
                            if enforced and not policy[0]:
                                result_allowed = False  ## set result_allowed to False

            ## Else (element 0 of violations is NOT a list):
            else:
                ## Append a string to the result list containing a comma separated list of violations like:
                ## ("- Cause of Policy Violation: VIOLATION, VIOLATION\n")
                result.append("- Cause of Policy Violation: " + ", ".join(violations) + "\n")

                ## If the value of enforced is True and element 0 of policy is False:
                if enforced and not policy[0]:
                    result_allowed = False  ## set result_allowed to False

        ## If a LookupError exception is encountered during execution of any above code within the 'try' block,
        ## then handle the exception as follows.
        except LookupError:
            if not policy[0]:  ## if element 0 of policy is False:
                ## Append the following constant string to the result list.
                result.append("- Violating resources are not available.\n")

                ## If the value of enforced is True:
                if enforced:
                    result_allowed = False  ## set result_allowed to False

    ## append a constant string containing the following hyphens ending in a newline character to the result list.
    result.append("-------------------------------\n")

    ## If result_allowed is False and the first element of 'r' is False:
    if not result_allowed and not r[0]:
        ## The following 3 list inserts places 3 strings in the order shown at the head of the list, starting at index 0.
        ## The format() function does no special formatting in this code.  It takes the value of 'project', and inserts
        ## it into the string where the {} placeholder is located.
        result.insert(0, "******* Validating Policies for Project {} *********\n".format(project))
        result.insert(1, "Overall Policy Result --> Not Allowed\n")
        result.insert(2, ">>> VALIDATING POLICY DETAIL <<<\n")
    ## Else (the above 'if' conditions evaluated to False)
    else:
        ## The following 3 list inserts, together place 3 strings in the order shown at the head of the list, starting at index 0.
        ## The format() function does no special formatting in this code.  It takes the value of 'project', and inserts
        ## it into the string where the {} placeholder is located.
        result.insert(0, "******* Evaluated Policies for Project {} *********\n".format(project))
        result.insert(1, "Overall Policy Result --> Allowed with Warning\n")
        result.insert(2, ">>> POLICY DETAIL <<<\n")

    ## This writeout_report(r, project, suite) function with arguments returns a tuple data-structure containing 3 variables
    ## that are accessible by their given position in the tuple, when this function is called by another function.  
    return result, warning, result_allowed

## This defines function yml_files_to_json_file().
def yml_files_to_json_file(yml_files, prefix=''):
    """
    Loads yaml from file, convers to JSON and stores in temp file
    """
    ## tempfile.mkstemp() returns a tuple data-structure containing 2 variables.
    ## This call to mkstemp() uses an '_' to ignore the first variable.
    ## Here, mkstemp() will create a temporary file with a filename suffix of '.json' with permission bits that only allow
    ## read and write access to the owner of the file.
    _, temp_file = tempfile.mkstemp(suffix='.json', prefix=prefix)

    # merge yml files into one without overwrite
    ## Merge all yaml files into a single 'merged_yml' data-structure, where sub elements with matching key_names are concatenated.
    merged_yml = hiyapyco.load(yml_files, method=hiyapyco.METHOD_MERGE)  

    ## In a 'with' block, open the 'temp_file' for writing as object 'outfile'.
    ## Call the 'write' method of 'outfile' to write merged_yml into it.
    ## when the 'with' block completes, the temp_file will be automatically closed().
    with open(temp_file, 'w') as outfile:
        outfile.write(json.dumps(merged_yml))

    ## This yml_files_to_json_file(yml_files, prefix='') function with arguments returns the absolute pathname of the
    ## temporary file when called by another function.
    return temp_file

## This defines function is_opa_allowed(input_file, policy_data_file, rego_file, package, args).
def is_opa_allowed(input_file, policy_data_file, rego_file, package, args):
    """
    Runs OPA evaluation with given data, parses and interprets result

    ## This function generates CLI command arguments to be sent the opa program.  Then it
    ## creates a child process to execute opa with the given arguments.
    ## It receives the output of opa, and places it in an object called 'result'.
    """
    ## Generate augment list for an opa command.  The format() function here does no formatting aleration
    ## of 'package', but simply inserts it into the 'data.{}' placeholder.
    arg_list = [args.opa_binary, 'eval', '-i', input_file, '-d', policy_data_file,
                '-d', rego_file, "data.{}".format(package)]

    ## Execute the opa command, supplying the argument list to it, and obtaining the output of opa.
    result = subprocess.run(' '.join(arg_list),
                            shell=True, stdout=subprocess.PIPE)

    ## If 'result.returncode' is True
    if result.returncode:
        ## Instruct the Python logger to generate and handle an error message string.
        ## Here, the format() function does no formatting alteration of the returncode.  It simply inserts it
        ## into the new string, positioned to overwrite the {} placeholder.
        logger.error("Process exited with code {}".format(result.returncode))

    ## If 'result.returncode' equals 0:
    if result.returncode == 0:
        ## Instruct the Python logger to generate and handle an information (INFO) level message.
        ## The format() function input decodes the stdout BYTES of the opa command to a 'utf-8' standard string, so the logger can use the 
        ## data as a string.  Format places the output into the string at the {} placeholder location.
        logger.info("OPA evaluation compeleted\nResult set. START\n{}\nResult set. END".format(result.stdout.decode('utf-8')))

        ## This is try/except code block with no 'finally' clause specified.
        try:
            ## - Use the json module to 'loads' the 'result.stdout' BYTE stream into 'r_parsed'.
            r_parsed = json.loads(result.stdout)

            #todo: make sure that parsing is reliable
            ## traverse 'r_parsed' to grab the value of 'allow' element and store it in 'allowed'.
            allowed = r_parsed['result'][0]['expressions'][0]['value']['allow']

            ## return from the function if this code is reached.
            ## This return provides two variables, (allowed and r_parsed) to the calling function.
            return allowed, r_parsed

        ## If the specific exception 'BaseException' is encountered in the 'try' block above:
        except BaseException:
            ## Tell the Python logger to generate and handle an ERROR level message with the following string.
            logger.error("Failed to parse result set!")

            ##  Return from the function here, if this code is reached.  Here, the {} creates an empty dictionary.
            ##  Two values (False and an empty dictionary) are returned.
            return False, {}

    ## Else (result.returncode does not equal 0)
    else:
        ## Tell the Python logger to generate and handle an ERROR level message with the given string below.
        ## The format function places the value of 'result.stderr' into the string at the replacement text
        ## positional placeholder {} location.
        logger.error("OPA evaluation failed!{}".format(result.stderr))

        ## retun a tuple containing 2 objects (False, and an empty dictionary), if this point in the code is reached.
        return False, {}


## This defines function process_opa(processed_yml, args).
def process_opa(processed_yml, args):
    """
    Process OPA on temp file
    """
    ## With given 'processed_yml' path, call function yml_files_to_json_file() that is defined in this program.
    ## it returns the path to the input_data_file path containing merged yaml data.
    input_data_file = yml_files_to_json_file(
        yml_files=[processed_yml], prefix="input_")
    
    return_tuples = []  ## Initialize an empty list.
    project_return_status = True  ## Initialize a boolean and set it to True.

    ## In a 'with' code block, open the file specified as 'args.suite' as an object named 'suite_f'.
    ##        - Read the yaml data from 'suite_f' and transform into variable 'suites'.
    ##            - Note that: yaml.SafeLoader is a form of security protection against malicious 
    ##              yaml files from an untrustworthy source.
    ##        - Loop through 'suites' object 'policies' getting each as 'item':
    ##            - If item['active'] is true:
    ##                - Initialize variable policy_yml_files with contents of item['policyDataFiles']
    ##                - Initialize variable policy_data_files with data returned from function yml_files_to_json_file().
    ##                - Initialize variable rego_file with contents of item["policyRegoFile"]
    ##                - Initialize variable package with contents of item["package"]
    ##                - Initialize and set 'allowed' and result with data returned from is_opa_allowed() that is 
    ##                  defined in this program.
    ##                - If 'allowed' is False
    ##                    - set project_return_status to False
    ##                - append to 'retun_tuples list, the two values (allowed and result).
    ##                - In a try/except code construct with no finally cause, attempt to remove the temporary policy 
    ##                  data file.  If an exception is encountered, just call 'pass' to ignore the exception.
    ##        - The file will be closed when 'with' block execution has concluded.
    ##
    ##      - If the return_tuples variable contains data:
    ##            - this function will return: 'project_return_status' and 'return_tuples'
    ##      - In the event that return_tuples variable did not contain data:
    ##            - this function will return: (True, None).   The Python keyword None indicates a Null value.
    ##
    with open(args.suite) as suite_f:
        suites = yaml.load(suite_f, Loader=yaml.SafeLoader)
        return_tuples = []
        for item in suites["policies"]:
            if item['active']:
                #load policy data
                policy_yml_files = item['policyDataFiles']
                policy_data_file = yml_files_to_json_file(
                    yml_files=policy_yml_files,
                    prefix="policy_"
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

def main():  ## This defines the main() function.
    """
    Main entry point
    ## The Python interpreter reads and executes this code beginning at the top of the file, but 
    ## in this file those instructions were to import code, and then define variables such as strings,
    ## objects and functions.
    ## When this function, main() is called at the bottom of this file, then main() becomes the 'main' body
    ## of code that in general uses the other functions and variables defined elsewhere in this code or in
    ## code that has been imported.
    """

    # Import Args
    ## The following code uses the argparse module to define command input arguments, and help messages.
    ## help messages can be viewed by executing this code as a command with '--help' specified.
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store', dest='input', help='Folder containing each of the projects.')
    parser.add_argument('--suite_definition', action='store', dest='suite',
                        help='File defining policy suite definition')
    parser.add_argument('--log_file', action='store', dest='log_file', help='Log file')
    parser.add_argument('--report_file', action='store', dest='report_file', help='Report file')
    parser.add_argument('--opa_binary', action='store', dest='opa_binary', help='OPA binary')
    args = parser.parse_args()



    # init logging
    ## Python logging creates a hierarch of loggers that have parent/child relationships. The highest level
    ## logger parent is named 'root'.  The logger object configured below is called '__main__'.  Child loggers
    ## by default propagate their logging records to their parent, unless logger.propagate is set to False.
    logger.propagate = False  # do not log to console

    ##  This creates a log output formatting object that would output 'timestamp log_message_level: log_message'. 
    fmt = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')  

    ## This is try/except code block with no 'finally' clause specified.  The code block will attempt to:
    ##    -  define a logging handler that knows how to write to file(s). 
    ##    -  tell the logging handler to use the given log formatter
    ##    -  set the logger output message severity threshold level to Debug. Less severe messages will not be emitted.
    ##    -  then the new handler is added to this logger.
    ## If any of the attempted code throws the SPECIFIC exception 'IOError', it jumps straight to the except clause below, 
    ## where it 'prints' a warning message that includes the generated 'error' string to the command's standard output. 
    try:
        log_handler = logging.FileHandler('{}'.format(args.log_file), mode='a')
        log_handler.setFormatter(fmt)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_handler)
    except IOError as error:
        print("Warning: unable to set file handler for logger {}".format(str(error)))

    ## This creates a 'report_f' object that opens the given 'report_file' in 'a+' mode.  The a+ mode means to
    ## create a new file, if it doesn't already exist for reading and writing, but position the file pointer
    ## to the end of the file for appended writing.
    report_f = open(args.report_file, 'a+') #Unique

    ## Initialize two empty lists
    project_paths = []
    project_list = []


    ## This for loop iterates through the elements (directories, perhaps files) of the project directory specified by '--input'.
    ## It uses os.scandir, so it knows the filesystem attributes of the elements found within a directory.
    for project in os.scandir(args.input):

        ## if the entry is found to be a filesystem directory 
        ##     - append the name of the directory to project_list
        ##     - concatenate project path with '/processed_values.yml', and append it to project_paths.
        if project.is_dir():  
            project_list.append(project.path.split('/')[-1:])  ## split path into a list, and get only last element.
            project_paths.append(project.path + '/processed_values.yml')  ## concatenate two strings


    ## An iterable is an object that can be used as a sequence by a loop.
    ## Here, 'reports' is an iterable that contains a group of objects that each map
    ## a set of arguments to be sent to 'process_opa'.
    ## Within reports:
    ##     For each 'item' in 'project_paths' an iterable is created that maps
    ##        the function 'process_opa' to that 'item', along with the full set of args given.
    ## When reports is eventually used by a loop, process_opa() will be executed with its arguments
    ## during each loop iteration. 
    reports = map(process_opa, project_paths, repeat(args))

    #Writes Report File

    ## Initialize empty lists.
    allowed_projects = []  	## A list to contain allowed projects.
    denied_reports = []  	## A list to contain denied reports.
    policies = []  			## A list to contain policies.

    ## Initialize more variables
    policies_found = False
    i = 0  ## Used in the following for loop to count the number of times the loop is executed.

    ## Loop through the 'reports' object getting each 'report' one at a time.
    ##     Take the output of function 'writeout_report()', and put it into:
    ##         variables:  current_report, warning, result_allowed 
    ##     Record projects that are allowed, and reports that are denied in the appropriate lists.
    ##         - If a result is not allowed, add it to denied_reports.
    ##         - If a report has a warning, record that the report is denied, but append the project to allowed_projects.
    ##         - If a report is not denied and has no warning, add it to allowed_projects.
    ##              - Then, if the policies have not yet been recorded, extract all of them from 'report[1]'.
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

    allowed_projects_num = len(allowed_projects)  ## Length of allowed_projects is used to count them.
    projects_num = len(project_list)  ## Length of project_list is used to count them.

    ## If projects_num is greater than 1:
    ##     - write to file report_f.  The format is:
    ##         '********* allowed_projects_num/projects_num Projects Allowed *********\n'  
    ##     - If allowed_projects is greater than 0:
    ##         - write 'Project(s) Allowed --> \n' to report_f.  The \n is a newline 
    ##         - while keeping count loop through allowed_projects list strings one at a time.
    ##             - Write a newline every 4th time, or if the last item in allowed_projects was written.
    ##             - If neither of the above line is true, then:
    ##                   - calculate 31 minus the length of the current allowed_projects string,
    ##                     and use that number as a multipler of ' ' space characters.  
    ##                   - Then write a comma followed by those space characters to report_f. like: ",           ". 
    ## Else If allowed_projects_num is equal to 1:
    ##     Taking the first object from project_list, (which I think is always a string):
    ##         take each character from that single string, and join them together as a single string. 
    ##         This looks like the programmer had an issue, where some code checker couldn't see a guarantee that
    ##         project_list contains strings, so they used join as a way to force it to look like a string.
    ##         With that SINGLE_STRING created by join: 
    ##             write:    "********* One Project Change: SINGLE_STRING --> Allowed *********\n" to report_f.
    ##             Note that the \n at the end is a newline.
    ## Else if neither of the two main clauses above were true, then:
    ##             write:    "********* One Project Change: SINGLE_STRING --> Not Allowed *********\n" to report_f.
    ##        
    ##        
    ##        
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


    ## loop through the denied reports one at a time, writing the contents to report_f
    for report in denied_reports:
        for line in report:
            report_f.write(line)

    ## If allowed_projects_num is equal to projects_num:
    ##     If denied reports is 0:
    ##         - write ">>> OVERALL POLICY DETAILS <<<\n" to report_f.
    ##         - loop through 'policies' one at a time getting a POLICY.
    ##             - write into report_f, creating a right justified left padded string with a width of
    ##               80 minus the lenth of the policy variable, like:
    ##                 "                                           POLICY --> Allowed: True\n"
    ##         - Exit from the program with a return code of 0.  0 generally means execution was successful.
    ## Exit from the program with a return code of 1, which generally means something was not as desired during execution.
    if allowed_projects_num == projects_num:
        if len(denied_reports) == 0:
            report_f.write(">>> OVERALL POLICY DETAILS <<<\n")
            for policy in policies:
                report_f.write(policy + " --> Allowed: True\n".rjust(80-len(policy)))

        sys.exit(0)
    sys.exit(1)


## If the program is executed as a script, the following call to main() will be executed.
## Otherwise, if some other Python program imports this code, then main() will not be executed.
if __name__ == "__main__":
    main()