package commonmerit.gitops.kcc.gcp_project.service.apis

# policy data
policy_data = {
      "allowedAPIsPerProject": {
         "project-a": [
              "stackdriver.googleapis.com",
              "odd.googleapis.com"
         ]
      },
      "allowedAPIs": {
         "nonprd": [
            "cloudresourcemanager.googleapis.com",
            "compute.googleapis.com"
         ],
         "prd": [
            "cloudresourcemanager.googleapis.com",
            "compute.googleapis.com",
            "bigquery-json.googleapis.com"
         ]
      }
}

# inputs
input_bad_environment = {
   "project": {
      "labels": {
         "environment-type": "llee"
        },
      "name": "project-a"
   },
   "serviceAPIs": {
      "bigquery-json.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "cloudresourcemanager.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "compute.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "stackdriver.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      }
   }
}

input_allowed_by_env = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project-a"
    },
   "serviceAPIs": {
      "cloudresourcemanager.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "compute.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      }
   }
}

input_allowed_by_project = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project-a"
    },
   "serviceAPIs": {
      "cloudresourcemanager.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "compute.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "stackdriver.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      }
   }
}

input_bad_role = {
   "project": {
      "labels": {
         "environment-type": "llee"
        },
      "name": "project-a"
   },
   "serviceAPIs": {
      "bigquery-json.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "cloudresourcemanager.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "compute.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      },
      "badrole.googleapis.com": {
         "deletionPolicy": "abandon",
         "disableDependentServices": false
      }
   }
}

# *************************************** TEST CASES ********************************************
# Unknown environment: DO NOT ALLOW
test_not_allow_with_wrong_env {
    not allow with input as input_bad_environment with data.service as policy_data
}

test_allow_by_env {
    allow with input as input_allowed_by_env with data.service as policy_data
}

test_allow_by_project {
    allow with input as input_allowed_by_project with data.service as policy_data
}

test_not_allow {
    not allow with input as input_bad_role with data.service as policy_data
}