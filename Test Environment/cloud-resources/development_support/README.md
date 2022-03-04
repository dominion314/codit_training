
## Makefile test guide
### Creation of workspace
To simplify development and tests of templates and inspec controls from your local machine you can use following makefile guide. 

0. Install inspec4.16, virtualenv, minikube, virtualbox, virtualenv

1. Create your test project by creating new catalog under test_vars/gcp_project called kohls-dev-**$LOB**-**$YOUR_NAME**-test-**$ENV**. example: kohls-dev-**cpa**-**rick**-test-**lle**.

2. Create project.yml file inside your catalog.

3. Create additional resource files like buckets.yml. 

4. Run export MY_PROJECT=kohls-dev-**$LOB**-**$YOUR_NAME**-test-**$ENV**`

Example: `export MY_PROJECT=kohls-dev-cpa-rick-test-lle`.

5. Pull this repo, go to the repo catalog.

**Note**: Make sure you have key.json which are credentials to cnrm service account in gcp dev space. key should be located in root of the repository. 

### Usage

To run minikube and install newest relase of kcc:

`make install`

To create pyenv and install python dependencies on it:

`make pythonenv`

Activate your virtual environment:

`source /tmp-virtualenv/bin/activate`

**Note:** if requironments were not installed in your env run: 

`pip install requironments.txt`

To initiate inspec profile:

`make inspec-profile`

define validation-manifest.yaml file on repo root directory. Example content:

```
--- 
artifacts:
    kcc_yaml_file: artifacts/kcc.yml
    combined_var_yaml_file: artifacts/input.yml
    combined_var_pdf_file: artifacts/input.pdf
inputVars: 
  - fileName: test_vars/gcp_project/kohls-dev-cpa-mateusz-test-lle/project.yml
    schema: schemas/vars/gcp_project/project.yml
  - fileName: test_vars/gcp_project/kohls-dev-cpa-mateusz-test-lle/storage-buckets.yml
  - fileName: test_vars/gcp_project/kohls-dev-cpa-mateusz-test-lle/service-accounts.yml
inspecControls: 
  - fileName: inspec/controls/StorageBuckets.rb
  - fileName: inspec/controls/IAMServiceAccounts.rb
kccJinjaTemplates: 
  - fileName: templates/gcp-project/storage-buckets.yml.j2
  - fileName: templates/gcp-project/iam-service-accounts.yml.j2
```

To render your parameter though templates locally **(not recommended)**:

`make render` 

**Recommended** way of rendering files is using Cloud Build: 

**Note:** if you don't have permissions to run following command means that you don't have permissions. Please contact maintaiiner of the repo. 

`gcloud config set project kohls-iaas-lle`

`make cbrender`

Annotate your KCC namespace with your GCP test project:

`make project`

To build resources in your project namespace:

`make build`

To check status: 

`make logs`

To run inspec control files: 

`make test`

To delete resorces and cleanup repo:

`make delete` or `make cbdelete` if render was made in Cloud Build **(recommended)**

## Example of initiating testing environment:

```
make install

export MY_PROJECT=kohls-dev-cpa-mateusz-test-lle

make project

make inspec-profile
```
## Example of performing test:

You are developing jinja template for storage buckets. You made some changes and want to test it. You modified folowing files:

```
inspec/controls/BiqQueryDataset.rb
templates/gcp-project/big-query-dataset.yml.j2
```

To test changes you created project folder, project definition and bucket definitions: 

```
test_vars/kohls-dev-cpa-mateusz-test-lle/project.yml
test_vars/kohls-dev-cpa-mateusz-test-lle/storage-buckets.yml
```

Now you want to validate if templates are rendering corectly. You define validation-manifest.yaml in repo root directory:

```
# validation-manifest.yaml
--- 
artifacts:
    kcc_yaml_file: artifacts/kcc.yml
    combined_var_yaml_file: artifacts/input.yml
    combined_var_pdf_file: artifacts/input.pdf
inputVars: 
  - fileName: test_vars/gcp_project/kohls-dev-cpa-mateusz-test-lle/project.yml
  - fileName: test_vars/gcp_project/kohls-dev-cpa-mateusz-test-lle/storage-buckets.yml
inspecControls: 
  - fileName: inspec/controls/StorageBuckets.rb
kccJinjaTemplates: 
  - fileName: templates/gcp-project/storage-buckets.yml.j2
```

- `make cbrender` to render your parameter against your template in Cloud Build

In the case of success in your workspace should appear 4 files which are ignored by git:
```
logs.txt                    #include logs of Cloud Build run 
artifact-manifest.json      #include url's to artifacts of build
render.yml                  #include rendered files for KCC
input.yml                   #include merged files for Insec
```

In case of failures you will be able to chekc the reason on logs of cloud build. 

Now build your resources in GCP space using KCC:

- `make build` to check if kcc is able to create your resource 

You should see output like this: 
```
kubectl apply -f render.yml
storagebucket.storage.cnrm.cloud.google.com/kohls-dev-cpa-mateusz-test-bucket-01 created
storagebucket.storage.cnrm.cloud.google.com/kohls-dev-cpa-mateusz-test-bucket-02 created
```

In case of issues or just to check if KCC is ok with your rendered file run:
- `make logs` to check recent kcc events from your namespace 

```
/bin/sh: /Users/msulek/repo/gitops/gcp-config/tmp-virtualenv/bin/activate: No such file or directory
kubectl get events --sort-by='.lastTimestamp' --namespace gcp-kohls-dev-cpa-mateusz-test-lle
LAST SEEN   TYPE      REASON         OBJECT                                               MESSAGE
81s         Normal    Updating       storagebucket/kohls-dev-cpa-mateusz-test-bucket-01   Update in progress
81s         Normal    Updating       storagebucket/kohls-dev-cpa-mateusz-test-bucket-02   Update in progress
79s         Normal    Deleting       computenetwork/demo2-vpc                             Deletion in progress
79s         Normal    UpToDate       storagebucket/kohls-dev-cpa-mateusz-test-bucket-01   The resource is up to date
79s         Normal    UpToDate       storagebucket/kohls-dev-cpa-mateusz-test-bucket-02   The resource is up to date
75s         Warning   DeleteFailed   computenetwork/demo2-vpc                             Delete call failed: error deleting resource: Error waiting for Deleting Network: The network resource 'projects/kohls-dev-cpa-mateusz-test-lle/global/networks/demo2-vpc' is already being used by 'projects/kohls-dev-cpa-mateusz-test-lle/regions/us-central1/subnetworks/demo2-vpc-subn-central1-prv01'
```

- `make test` to check if inspec test confirm that all resources from params has been built. (compare input.yml to actual GCP resources)

- `make cdelete` to cleanup you gcp project from test resources and cleanupp your working directory from build artifacts. 

**Note**: You don't have to make install/project/init every time you want to run tests. 

**Note**: You can alternatively use local build using `make build` and `make delete`