Repo containing code for linting jobs, here is the list of Jenkins methods and their details:
------------

- ansibleLinter()             - Ansible linting tests
- configValidation()          - Config validation check
- cerberusSchemaFileLinter(String _schemaFolder_) - Cerberus Schema Files linter
- declarativePipelineLinter() - Declarative Pipeline linter
- goBuild()                   - Go build tests
- goFmt()                     - Go format tests
- goLint()                    - Go lint tests
- goTest()                    - Go test
- goVet()                     - Go vet tests
- ingressChecker()            - Ingress rules check
- InSpecTest()                - InSpec tests
- PylintTest(String _pythonVersion_="2") - Pylint tests
- rubocopTest()               - Rubocop tests
- schemaValidation(String schemasRepo, String schemasRootDir) - Yaml files validation against schemas
- shellTest()                 - Shell tests
- yamlLinter()                - Yaml linter
- yamlRender()                - Yaml Render linter

Ansible linting tests
=========
content to be added ...

Config validation check
=========


configValidation() uses an Ansible role named [openshift-resources-jinja-processing](https://github.doms.com/Ansible/openshift-resources-jinja-processing) to validate if the [ansible-role-openshift-provision](https://github.com/domsTechnology/ansible-role-openshift-provision) role (used e.g. during cluster deployment) can proceed successfully with a given config. It processes the config the way the [ansible-role-openshift-provision](https://github.com/domsTechnology/ansible-role-openshift-provision) does. Additionally it does Yaml linting for dumped config files, validating Prometheus rules, Alertmanager configs and running ProductionChangeCheck.

Trigger file example
------------
[Jenkinsfile.dumpCheck](https://github.doms.com/xPaaS-Operations/openshift-cluster-config/blob/master/Jenkinsfile.dumpCheck)

Requirements
------------

Following files must exist in a repo that is being checked:
- validate-config.yml - a playbook that calls openshift-resources-jinja-processing role and defines all the variables that are validated i.e.
    - variables used in a process of templating the resources (including mock dynamic variables)
    - [openshift_cluster](https://github.com/domsTechnology/ansible-role-openshift-provision/#openshift_clusters)
    - [openshift_resource_path](https://github.com/domsTechnology/ansible-role-openshift-provision/#role-variables)
- exclusions.txt - a one-line file containing a regex that describes names of clusters which this check should not be run against

These files must be placed in [repo main direcotry]/tests/config-validation directory.

Dependencies
------------

- [openshift-resources-jinja-processing](https://github.doms.com/Ansible/openshift-resources-jinja-processing) Ansible role

Example of use (from the [xPaaS-Operations/openshift-cluster-config](https://github.doms.com/xPaaS-Operations/openshift-cluster-config) repo)
------------

[validate-config.yml playbook](https://github.doms.com/xPaaS-Operations/openshift-cluster-config/blob/master/tests/config-validation/validate-config.yml)

Schema Validation
=========
Schema Validation check uses [Cerberus](https://pypi.org/project/Cerberus/) Python module to check files structure against provided schemas. It requires two arguments:
- String _schemasRepo_ - url to repository in which schemas used in the check are defined
- String _schemasRootDir_ - path to the schemas directory in schemasRepo

The check looks first for manifest files in the directory/repo in which it runes. Then runs Python3 script with Cerberus validation for each manifest file against all the yamls specified in it.

Manifest file should be written in json format and should have structure like the following:

```json
{
  "items": [
    {
      "input_yml_file": "<relative path (from current directory) to the yml file to check>",
      "schema_file": "<relative path (from schemasRepo/schemasRootDir/) to a corresponding schema file>"
    },
    {
      "input_yml_file": "...",
      "schema_file": "..."
    }
  ]
}
```

The check succeeds if all validations of the yaml_file<->schema pairs defined in each manifest end in success. Fails otherwise.

Requirements
------------
[Cerberus](https://pypi.org/project/Cerberus/)>=1.3


Cerberus Schema Files linter
=========
This linter ensures that yaml files in specified folder and its subfolders are valid cerberus schemas. The linter only attempts to validate files with **yml** or **yaml** extension. Linter prints progress to stdout and errors to stderror. Linting finishes with non zero exit code if any of files fail to be valid Cerberus schemas.
**resources/cerberus_schema_linter_requirements.txt** specifies which version of cerberus module is used for validation



Example of output:
```
+ python script.py schemas
*** VALIDATION FAILED ***
>>>>>> schemas/sub_dir/sub-sub-dir/bad_schema.yml is INVALID Cerberus schema: {'iamPolicyMembers': [{'schemas': ['unknown rule']}]}
>>>>>> schemas/sub_dir/sub-sub-dir/hello_kitty.Yml: INVALID YAML: while scanning for the next token
found character '\t' that cannot start any token
  in "schemas/sub_dir/sub-sub-dir/hello_kitty.Yml", line 2, column 1
Validating schemas/project_schema.yml
Validating schemas/pub-sub-subscriptions_schema.yml
Validating schemas/sub_dir/iam-policy-members_schema.Yml
Validating schemas/sub_dir/storage-buckets_schema.yaml
Validating schemas/sub_dir/sub-sub-dir/bad_schema.yml
Validating schemas/sub_dir/sub-sub-dir/hello_kitty.Yml
script returned exit code 1
```

Declarative Pipeline linter
=========
content to be added ...

Go build tests
=========
content to be added ...

Go format tests
=========
content to be added ...

Go lint tests
=========
content to be added ...

Go test
=========
content to be added ...

Go vet tests
=========
content to be added ...

Ingress rules check
=========
content to be added ...

InSpec tests
=========
content to be added ...

Pylint tests
=========
content to be added ...

Rubocop tests
=========
content to be added ...

Shell tests
=========
content to be added ...

Yaml linter
=========
content to be added ...

Yaml Render linter
=========
content to be added ...
