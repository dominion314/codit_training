# OPA based policy validation process

### Basic principles of Gitops eco-system:
- Infrastructure state (resourcess, access, configuration etc) is expressed in code
- Change in infrastructure state is Pull Request (PR) against config repository
- When PR is approved the configuration is reflected against live platform to bring it to desired state

### Challenges
- We must protect and assure data quality
- We must make sure that the right people are changing content
- We myst make sure that the right and required people are involved in PR approval process


### OPA helps solve these challenges through its policy suite of different checks
```
cloud-resources/opa/policy_suite.yml contains definitions of individual policies listed here:
policies:
# - name: "Cloud Connectivity"
# - name: "Egress Firewall rule checks"
# - name: "Ingress Firewall rule checks"
# - name: "Limit interconnect bandwidth"
# - name: "Only allow whitelisted Service APIs"
# - name: "Users, Groups and Service Accounts are only given allowed roles"
# - name: "Users, Groups and Service Accounts with Custom roles"
# - name: "Validates Project Configuration"
# - name: "Validates Big Query Datasets"
# - name: "VPC checks"
```

### Repos you will use:
cloud-resources
gcp-config
githook-yaml-lint

### Install and activate proper python environment
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r githook-yaml-lint/resources/opa_validation/requirements.txt 
```

### Download opa binary ( example is for OS-X)
```
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_darwin_amd64
chmod 755 opa
```

## Run validation
- Navigate to **opa** folder in template repo
```cd cloud-resources/opa/```

- Execute validation:
```
 python3 ../../githook-yaml-lint/resources/opa_validation/opa_linter.py  --opa_config=../../gcp-config/opa.yml --opa_binary=../../opa --opa_runner=../../githook-yaml-lint/resources/opa_validation/opa_run.py  --opa_suite_definition=./policy_suite.yml --log=./opa.log --report_file=./report.txt
```
- Check results:
```
cloud-resources/opa/opa.log
cloud-resource/opa/report.txt

To run the script again, delete the data not the file. Save the empty file and run the script again. 
```

