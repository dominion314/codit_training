# Getting started with Inspec for GCP

## inspec-gcp information:
This InSpec resource pack uses the native Google Cloud Platform (GCP) support in InSpec and provides the required resources to write tests for GCP.
### github page
https://github.com/inspec/inspec-gcp

### GCP resources supported by inspec-gcp 
https://github.com/inspec/inspec-gcp/tree/master/docs/resources

## Installing inspec on OS-X workstaton
### Prerequisites: 
#### Have GCP SDK Installed
Download the [SDK](https://cloud.google.com/sdk/docs/) and run the installation:
```
./google-cloud-sdk/install.sh
```

#### Have ruby installed using homebrew
```
brew install ruby
```
    
#### Optional: remove older inspec gems:
```
gem cleanup inspec
```

#### Install latest inspec gem, version 4.16.0 
The latest version of inspec, at the time of writing - 4.18, is broken against inspec-gcp pack:
https://github.com/inspec/inspec/issues/4562

```bash
$ gem install inspec -v 4.16.0
Fetching: inspec-4.16.0.gem (100%)
Successfully installed inspec-4.16.0
Parsing documentation for inspec-4.16.0
Installing ri documentation for inspec-4.16.0
Done installing documentation for inspec after 6 seconds
1 gem installed
$ gem install inspec-bin -v 4.16.0
Fetching: inspec-bin-4.16.0.gem (100%)
Successfully installed inspec-bin-4.16.0
Parsing documentation for inspec-bin-4.16.0
Installing ri documentation for inspec-bin-4.16.0
Done installing documentation for inspec-bin after 0 seconds
1 gem installed
$ gem list | grep inspec
inspec (4.16.0)
inspec-bin (4.16.0)
```

## Configure and validate inital profile

### Set proper service acccount in GOOGLE_APPLICATION_CREDENTIALS environmental variable
```bash
export GOOGLE_APPLICATION_CREDENTIALS=<your_service_account.json> 
```


### Run detect for transport gcp to validate that support is in place 

```
inspec detect -t gcp://

 ────────────────────────────── Platform Details ────────────────────────────── 

Name:      gcp
Families:  cloud, api
Release:   google-api-client-v0.23.9
```

### Initialise profile named gitops
```
$ inspec init profile --platform gcp gitops

 ─────────────────────────── InSpec Code Generator ─────────────────────────── 

Creating new profile at /Users/tkmam6x/PycharmProjects/yaml_validation/inspec/gitops
 • Creating directory libraries
 • Creating file README.md
 • Creating directory controls
 • Creating file controls/example.rb
 • Creating file inspec.yml
 • Creating file attributes.yml
 • Creating file libraries/.gitkeep
```


### Observe profile file. 
Note that depends.url is by default set to latest master from github
In case we do our own modifications to inspec resource pack we will change this 
setting in profile to point to proper URL or local tarball

```
$ cat gitops/inspec.yml 
name: gitops
title: GCP InSpec Profile
maintainer: The Authors
copyright: The Authors
copyright_email: you@example.com
license: Apache-2.0
summary: An InSpec Compliance Profile For GCP
version: 0.1.0
inspec_version: '>= 2.3.5'
attributes:
- name: gcp_project_id
  required: true
  description: 'The GCP project identifier.'
  type: string
depends:
- name: inspec-gcp
  url: https://github.com/inspec/inspec-gcp/archive/master.tar.gz
supports:
- platform: gcpIS-C02S621DG8WP:inspec tkmam6x$ 
```


## Prepare control specification by hand
### Remove requirements of attributes
 - Remove attributes.yml
 - Modify inspec.yml ( attributes element is empty )
 
```bash
name: gitops
title: GCP InSpec Profile
maintainer: The Authors
copyright: The Authors
copyright_email: you@example.com
license: Apache-2.0
summary: An InSpec Compliance Profile For GCP
version: 0.1.0
inspec_version: '>= 2.3.5'
depends:
- name: inspec-gcp
  url: https://github.com/inspec/inspec-gcp/archive/master.tar.gz
supports:
- platform: gcp
```

### Prepare and validate  'check if project exists' condition
- remove control/example.rb file
- create control/project_exists.rb file with the following content

```bash
# copyright: 2018, The Authors

title "Check if project exists"
project_id = 'doms-cpa-forseti-sbx'

# you add controls here
control "check if project exists" do
  impact 1.0
  title "Check if project exists"
  desc "An optional description..."
    describe google_compute_project_info(project: project_id) do
        it { should exist }
    end
end
```

### Execute against control file
execute the following command from profile folder:

```bash
IS-C02S621DG8WP:gitops tkmam6x$ inspec exec . -t gcp://

Profile: GCP InSpec Profile (gitops)
Version: 0.1.0
Target:  gcp://32555940559.apps.googleusercontent.com

  ✔  check if project exists: Check if project exists
     ✔  Compute Project Info doms-cpa-forseti-sbx should exist


Profile: Google Cloud Platform Resource Pack (inspec-gcp)
Version: 0.16.1
Target:  gcp://32555940559.apps.googleusercontent.com

     No tests executed.

Profile Summary: 1 successful control, 0 control failures, 0 controls skipped
Test Summary: 1 successful, 0 failures, 0 skipped
```

### Execute against control file, store outcome in JSON file
The result JSON file can be parsed to programatically determine which conditions passed and which ones failed
```bash
$inspec exec . -t gcp:// --reporter json:./result.json
```

result.json:
```json
{"platform":{"name":"gcp","release":"google-api-client-v0.23.9"},"profiles":[{"name":"gitops","version":"0.1.0","sha256":"60afcf72e3902760447c2c056d65426128e5f0a87b6ad150f67020eb5a250c50","title":"GCP InSpec Profile","maintainer":"The Authors","summary":"An InSpec Compliance Profile For GCP","license":"Apache-2.0","copyright":"The Authors","copyright_email":"you@example.com","supports":[{"platform":"gcp"}],"attributes":[],"depends":[{"name":"inspec-gcp","url":"https://github.com/inspec/inspec-gcp/archive/master.tar.gz","status":"loaded"}],"groups":[{"id":"controls/project_exists.rb","controls":["check if project exists"],"title":"Check if project exists"}],"controls":[{"id":"check if project exists","title":"Check if project exists","desc":"An optional description...","descriptions":[{"label":"default","data":"An optional description..."}],"impact":1.0,"refs":[],"tags":{},"code":"control \"check if project exists\" do\n  impact 1.0\n  title \"Check if project exists\"\n  desc \"An optional description...\"\n    describe google_compute_project_info(project: project_id) do\n        it { should exist }\n    end\nend\n","source_location":{"line":7,"ref":"./controls/project_exists.rb"},"results":[{"status":"passed","code_desc":"Compute Project Info doms-cpa-forseti-sbx should exist","run_time":0.002256,"start_time":"2019-10-15T13:01:48-05:00"}]}],"status":"loaded"},{"name":"inspec-gcp","version":"0.16.1","sha256":"c7cb1b87ce95c77b5a147c2cdceea3a15070e569477ffc50adccbb854809c861","title":"Google Cloud Platform Resource Pack","maintainer":"spaterson@chef.io,russell.seymour@turtlesystems.co.uk","summary":"This resource pack provides compliance resources_old_ignore for Google Cloud Platform","license":"Apache-2.0","copyright":"spaterson@chef.io,russell.seymour@turtlesystems.co.uk","copyright_email":"spaterson@chef.io,russell.seymour@turtlesystems.co.uk","supports":[{"platform":"gcp"}],"attributes":[],"parent_profile":"gitops","groups":[],"controls":[],"status":"loaded"}],"statistics":{"duration":0.00655},"version":"4.16.0"}
```

Highlighted **outcome**:

![result.json](/docs/result.json.png "result.json")

