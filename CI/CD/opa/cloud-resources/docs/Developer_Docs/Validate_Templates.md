# How to Test Template Modification/Additions/Deletions

1. Install ansible.
2. Navigate to the cloud-resources repo.
3. Run the following command, where **project_name** is the name of the project in question.

```bash
ansible-playbook resource_dump.yml -e project_name=*project_name*
```

This will initiate a test run of all the templates in the template repo to determine their success or failure in parsing a specific projects configuration data. This is helpful when templates are modified or added.

The result of this run will be a folder inside your cloud-resources repo named: cr-output. This folder contains the files that will be used by Eunomia to create the custom resources in our GKE cluster. These are temporary files and will be overwritten if you run the playbook again.