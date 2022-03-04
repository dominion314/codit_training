# GCP Inspec Tests
This folder is the inspec profile directory that will be used by Jenkins job: {name to be added} to execute gcp inspec tests on pull requests to master.

All gcp resource inspec tests reside here: ```inspec/controls```

**All network inspec tests need to be updated so they have .old on the end of the file names so they are not executed until they are updated** 

At a high level, the Jenkins job kicks off the following automation:
1.  Start pod with Inspec components installed
2.  Pod will clone repo
3.  Pod will merge parameter yml files using yq and place in directory ```inspec/files``` of the cloned repo.
4.  Pod will execute inspec command ```inspec exec . -t gcp://```
5.  Test results will be returned to ???
