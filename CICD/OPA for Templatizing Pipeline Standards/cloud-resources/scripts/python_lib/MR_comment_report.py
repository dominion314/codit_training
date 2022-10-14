import argparse
from merge_messages import CommentPrint
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('--token')
parser.add_argument('--project_id')
parser.add_argument('--merge_request_id')
parser.add_argument('--report')
parser.add_argument('--error_codes')

args = parser.parse_args()
temp_comment = 'Pipeline processing...'

if args.project_id == "" or args.project_id is None:
    print("Project_id argument is missing or blank, unable to run comment script.")
    exit()
if args.merge_request_id == "" or args.merge_request_id is None:
    print("Merge_request_id argument is missing or blank, unable to run comment script.")
    exit()
if args.token == "" or args.token is None:
    print("Token argument is missing or blank, unable to run comment script.")
    exit()
if args.report == "" or args.report is None:
    print("Report argument is missing or blank, unable to run comment script.")
    exit()
if args.error_codes == "" or args.error_codes is None:
    print("Error_codes argument is missing or blank, unable to run comment script.")
    exit()

run_kind = ""
error_codes = []
if 'schema_report.txt' in args.report: # Then it is a Schema report file.
    run_kind = "Cerberus"
    try:
        with open(args.report, 'r') as report_file:
            prev_line=''
            for line in report_file:
                if 'ERROR' in line:
                    if '[a-zA-Z0-9_]{5,1024}' in line:
                        error_codes.append(["Cerberus-102",prev_line,line])
                    elif '^[0-9a-z-]+' in line:
                        error_codes.append(["Cerberus-104",prev_line,line])
                    elif '.*@commonmerit\.com|.*@qa\.commonmerit\.com|.*@dev\.commonmerit\.com' in line:
                        error_codes.append(["Cerberus-106",prev_line,line])
                    elif '.*@.*\.gserviceaccount\.com' in line:
                        error_codes.append(["Cerberus-108",prev_line,line])
                    elif '[a-z]([-a-z0-9]*[a-z0-9])?' in line:
                        error_codes.append(["Cerberus-110",prev_line,line])
                    elif '^[0-9a-z-_]+' in line:
                        error_codes.append(["Cerberus-112",prev_line,line])
                    elif '^[a-z][a-zA-Z0-9-]{5,29}$' in line:
                        error_codes.append(["Cerberus-114",prev_line,line])
                    elif '^\d+(.?\d?\d?)s$' in line:
                        error_codes.append(["Cerberus-116",prev_line,line])
                    elif '^[0-9a-z-]{6,30}$' in line:
                        error_codes.append(["Cerberus-118",prev_line,line])
                    elif '^[ 0-9a-zA-Z-\/\.]{1,100}$' in line:
                        error_codes.append(["Cerberus-120",prev_line,line])
                    elif '^[ 0-9a-zA-Z-\.\,]{1,256}$' in line:
                        error_codes.append(["Cerberus-122",prev_line,line])
                    elif '[-a-z0-9\._]+' in line:
                        error_codes.append(["Cerberus-124",prev_line,line])
                    elif '.*@commonmerit\.com|.*@qa\.commonmerit\.com|.*@dev\.commonmerit\.com|.*\.gserviceaccount\.com' in line:
                        error_codes.append(["Cerberus-126",prev_line,line])
                    elif '^(19|20|21)\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])' in line:
                        error_codes.append(["Cerberus-128",prev_line,line])
                    elif '\d+' in line:
                        error_codes.append(["Cerberus-130",prev_line,line])
                    elif '^[a-z][a-z0-9]+-(nx|xpn)-(lle|hle|prd|ops|sbx|transit)$' in line:
                        error_codes.append(["Cerberus-132",prev_line,line])
                    elif '^[a-z][a-z0-9]+-(nx|xpn)-(lle|hle|prd|ops|sbx|transit)-((c|e)\d)-gcp-rtr[0-9]{2}$' in line:
                        error_codes.append("Cerberus-134")
                    elif '^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))$' in line:
                        error_codes.append("Cerberus-136")
                    elif '^[a-z][a-z0-9]+-(nx|xpn)-(lle|hle|prd|ops|sbx|transit)-([a-z0-9-]{0,10})?((c|e)\d)-nat-gateway$' in line:
                        error_codes.append("Cerberus-138")
                    elif '^[a-z][a-z0-9]+-(nx|xpn)-(lle|hle|prd|ops|sbx|transit)-((c|e)\d)-totransit(-\d\d)?$' in line:
                        error_codes.append("Cerberus-140")
                    elif '(169\.254\.)((([0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}|2[0-4][0-9]|25[0-4])[.])(([0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}|2[0-4][0-9]|25[0-5])))/30$' in line:
                        error_codes.append("Cerberus-142")
                    elif '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))?$' in line:
                        error_codes.append("Cerberus-144")
                    elif '^(((6553[0-5]|655[0-2]\d|65[0-4]\d\d|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0))-)?((6553[0-5]|655[0-2]\d|65[0-4]\d\d|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0))$' in line:
                        error_codes.append("Cerberus-146")
                    elif '\.([a-z0-9]+\.)*[a-z0-9]+\.[a-z]+' in line:
                        error_codes.append("Cerberus-148")
                    elif '([a-z0-9-]{5,50})' in line:
                        error_codes.append(["Cerberus-150",prev_line,line])
                    elif 'unknown field' in line:
                        error_codes.append(["Cerberus-200",prev_line,line])
                    else:
                        error_codes.append(["Cerberus-250",prev_line,line])
                prev_line = line
    except FileNotFoundError as try_error:
        print("Error FileNotFoundError for the Cerberus report file, exiting script...", try_error)
        exit()

elif 'report.txt' in args.report: # Then it is an OPA report file.
    run_kind = "OPA"
    try:
        with open(args.report, 'r') as report_file:
            last_line = ''
            for line in report_file:
                if 'Denied' in line:
                    if 'Service Apis' in line:
                        error_codes.append(["OPA-5000", line.split("---->")[-1]])
                    elif 'User Roles' in line:
                        if 'custom.iam.roles' in last_line:
                            error_codes.append(["OPA-7000", line.split("---->")[-1]])
                        else:
                            error_codes.append(["OPA-6000", line.split("---->")[-1]])
                    elif 'Group Roles' in line:
                        if 'custom.iam.roles' in last_line:
                            error_codes.append(["OPA-7010", line.split("---->")[-1]])
                        else:
                            error_codes.append(["OPA-6010", line.split("---->")[-1]])
                    elif 'Service Account Roles' in line:
                        if 'custom.iam.roles' in last_line:
                            error_codes.append(["OPA-7020", line.split("---->")[-1]])
                        else:
                            error_codes.append(["OPA-6020", line.split("---->")[-1]])
                    elif 'Environment Type with FolderID, Allowed' in line:
                        error_codes.append("OPA-8000")
                    elif 'Environment Type with FolderID and Product Domain' in line:
                        error_codes.append("OPA-8010")
                    elif 'Billing Department ID' in line:
                        error_codes.append("OPA-8020")
                    elif 'Missing All Required Role' in line:
                        error_codes.append("OPA-9000")
                    last_line = line
                elif 'Validating Policies' in line:
                    error_codes.append(line)
    except FileNotFoundError as try_error:
        print("Error FileNotFoundError for the OPA report file, exiting script...", try_error)
        exit()

if len(error_codes) > 0:
    try:
        with open(args.error_codes, 'r') as error_codes_file:
            error_codes_yaml = yaml.safe_load(error_codes_file)
            mr_comment = CommentPrint(args.token, args.merge_request_id, args.project_id)
            mr_comment.write_to_comment("### "+ run_kind + " Run:  ")
            for error_code in error_codes:
                try:
                    if run_kind == "Cerberus": #Cerberus
                        tip = error_codes_yaml[run_kind][error_code[0]] + '\n'
                        cerb_body = """
Cerberus Fail Path:<BR>
{}<BR>
**{}**<BR>
{}<BR>
""".format(error_code[1].strip().replace('@','@&#x200B;'),error_code[2].strip(),tip)
                        mr_comment.write_to_comment(cerb_body)
                    elif run_kind == "OPA": #OPA
                        if 'Validating Policies' in error_code:
                            project_name = error_code.split(' ')[5]
                            project_body ="""
{}
""".format("The Following Errors for Project " + project_name + ":")
                            mr_comment.write_to_comment(project_body)
                        elif isinstance(error_code, list):
                            tip = error_codes_yaml[run_kind][error_code[0]].replace(" ~item(s)~ ",
                                error_code[1]).split(' ~split~ ')
                            opa_body ="""
**{}**<BR>
{}<BR>
""".format(tip[0], tip[1])
                            mr_comment.write_to_comment(opa_body)
                        else:
                            tip = error_codes_yaml[run_kind][error_code].split(' ~split~ ')
                            opa_body ="""
**{}**<BR>
{}<BR>
""".format(tip[0], tip[1])
                            mr_comment.write_to_comment(opa_body)
                except ValueError:
                    print("Error unable to find error listed for given error code:", error_code)
    except FileNotFoundError as try_error:
        print("Error FileNotFoundError for the error codes file, exiting script...", try_error)
        exit()
