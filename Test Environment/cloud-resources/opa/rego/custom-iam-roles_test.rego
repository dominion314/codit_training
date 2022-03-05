package doms.gitops.kcc.gcp_project.custom.iam.roles

policy_data_custom_iam = { "allowedRoles": {
         "nonprd": {
            "roles": [
               {
                  "CustomRole664": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomCustomInstanceMove": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomComputeInstanceAdminv1": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iaas_xpn_engineer": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomBQsavedqueries": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "StorageObjectReadWriteDelete": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "Jenkins_kos_CICD_Autoscale": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "getSerialPortOutput": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "gceSetInstanceMetaData": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               }
            ]
         },
         "prd": {
            "roles": [
               {
                  "CustomRole664": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomCustomInstanceMove": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomComputeInstanceAdminv1": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iaas_xpn_engineer": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomBQsavedqueries": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "StorageObjectReadWriteDelete": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "Jenkins_kos_CICD_Autoscale": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "getSerialPortOutput": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "gceSetInstanceMetaData": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               }
            ]
         },
         "sbx": {
            "roles": [
               {
                  "CustomRole664": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": true
                  }
               },
               {
                  "CustomCustomInstanceMove": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomComputeInstanceAdminv1": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iaas_xpn_engineer": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "CustomBQsavedqueries": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "StorageObjectReadWriteDelete": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "Jenkins_kos_CICD_Autoscale": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "getSerialPortOutput": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "gceSetInstanceMetaData": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               }
            ]
         }
      }
}

policy_data_iam = { "allowedRolesPerProject": {
         "doms-cpe-e2edemo-lle": {
            "roles": [
               {
                  "editor": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": true
                  }
               },
               {
                  "bigquery.jobUser": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": true
                  }
               },
               {
                  "viewer": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": true
                  }
               }
            ]
         }
   }
}


# inputs
input_bad_environment = {
    "project": {
        "labels": {
            "environment-type": "wrong_env"
        }
    },
    "iamPolicyMembersV2": {
        "groupsByEmail": {
            "group@doms.com": [
                {
                    "role": "gceSetInstanceMetaData"
                },
                {
                    "role": "getSerialPortOutput"
                }
            ]
        }
    }
}

input_role_is_not_listed = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "groupsByEmail": {
            "group@doms.com": [
                {
                    "role": "Jenkins_kos_CICD_Autoscale"
                },
                {
                    "role": "StorageObjectReadWriteDelete"
                },
                {
                    "role": "notRole"
                }
            ]
        }
    }
}

input_sa_allowed_group_not_allowed = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
            },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "serviceAccountsByEmail": {
            "sa@doms.com": [
                {
                    "role": "StorageObjectReadWriteDelete"
                }
            ]
        },
        "groupsByEmail": {
            "group@doms.com": [
                {
                    "role": "adminOfUniverse"
                }
            ]
        }
    }
}


input_sa_allowed_group_allowed = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "serviceAccountsByEmail": {
            "sa@doms.com": [
                {
                    "role": "adminOfUniverse"
                }
            ]
        },
        "groupsByEmail": {
            "group@doms.com": [
                {
                    "role": "editor"
                }
            ]
        }
    }
}

# *** Tests for Environments nonprd ***
input_allowed_group = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "groupsByEmail": {
            "group@doms.com": [
                {
                    "role": "CustomBQsavedqueries"
                }
            ]
        }
    }
}
input_allowed_sa = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "serviceAccountsByEmail": {
            "sa@doms.com": [
                {
                    "role": "iaas_xpn_engineer"
                }
            ]
        }
    }
}
input_allowed_sa_group = {
    "project": {
        "labels": {
            "environment-type": "prd"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "serviceAccountsByEmail": {
            "sa@doms.com": [
                {
                    "role": "CustomComputeInstanceAdminv1"
                }
            ],
            "group@doms.com": [
                {
                    "role": "CustomCustomInstanceMove"
                }
            ]
        }
    }
}
# *** Tests for Environments sbx ***
input_allowed_sbx_user = {
    "project": {
        "labels": {
            "environment-type": "sbx"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "usersByEmail": {
            "user@doms.com": [
                {
                    "role": "CustomRole664" #Only allowed for sbx.
                }
            ]
        }
    }
}
input_not_allowed_nonops_user = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "usersByEmail": {
            "user@doms.com": [
                {
                    "role": "CustomRole664"
                }
            ]
        }
    }
}

# *** Tests for projects ***
input_allowed_per_projects = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "doms-cpe-e2edemo-lle"
    },
    "iamPolicyMembersV2": {
        "usersByEmail": {
            "user@doms.com": [
                {
                    "role": "editor" #Only allowed for doms-cpe-e2edemo-lle
                }
            ]
        }
    }
}

input_not_allowed_per_projects = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembersV2": {
        "usersByEmail": {
            "user@doms.com": [
                {
                    "role": "editor" #Only allowed for doms-cpe-e2edemo-lle
                }
            ]
        }
    }
}

# *************************************** TEST CASES ********************************************
# Unknown environment: DO NOT ALLOW
test_bad_project_environment {
    not allow with input as input_bad_environment with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}

# Requested role is not listed: DO NOT ALLOW
test_role_not_listed {
    not allow with input as input_role_is_not_listed with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}

# not allow if any of requested roles is not allowed
test_not_allow_if_any_not_allowed {
    not allow with input as input_sa_allowed_group_not_allowed with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}

# *** Tests for Environments ***
test_input_allowed_group {
    allow with input as input_allowed_group with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}
test_input_allowed_sa {
    allow with input as input_allowed_sa with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}
test_input_allowed_sa_group {
    allow with input as input_allowed_sa_group with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}
test_input_allowed_sbx_user {
    allow with input as input_allowed_sbx_user with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}
test_input_not_allowed_nonops_user {
    not allow with input as input_not_allowed_nonops_user with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}

# *** Tests per Project ***
test_input_allowed_per_projects {
    allow with input as input_allowed_per_projects with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}
test_input_not_allowed_per_projects {
    not allow with input as input_not_allowed_per_projects with data.customIam as policy_data_custom_iam with data.iam as policy_data_iam
}
