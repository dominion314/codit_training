package kohls.gitops.kcc.gcp_project.project

policy_data_project = {
      "allowedFolderId": {
         "nonprd": [
            {
               "non-production-platform": "1057338141298"
            },
            {
               "EnterpriseServices-Credit-Payments": "859213288423"
            },
            {
               "merch-mkt-analytics": "963520663007"
            },
            {
               "supply-field-people": "857045434788"
            },
            {
               "ccx": "124759181101"
            },
            {
               "architecture": "872364499101"
            },
            {
               "security": "882166644980"
            },
            {
               "infra-ops": "345254712059"
            },
            {
               "xpn": "778811484176"
            }
         ],
         "sbx": [
            {
               "non-production-platform": "1057338141298"
            },
            {
               "EnterpriseServices-Credit-Payments": "859213288423"
            },
            {
               "merch-mkt-analytics": "963520663007"
            },
            {
               "supply-field-people": "857045434788"
            },
            {
               "ccx": "124759181101"
            },
            {
               "architecture": "872364499101"
            },
            {
               "security": "882166644980"
            },
            {
               "infra-ops": "345254712059"
            },
            {
               "xpn": "778811484176"
            }
         ],
         "prd": [
            {
               "production-platform": "48229324135"
            },
            {
               "enterprise-services-credit-payments": "155882274299"
            },
            {
               "merch-mkt-analytics": "217021366087"
            },
            {
               "supply-field-people": "921350738615"
            },
            {
               "ccx": "121961327479"
            },
            {
               "architecture": "863157377269"
            },
            {
               "security": "726913521927"
            },
            {
               "infra-ops": "980929416788"
            },
            {
               "xpn": "970875009337"
            }
         ]
      },
      "allowedFolderIdLegacy": {
         "nonprd": [
            "53524313723",
            "102699970763",
            "554838985838",
            "979004260447",
            "545282641185",
            "351126992478",
            "448245936424",
            "668741070945",
            "262213651202",
            "711959037663",
            "439116431032",
            "849181480944",
            "557759831541",
            "26895931360",
            "397110810696",
            "820532634363",
            "402212390076",
            "778811484176",
            "143390332256",
            "1005278392251",
            "884280016542",
            "1018996571054",
            "216500746233",
            "644963936779",
            "307494924870",
            "949731060623",
            "901528147446",
            "28944765966",
            "636952907363",
            "499986558306",
            "345490673407",
            "1050226140279",
            "1031310294968",
            "1023332649452",
            "77081016916",
            "306278316108",
            "624508295600",
            "386637910671",
            "267734544543",
            "666234566364",
            "1071586093516",
            "460517918342",
            "766183312556",
            "931070720587",
            "153127332000",
            "234600925752",
            "253712500046",
            "153230486679",
            "672146589306",
            "564094352953",
            "1003925262889",
            "341043455429",
            "766168305774",
            "402839726008",
            "883693780486"
         ],
         "sbx": [
            "965792343442",
            "3295572382",
            "977449771024",
            "811983839911",
            "1033800604751",
            "224019032935",
            "855803479287",
            "141225868140",
            "977295768158",
            "98432095871",
            "122943202533",
            "825283481745",
            "270129109787",
            "772322907017",
            "310040317736",
            "885700365961",
            "224728249592"
         ],
         "prd": [
            "106220115873",
            "699108937069",
            "793142105925",
            "46233836581",
            "206335353876",
            "197202166383",
            "970875009337",
            "229702298340",
            "875461611002",
            "454873420302",
            "347385755519",
            "1038729868631",
            "242959990518",
            "343146003818",
            "488142938159",
            "1064417150642",
            "397051752047",
            "42263300424",
            "259606834999"
         ]
      }
}

# inputs
input_bad_environment = {
    "project": {
        "folderId": "1057338141298",
        "labels": {
            "environment-type": "wrong_env"
        }
    }
}

input_bad_domain = {
    "project": {
        "folderId": "1057338141298",
        "labels": {
            "environment-type": "nonprd",
            "product-domain": "cloub"
        }
    }
}

input_bad_domain_legacy = {
    "project": {
        "folderId": "53524313723",
        "labels": {
            "environment-type": "nonprd",
            "product-domain": "merch-mkt-analytics"
        }
    }
}

input_allowed_nonprd_legacy = {
    "project": {
        "labels": {
            "environment-type": "nonprd"
            },
        "folderId": "53524313723"
    }
}
input_allowed_sbx_legacy = {
    "project": {
        "labels": {
            "environment-type": "sbx"
            },
        "folderId": "965792343442"
    }
}
input_allowed_prd_legacy = {
    "project": {
        "labels": {
            "environment-type": "prd"
            },
        "folderId": "106220115873"
    }
}
input_not_allowed_legacy = {
    "project": {
        "labels": {
            "environment-type": "sbx"
            },
        "folderId": "21345678"
    }
}
input_allowed_prd = {
    "project": {
        "folderId": "121961327479",
        "labels": {
            "environment-type": "prd",
            "product-domain": "ccx"
        }
    }
}
input_allowed_nonprd = {
    "project": {
        "folderId": "124759181101",
        "labels": {
            "environment-type": "nonprd",
            "product-domain": "ccx"
        }
    }
}
input_allowed_sbx = {
    "project": {
        "folderId": "124759181101",
        "labels": {
            "environment-type": "sbx",
            "product-domain": "ccx"
        }
    }
}
input_not_allowed_domain = {
    "project": {
        "folderId": "124759181101",
        "labels": {
            "environment-type": "sbx",
            "product-domain": "architecture"
        }
    }
}

# *************************************** TEST CASES ********************************************
# Unknown Environment: DO NOT ALLOW
test_bad_project_environment {
    not allow with input as input_bad_environment with data.project as policy_data_project
}
test_input_bad_domain {
    not allow with input as input_bad_domain with data.project as policy_data_project
}
test_input_bad_domain_legacy {
    not allow with input as input_bad_domain_legacy with data.project as policy_data_project
}
test_input_allowed_nonprd_legacy {
    allow with input as input_allowed_nonprd_legacy with data.project as policy_data_project
}
test_input_allowed_sbx_legacy {
    allow with input as input_allowed_sbx_legacy with data.project as policy_data_project
}
test_input_allowed_prd_legacy {
    allow with input as input_allowed_prd_legacy with data.project as policy_data_project
}
test_input_not_allowed_legacy {
    not allow with input as input_not_allowed_legacy with data.project as policy_data_project
}
test_input_allowed_prd {
    allow with input as input_allowed_prd with data.project as policy_data_project
}
test_input_allowed_nonprd {
    allow with input as input_allowed_nonprd with data.project as policy_data_project
}
test_input_allowed_sbx {
    allow with input as input_allowed_sbx with data.project as policy_data_project
}
test_input_not_allowed_domain {
    not allow with input as input_not_allowed_domain with data.project as policy_data_project
}
