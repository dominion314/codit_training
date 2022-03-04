package kohls.gitops.kcc.gcp_project.iam.roles

# policy data
policy_data_iam = {
        "allowedRoles": {
            "nonprd": {
            "roles": [
               {
                  "compute.imageUser": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iam.serviceAccountTokenCreator": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": false
                  }
               },
               {
                  "sourcerepo.serviceAgent": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "compute.osLogin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "storage.admin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "bigquery.admin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iam.serviceAccountKeyAdmin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": false
                  }
               },
               {
                  "bigquerydatatransfer.serviceAgent": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               }
            ]
         },
         "prd": {
            "roles": [
               {
                  "compute.imageUser": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iam.serviceAccountTokenCreator": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": false
                  }
               },
               {
                  "sourcerepo.serviceAgent": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "compute.osLogin": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": false
                  }
               },
               {
                  "storage.admin": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "bigquery.admin": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iam.serviceAccountKeyAdmin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": false,
                     "allowedForUsers": false
                  }
               },
               {
                  "bigquerydatatransfer.serviceAgent": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               }
            ]
         },
         "sbx": {
            "roles": [
               {
                  "compute.imageUser": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": true
                  }
               },
               {
                  "iam.serviceAccountTokenCreator": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": true
                  }
               },
               {
                  "sourcerepo.serviceAgent": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": true
                  }
               },
               {
                  "compute.osLogin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "storage.admin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": true
                  }
               },
               {
                  "bigquery.admin": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iam.serviceAccountKeyAdmin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": true
                  }
               },
               {
                  "bigquerydatatransfer.serviceAgent": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               }
            ]
         }
      },
        "allowedRolesPerProject": {
         "kohls-platform-dbaas-ops": {
            "roles": [
               {
                  "cloudsql.client": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "datamigration.admin": {
                     "allowedForGroups": true,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "iap.tunnelResourceAccessor": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
                  }
               },
               {
                  "storage.hmacKeyAdmin": {
                     "allowedForGroups": false,
                     "allowedForServiceAccounts": true,
                     "allowedForUsers": false
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
    "iamPolicyMembers": {
        "usersByEmail": {
            "user@kohls.com": {"roles": [ "editor", "viewer"] }
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
    "iamPolicyMembers": {
        "usersByEmail": {
            "user@kohls.com": {"roles": [ "editor", "viewer", "admin"] }
        }
    }
}

input_role_not_allowed_for_group_not_listed = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
            },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "adminOfUniverse" ] }
        }
    }
}


input_user_allowed_group_not_allowed_not_listed = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
            },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "usersByEmail": {
            "user@kohls.com": {"roles": [ "adminOfUniverse" ] }
        },
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "adminOfUniverse" ] }
        }
    }
}

input_user_allowed_service_accounts_not_allowed_not_listed = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "serviceAccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "iam.serviceAccountOfUniverse" ] }
        }
    }
}
# ***Tests for Environment nonprd ***

input_allowed_allowedForGroups = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "bigquery.admin" ] } # Allowed for Groups
        }
    }
}
input_not_allowed_allowedForGroups = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "bigquerydatatransfer.serviceAgent" ] } # Not Allowed for Groups
        }
    }
}
input_allowed_allowedForServiceAccounts = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "ServiceaccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "bigquerydatatransfer.serviceAgent" ] } # Allowed for Service Accounts
        }
    }
}
input_not_allowed_allowedForServiceAccounts = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "serviceAccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "iam.serviceAccountKeyAdmin" ] } # Not Allowed for Service Accounts
        }
    }
}
input_not_allowed_allowedForUsers = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "usersByEmail": {
            "user@kohls.com": {"roles": [ "bigquery.admin"] } # Not Allowed for Users
        }
    }
}


# ***Tests for prd Environment***

input_not_allowed_prd_allowedForGroups = {
    "project": {
        "labels": {
            "environment-type": "prd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "storage.admin" ] } # Not Allowed for Groups for prd, but is in lle.
        }
    }
}
input_allowed_nonprd_allowedForGroups = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "storage.admin" ] } # Not Allowed for Groups for prd, but is in othere.
        }
    }
}

input_not_allowed_prd_allowedForServiceAccounts = {
    "project": {
        "labels": {
            "environment-type": "prd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "serviceAccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "compute.osLogin" ] } # Not Allowed for Service Accounts for prd, but is in others.
        }
    }
}
input_allowed_nonprd_allowedForServiceAccounts = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "ServiceaccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "compute.osLogin" ] } # Not Allowed for Service Accounts for prd, but is in others.
        }
    }
}

# ***Tests for sbx Environment***

input_allowed_sbx_allowedForGroups = {
    "project": {
        "labels": {
            "environment-type": "sbx"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "sourcerepo.serviceAgent" ] } # Allowed for Groups for sbx, but is in other.
        }
    }
}

input_not_allowed_nonsbx_allowedForGroups = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "sourcerepo.serviceAgent" ] } # Allowed for Groups for sbx, but is not in other.
        }
    }
}

input_allowed_sbx_allowedForServiceAccounts = {
    "project": {
        "labels": {
            "environment-type": "sbx"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "serviceAccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "iam.serviceAccountTokenCreator" ] } # Allowed for Service Accounts for sbx, but is not in other.
        }
    }
}

input_not_allowed_nonsbx_allowedForServiceAccounts = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "serviceAccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "iam.serviceAccountTokenCreator" ] } # Allowed for Service Accounts for sbx, but is not in other.
        }
    }
}

input_allowed_sbx_allowedForUsers = {
    "project": {
        "labels": {
            "environment-type": "sbx"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "usersByEmail": {
            "user@kohls.com": {"roles": [ "compute.imageUser"] } # Allowed for Users for sbx, but is not in other.
        }
    }
}

input_not_allowed_nonsbx_allowedForUsers = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
        },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "usersByEmail": {
            "user@kohls.com": {"roles": [ "compute.imageUser"] } # Allowed for Users for sbx, but is not in other.
        }
    }
}

# *** Roles per project ***
input_allowed_by_project = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
            },
        "name": "kohls-platform-dbaas-ops"
    },
    "iamPolicyMembers": {
        "serviceAccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "iap.tunnelResourceAccessor", "storage.hmacKeyAdmin" ] }
        },
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "cloudsql.client" ] }
        }
    }
}

input_not_allowed_by_project = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
            },
        "name": "project_name"
    },
    "iamPolicyMembers": {
        "serviceAccountsByEmail": {
            "serviceaccount@kohls.com": {"roles": [ "iap.tunnelResourceAccessor", "storage.hmacKeyAdmin" ] }
        },
        "groupsByEmail": {
            "group@kohls.com": {"roles": [ "cloudsql.client" ] }
        }
    }
}

# *************************************** TEST CASES ********************************************
# Unknown Environment: DO NOT ALLOW
test_bad_project_environment {
    not allow with input as input_bad_environment with data.iam as policy_data_iam
}

# Unknown Role: DO NOT ALLOW
test_role_not_listed {
    not allow with input as input_role_is_not_listed with data.iam as policy_data_iam
}

# Unknown Group: DO NOT ALLOW
test_input_role_not_allowed_for_group_not_listed {
    not allow with input as input_role_not_allowed_for_group_not_listed with data.iam as policy_data_iam
}

# not allow if any of requested roles are unknown
test_input_user_allowed_group_not_allowed_not_listed {
    not allow with input as input_user_allowed_group_not_allowed_not_listed with data.iam as policy_data_iam
}

# Unknown service account: DO NOT ALLOW
test_input_user_allowed_service_accounts_not_allowed_not_listed {
    not allow with input as input_user_allowed_service_accounts_not_allowed_not_listed with data.iam as policy_data_iam
}

# ***Tests for lle,hle,ops Environment***
test_input_allowed_allowedForGroups {
    allow with input as input_allowed_allowedForGroups with data.iam as policy_data_iam
}
test_input_not_allowed_allowedForGroups {
    not allow with input as input_not_allowed_allowedForGroups with data.iam as policy_data_iam
}
test_input_allowed_allowedForServiceAccounts {
    allow with input as input_allowed_allowedForServiceAccounts with data.iam as policy_data_iam
}
test_input_not_allowed_allowedForServiceAccounts {
    not allow with input as input_not_allowed_allowedForServiceAccounts with data.iam as policy_data_iam
}
test_input_not_allowed_allowedForUsers {
    not allow with input as input_not_allowed_allowedForUsers with data.iam as policy_data_iam
}
# ***Tests for prd Environment***
test_input_not_allowed_prd_allowedForGroups {
    not allow with input as input_not_allowed_prd_allowedForGroups with data.iam as policy_data_iam
}
test_input_not_allowed_prd_allowedForServiceAccounts {
    not allow with input as input_not_allowed_prd_allowedForServiceAccounts with data.iam as policy_data_iam
}
test_input_allowed_nonprd_allowedForGroups {
    allow with input as input_allowed_nonprd_allowedForGroups with data.iam as policy_data_iam
}
test_input_allowed_nonprd_allowedForServiceAccounts {
    allow with input as input_allowed_nonprd_allowedForServiceAccounts with data.iam as policy_data_iam
}
# ***Tests for sbx Environment***
test_input_allowed_sbx_allowedForGroups {
    allow with input as input_allowed_sbx_allowedForGroups with data.iam as policy_data_iam
}
test_input_not_allowed_nonsbx_allowedForGroups {
    not allow with input as input_not_allowed_nonsbx_allowedForGroups with data.iam as policy_data_iam
}
test_input_allowed_sbx_allowedForServiceAccounts {
    allow with input as input_allowed_sbx_allowedForServiceAccounts with data.iam as policy_data_iam
}
test_input_not_allowed_nonsbx_allowedForServiceAccounts {
    not allow with input as input_not_allowed_nonsbx_allowedForServiceAccounts with data.iam as policy_data_iam
}
test_input_allowed_sbx_allowedForUsers {
    allow with input as input_allowed_sbx_allowedForUsers with data.iam as policy_data_iam
}
test_input_not_allowed_nonsbx_allowedForUsers {
    not allow with input as input_not_allowed_nonsbx_allowedForUsers with data.iam as policy_data_iam
}
# *** Test by Projects ***
test_input_allowed_by_project {
    allow with input as input_allowed_by_project with data.iam as policy_data_iam
}
test_input_not_allowed_by_project {
    not allow with input as input_not_allowed_by_project with data.iam as policy_data_iam
}
