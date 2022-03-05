'''
Created on November 2020

@author: dominickhernandez
'''
   
from pprint import pprint  
##  useful to 'pretty print, or pretty format' data-structures, that are nested or not.
import json, os     ## module for JSON data encoding and decoding.
from string import Template
## This is useful for modifying code using '$' prefixes for variables when constructing a new string from a given string.
import uuid         ## module to generate random unique id's.
import argparse  	## module to get command arguments from the user.
import ipaddress  	## module with many methods to create and control IPV4/IPv6 addresses and networks.

## Create banner upon execution.
banner = """ 
     ___        __  ___ ___ __     __  __  __   _____ 
|\ ||__ |  |   |__)|__ |__ |__)   /__`/  `|__)||__)|  
| \||___|/\|   |   |___|___|  \   .__/\__,|  \||   |  
                                                      

"""

Dependency = [
    'colorama',
    'gitpython',
    'netaddr',
    'python_terraform',
    'termcolor',
    ]
## Dependency is a list of strings based on the modules needed to run this program.

try: 

    from python_terraform import * ## A module to call the 'terraform' command.
    from termcolor import colored  ## A module for ANSII Color formatting output for terminals of specific type based on shell exported $TERM  
    from git import Repo           ## Modules to interact with git repos.
    from netaddr import IPNetwork  ## Modules to manipulate IPv4/IPv6 networks.
    import colorama                ## Makes ANSI escape character sequences for producing colored terminal text.

except ImportError:
   
    print()
    print('Install the following dependencies and try again:', 'red')
    print('sudo pip3 install -t /opt/python3/lib/python3.7/site-packages/')  ## Tells the user what to install:

    for dep in Dependency: 
        print('- ' + dep)
        
    exit()

colorama.init()  ## Initialize colorama.


class Arguments(object):
    """
    Used for Arguments from the command line (--help gives usage).
    """

    def __init__(self, description=''):
        """
        Default arguments for any job
        """

        self._parser = argparse.ArgumentParser(description=description)


        self._parser.add_argument('-c',
                                  dest='cloud',
                                  default='',
                                  help='Cloud Environment')  ## create 'cloud' variable referenced later args.cloud .
        self._parser.add_argument('-r',
                                  dest='region',
                                  default='',
                                  help='Cloud Region')       ## create 'region' variable referenced later args.region .
        self._parser.add_argument('-cs',
                                  dest='cloud_secret',
                                  default='',
                                  help='Cloud Secret')       ## create 'cloud_secret' variable referenced later args.cloud_secret .
        self._parser.add_argument('-a',
                                  dest='app',
                                  default='',
                                  help='Application')        ## create 'app' variable referenced later args.app .
        self._parser.add_argument('-i',
                                  dest='ins',
                                  default='',
                                  help='Instance')           ## create 'ins' variable referenced later args.ins .
        self._parser.add_argument('-p', 
                                  dest='id',
                                  default='',
                                  help='Peer Identify')      ## create 'id' variable referenced later args.id .
        self._parser.add_argument('-s', 
                                  dest='subnet',
                                  default='',
                                  help='Peer Subnet')        ## create 'subnet' variable referenced later args.subnet .

    def get(self, access='read'):
        """
        Get the arguments and verify them
        """
        self._args = self._parser.parse_args() 


        return self._args  

def logger(color):
    """Log results"""
    def _logger(header, data, *args):
        if isinstance(data, dict) or isinstance(data, list):
            print(colored('\n[%s]\n' % header, color), pformat(data))
        elif isinstance(data, str):
            print(colored('[%s]' % header, color), data, *args)

    return _logger  ## This returns a unique wrapped function '_logger' to code that calls this.


log_i = logger('green')  
log_w = logger('yellow')  
log_e = logger('red')    


env = {
    'aws': {
        'us-east-1': '',
        'us-east-2': '',
        'us-west-2': '',
},
    'azure': {
        # 'Region'  : 'Vnet NextHop'
        'central-us': '10.116.0.68',
    }
}


sname = {
    # Cloud
    'aws': 'aws',
    'azure': 'az',
    # Region
    'us-east-1': 'ue1',
    'us-east-2': 'ue2',
    'us-west-2': 'uw2',
    'central-us': 'cus',
}


def yesno_query(ask, error):
    '''
    Query that will cancel script at no
    '''
    loop = True  ## Initialize boolian 'loop' as True.

    ##  While 'loop' remains True, keep executing this 'while' code block.
    while loop:	

        a = input(ask).lower()

        ## if 'a' is 'yes' or 'y':
        if a == 'yes' or a == 'y':
            loop = False  
 
        ## if 'a' is 'no' or 'n':
        if a == 'no' or a == 'n':
            print()  

            log_e('Manual Exit', error)

            exit()  


def not_option_query(ask, options):
    '''
    Query to make sure Answer is unique to option list
    '''
    loop = True  ## Initialize boolian 'loop' as True.

    while loop:

 
        a = input(ask).lower()


        if a != '' and a not in options:
            answer = a  
            loop = False  


        if loop == True:
            print()  ## print a newline with no visible text.

            log_e('Unknown Response', 'Instance should be unique from below list')

            for o in sorted(options):
                print('- ' + o)  
            print()  

    return answer  ## return the 'answer' string to the caller.


def not_option_verify(info, options, arg, ask):
    '''
    Validate Argument is unique to option list
    If false, user will be prompted via "not_option_query"
    '''

    if info != '' and info in options:
        log_e(arg, 'Argument invalid')

        return not_option_query(ask, options)

    if info == '':
        return not_option_query(ask, options)

    else:
        return info 


def option_query(ask, options):
    '''
    Query to make sure Answer is in option list
    '''

    loop = True


    while loop:


        a = input(ask).lower()

        if a in options:
            answer = a
            loop = False

        if loop == True:
            print() 

            log_e('Unknown Response', 'Please choose from list below:')

            for o in sorted(options):
                print('- ' + o)  

            print()  ## print a blank line.

    return answer 

def option_verify(info, options, arg, ask):
    '''
    Validate Argument is in option list
    If false, user will be prompted via "option_query"
    '''
    if info != '' and info not in options:
        log_e(arg, 'Argument invalid')

    if info not in options:
        return option_query(ask, options)
    ## Else return the given 'info' to the caller
    else:
        return info 


def simple_query(ask):
    '''
    Query for raw answer
    No validation
    '''
    loop = True  


    while loop:
 
        answer = input(ask).lower()

        ## If answer is not empty, return it.
        if answer != '':
            return answer


def simple_verify(info, ask):
    '''
    Validate Argument is set
    If empty, user will be prompted via "simple_query"
    '''
    if info == '':
        return simple_query(ask)
    else:
        return info 


def identify_cloud(args, info):
    '''
    Identify Cloud Environment
    '''
    ask = 'Specify Cloud Environment: '  ## Initialize 'ask' string

    info['cloud'] = option_verify(info = args.cloud.lower(), 
                           options = env.keys(),
                           arg = '-c', 
                           ask = ask)


def identify_region(args, info):
    '''
    Identify Cloud Region
    '''
    ask = 'Specify Cloud Region: '  ## Initialize 'ask' string

    info['region'] = option_verify(info = args.region.lower(), 
                            options = env[info['cloud']].keys(),
                            arg = '-r', 
                            ask = ask)
    ## If info dictionary at ['cloud'] is equal to the string 'azure':
    if info['cloud'] == 'azure':

        info['next_hop'] = list(env[info['cloud']].values())[0]


def identify_cloud_secret(args, info):
    '''
    For Azure, ask for Cloud Secret
    '''
    ask = 'Specify '+colored(info['cloud'].upper(), "green")+' Secret: '
    if info['cloud'] == 'azure':
        secret = simple_verify(info = args.cloud_secret, 
                               ask = ask)
    else:
        secret = ''
    info['cloud_secret'] = secret


def existing_instances(app):
    '''
    Indentify existing instances 
    for specified Application
    '''
    ins = []  ## Initialize 'ins' to be an empty list

    for p in os.listdir():

        if app in p:
            ins.append(p.split("_")[3])
    return(ins)



def identify_name(args, info):
    '''
    Create Peer Name: <app>_<cloud>_<region>_<instance>_<unique_id>
    '''
    # cloud/region Short Name
    cloud = sname[info['cloud']]   
    region = sname[info['region']]


    if info['cloud'] == 'aws':                       
        info['state'] = cloud + '_' + region + '_tgw' 
    if info['cloud'] == 'azure':                       
        info['state'] = cloud + '_' + region + '_transit' 

    # identify Application
    ask = 'Specify Application: '  ## Create 'ask' string

    app = simple_verify(info = args.app.lower().strip(), ask = ask)

    # pulls list of all existing Instances for specified Application
    exist_ins = existing_instances(app+'_'+cloud+'_'+region)

    # identify App Instance and confirm it is unique for App
    ask = 'Specify Application Instance: '
    ins = not_option_verify(info = args.ins.lower().strip(), 
                        options = exist_ins,
                        arg = '-i', 
                        ask = ask)

    unique_id = str(uuid.uuid4().hex) 

    ## Initialize info{} at key 'peer_name' as formatted in 'f string' below.
    info['peer_name'] = f'{app}_{cloud}_{region}_{ins}_{unique_id}'


def get_info(opt):
    '''
    Pull Information from Static Peer List
    Pull Options:
        peer
        id
        subnet
    '''

    with open('peer_list.json', 'r') as f:
        r = []  ## Initialize 'r' as an empty list
        p = json.load(f)  

        for a, b in p.items():

            if opt == 'peer':
                r.append(a)  
                return(r)   

            r.append(b[opt])

        return(r) 


def identify_subnet(args, info):
    '''
    Identify Peer Subnet
    Confirms Peer Subnet is not already used
    '''
    ask = 'Specify Subnet: '  
    loop = True  
    subnet = not_option_verify(info = args.subnet.lower(), 
                options = get_info('subnet'),
                arg = '-s', 
                ask = ask)

    while loop:

        try:
            ipaddress.ip_network(subnet)
            loop = False
        except:  ## If any exception is encountered:

            log_e('Subnet Incorrect', 'Please provide valid Subnet.')


            subnet = not_option_query(ask, get_info('subnet')) 


        for s in get_info('subnet'):


            if IPNetwork(subnet).ip in IPNetwork(s):
  
                log_e('Subnet Overlap', f'{subnet} is part of {s}.')

                subnet = not_option_query(ask, get_info('subnet'))
                loop = True  

            else:
                continue        

    info['peer_subnet'] = subnet


def identify_peer(args, info):
    '''
    Identify Peer ID
    Confirms Peer ID is not already used
    '''
    ask = 'Specify Peer Identity: ' 


    id = not_option_verify(info = args.id.lower(), 
                        options = get_info('id'),
                        arg = '-p', 
                        ask = ask)

    info['peer_id'] = id


def identify(args, info):
    '''
    Identify Peer Information
    '''
    ## With 'args' and 'info' arguments, call the identify* functions.
    identify_cloud(args, info)
    identify_region(args, info)
    identify_cloud_secret(args, info)
    identify_name(args, info)
    identify_subnet(args, info)
    identify_peer(args, info)

    print()  ## print a blank line

    print(colored('[Peer Information]', 'green')) 


    for key, value in info.items():

        l = ['cloud', 'region', 'peer_name', 'peer_subnet', 'peer_id']


        if key in l:
     
            print(f'{key.title()}: {value}')  

    ask = '\nProceed with Above Information? '
    error = 'Rerun with correct information.'
    yesno_query(ask, error)  


def pull_template(info):
    '''
    Pull Terraform Template for AWS/Azure Peers
    '''

    with open('peer_templates/' + info['cloud'] + '_peer_LATEST', 'r') as f:

        t = Template(f.read())

        data = t.substitute(info)
           
        return data  


def create_peer_tf(info):
    '''
    Create New Peer Directory & Config File
    '''
    tf = pull_template(info) 
    name = info['peer_name']  
    if os.path.isdir(name):
        print()  ## print() a blank line


        log_e('Error', f'{name} Already Exists')

        print('\tPlease rerun with unique Peer Name')
        exit()  

    log_i('Info', f"Creating Terraform Config File for '{name}'")

    try:
        os.mkdir(name)
    except (OSError, PermissionError, IsADirectoryError) as e:
        log_e(f'Error: Could not directory {name} for Terraform Config file. Error: {e}')
        
        exit(0)  
     
    file = os.path.join(name, name + '.tf')

    try:
        with open(file, 'w') as f:
            f.write(tf)
    except (OSError, PermissionError, IsADirectoryError) as e:
        log_e(f'Error: Could not write Terraform Config file: {file}. Error: {e}')
        
        exit(0)  

    log_i('Info', "Terraform Config File Created")


def terraform(path, secret):
    '''
    Utilize Terraform to push new Peer Config
    '''

    tf = Terraform(working_dir=path)


    log_i('Terraform', "Initialize Configuration")
    print()  ## print() blank line.

    tf.init(capture_output=False)  

    log_i('Terraform', "Configuration Initialized") 


    input('\nPress '+colored("[ENTER]", "green")+' to Continue to Terraform Plan\n')
    log_i('Terraform', "Plan Configuration") 
    print() ## print blank line.

    tf.plan(capture_output=False, var={'client_secret':secret})

    log_i('Terraform', "Plan Complete")

    print(colored('\n***Confirm there are no errors on Terraform Plan***\n', 'yellow'))

    ask = 'Do you want to continue to Terraform Apply? '
    error = 'Terraform Config has been created but not applied'
    yesno_query(ask, error) 

    log_i('Terraform', "Apply Configuration") 
    print() ## print blank line.

    tf.apply(skip_plan=True, capture_output=False, var={'client_secret':secret})
    print() ## print blank line.

    log_i('Terraform', "Configuration Applied")


def add_info(peer, id, subnet):
    '''
    Add new Peer to Static Peer List
    '''

    with open('peer_list.json', 'r') as f:

        p = json.load(f)  

        p[peer] = {'id': id, 'subnet': subnet}  

    with open('peer_list.json', 'w') as f:
        json.dump(p, f) 

def update_permissions(peer):

    os.chmod(peer, 0o774)  

    for root, dirs, files in os.walk(peer):
        ## loop through the directory names.
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o774)  
        for f in files:
            os.chmod(os.path.join(root, f), 0o774)
def git(name):
    '''
    Stage New Peer and Peer_List
    Commit/Push Changes to External BitBucket
    '''

    input('\nPress '+colored("[ENTER]", "green")+' to Continue to update GIT\n')
    repo = Repo(os.getcwd())

    log_i('GIT', "Pre Status")

    print(repo.git.status()) 
    log_i('GIT', 'Staging New Peer')
    print(repo.git.add(name)+repo.git.add('peer_list.json'))
    log_i('GIT', "Post Status") 

    print(repo.git.status())
    print(colored('Confirm new Folder and File are ready to be committed', "yellow"))
    ask = '\nDo you want to Commit Changes? '
    error = 'Terraform Config has been applied but version control not updated'
    yesno_query(ask, error)

    log_i('GIT', 'Performing Commit')

    print(repo.git.commit(m="Cloud Peer '%s' Add" % name))
    print() ## print a blank line.
    log_i('GIT', 'Pushing to External BitBucket.  Enter Passphrase if needed.')
    print(repo.git.push())

def main(): 
    description = 'Create AWS/Azure Peering Utilizing Terrafrom'
    args = Arguments(description)
    args = args.get()
             
    info = {}  

    try:
        print(banner) 

        identify(args, info)
        create_peer_tf(info)
        terraform(path   = info['peer_name'],
                secret = info['cloud_secret'])            
        add_info(peer = info['peer_name'],
                id = info['peer_id'],
                subnet = info['peer_subnet'])
        update_permissions(info['peer_name'])
        git(name = info['peer_name'])

    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()
