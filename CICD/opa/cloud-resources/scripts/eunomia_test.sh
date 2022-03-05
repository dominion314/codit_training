#!/bin/bash

myCronJob="None"
myParmFile="None"
myTemplateFile="None"
while getopts ":c:p:t:" opt; do
    case ${opt} in
      c ) myCronJob=$OPTARG
        ;;
      p ) myParmFile=$OPTARG
        ;;
      t ) myTemplateFile=$OPTARG
        ;;
      \? ) echo "Usage: cmd [-c] <cron job> [-p] <parameter file> [-t] <template file>"
        ;;
    esac
done

if [[ "$myCronJob" != "None" && "$myParmFile" != "None" && "$myTemplateFile" != "None" ]]
  then
      echo "Pulling values from eunomia cronjob --> $myCronJob"
      boolJobExists=$(kubectl get cronjob "${myCronJob}" --no-headers | wc -l )
      if (( boolJobExists > 0))
        then
           GITOPSCONFIG_NAME=$(kubectl get cronjobs "${myCronJob}" -o yaml | grep -A1 "name: GITOPSCONFIG_NAME" | grep -v "name: GITOPSCONFIG_NAME" | awk -F "value: " '{print $2}')
           TEMPLATE_GIT_URI=$(kubectl get cronjobs "${myCronJob}" -o yaml | grep -A1 "name: TEMPLATE_GIT_URI" | grep -v "name: TEMPLATE_GIT_URI" | awk -F "value: " '{print $2}')
           PARAMETER_GIT_URI=$(kubectl get cronjobs "${myCronJob}" -o yaml | grep -A1 "name: PARAMETER_GIT_URI" | grep -v "name: PARAMETER_GIT_URI" | awk -F "value: " '{print $2}')
           MY_HTTP_PROXY=$(kubectl get cronjobs "${myCronJob}" -o yaml | grep -A1 "name: PARAMETER_GIT_HTTP_PROXY" | grep -v "name: PARAMETER_GIT_HTTP_PROXY" | awk -F "value: " '{print $2}')
           CLONED_TEMPLATE_GIT_DIR=$(kubectl get cronjobs "${myCronJob}" -o yaml | grep -A1 "name: CLONED_TEMPLATE_GIT_DIR" | grep -v "name: CLONED_TEMPLATE_GIT_DIR" | awk -F 'value: /git/templates/' '{print $2}')
           CLONED_PARAMETER_GIT_DIR=$(kubectl get cronjobs "${myCronJob}" -o yaml | grep -A1 "name: CLONED_PARAMETER_GIT_DIR" | grep -v "name: CLONED_PARAMETER_GIT_DIR" | awk -F 'value: /git/parameters/' '{print $2}')
           TEMPLATE_ENGINE=$(kubectl get cronjobs "${myCronJob}" -o yaml | grep " image: " | awk -F 'image: ' '{print $2}')
           echo "---" > "${myParmFile}"
           echo "GITOPSCONFIG_NAME --> ${GITOPSCONFIG_NAME}"
           echo "GITOPSCONFIG_NAME: ${GITOPSCONFIG_NAME}" >> "${myParmFile}"
           echo "TEMPLATE_GIT_URI  --> $TEMPLATE_GIT_URI"
           echo "TEMPLATE_GIT_URI: ${TEMPLATE_GIT_URI}" >> "${myParmFile}"
           echo "PARAMETER_GIT_URI --> ${PARAMETER_GIT_URI}"
           echo "PARAMETER_GIT_URI: ${PARAMETER_GIT_URI}" >> "${myParmFile}"
           echo "HTTP_PROXY        --> ${MY_HTTP_PROXY}"
           echo "HTTP_PROXY: ${MY_HTTP_PROXY}" >> "${myParmFile}"
           echo "CLONED_TEMPLATE_GIT_DIR  --> ${CLONED_TEMPLATE_GIT_DIR}"
           echo "CLONED_TEMPLATE_GIT_DIR: ${CLONED_TEMPLATE_GIT_DIR}" >> "${myParmFile}"
           echo "CLONED_PARAMETER_GIT_DIR --> ${CLONED_PARAMETER_GIT_DIR}"
           echo "CLONED_PARAMETER_GIT_DIR: ${CLONED_PARAMETER_GIT_DIR}" >> "${myParmFile}"
           echo "TEMPLATE_ENGINE: ${TEMPLATE_ENGINE}" >> "${myParmFile}"
           cat "${myParmFile}"
           j2 -f yaml "${myTemplateFile}" "${myParmFile}"
           j2 -f yaml "${myTemplateFile}" "${myParmFile}" | kubectl create -f -
      fi
else
      echo "Usage: cmd [-c] <cron job> [-p] <parameter file> [-t] <template file>"
fi
