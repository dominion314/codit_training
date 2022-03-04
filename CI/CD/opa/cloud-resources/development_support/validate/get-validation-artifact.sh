#!/bin/bash -e 
#
#

VALIDATION_MANIFEST_FILE=development_support/validate/cloudbuild-validate-input.yaml
LOGS_FILE=logs.txt
ARTIFACT_ANIFEST_FILE=artifact-manifest.json 
KCC_INPUT_FILE=render.yml
INSPEC_INPUT_FILE=input.yml

# create tmp file
touch $LOGS_FILE

# submit job and dump logs to tmp file
gcloud builds submit --config=$VALIDATION_MANIFEST_FILE | tee $LOGS_FILE

# get artifact manifest url from logs
gsutil cp "$(grep 'Artifact manifest located at' $LOGS_FILE | sed 's/Artifact manifest located at//' | tr -d '[:space:]')" "$ARTIFACT_ANIFEST_FILE"

# save url to kcc 
RENDERED_FILE=$(grep kcc $ARTIFACT_ANIFEST_FILE | sed 's/{"location":"//' | sed 's/".*//')
MERGED_FILE=$(grep input.yml $ARTIFACT_ANIFEST_FILE | sed 's/{"location":"//' | sed 's/".*//')

gsutil cp "$RENDERED_FILE" "$KCC_INPUT_FILE"
gsutil cp "$MERGED_FILE" "$INSPEC_INPUT_FILE"
