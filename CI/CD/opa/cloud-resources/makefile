GCP_TEST_PROJECT=${MY_PROJECT}

TEMPLATE_FILES=templates/gcp-project
PARAMETERS_FILES=test_vars/gcp_project/$(GCP_TEST_PROJECT)

INSPEC_LOCATION=inspec
TMP_INSPEC_PROFILE=tmp-inspec-profile
TMP_PYTHON_ENV=tmp-virtualenv
RENDER_FILE=render.yml

#
# -------------- DEV TESTING --------------
#

# create virtalenv with dependencies to render templates
pythonenv:
	rm -rf $(TMP_PYTHON_ENV) | True
	virtualenv $(TMP_PYTHON_ENV) -p $(shell which python3)
    $(shell \
       source `pwd`/$(TMP_PYTHON_ENV)/bin/activate);\
       pip install -r requirements.txt;\
    )

# init tmp inspec profile, copy controls from inspec fixed location
inspec-profile:
	rm -rf $(TMP_INSPEC_PROFILE) | True
	inspec init profile --platform gcp $(TMP_INSPEC_PROFILE)
	rm $(TMP_INSPEC_PROFILE)/inspec.yml
	rm $(TMP_INSPEC_PROFILE)/controls/example.rb
	cp $(INSPEC_LOCATION)/inspec.yml $(TMP_INSPEC_PROFILE)/inspec.yml
	$(shell export GOOGLE_APPLICATION_CREDENTIALS="`pwd`/key.json")
	cp -r $(INSPEC_LOCATION)/controls/. $(TMP_INSPEC_PROFILE)/controls/
	mkdir $(TMP_INSPEC_PROFILE)/files

# render all params from initiated project against all templates
# create rendered file in main catalog
render:
	rm -f $(RENDER_FILE) | TRUE
	find $(TEMPLATE_FILES)/*.j2 -exec sh -c "yq merge $(PARAMETERS_FILES)/*.yml | j2 -f yaml {} > {}.new " \;
	yq merge $(shell find $(PARAMETERS_FILES)/*) > input.yml
	cp input.yml $(TMP_INSPEC_PROFILE)/files/input.yml
	cat `find $(TEMPLATE_FILES)/*.new` > $(RENDER_FILE)

# This target send whole local repo (without git ignore) to cloud build, process templates with yq, cerberus and j2 and pulls render.yml and input.yml from artifacts
# create rendered file in main catalog
cbrender:
	bash development_support/validate/get-validation-artifact.sh
	cp input.yml $(TMP_INSPEC_PROFILE)/files/input.yml

# annotate GCP namespace to kubectl
project:
	kubectl create namespace gcp-$(GCP_TEST_PROJECT)
	kubectl annotate namespace gcp-$(GCP_TEST_PROJECT) cnrm.cloud.google.com/project-id=$(GCP_TEST_PROJECT)

# apply gcp rendered resources
build:
	kubectl apply -f $(RENDER_FILE)

# run inspec controls
test: 
	cp -r $(INSPEC_LOCATION)/controls/. $(TMP_INSPEC_PROFILE)/controls/
	inspec exec $(TMP_INSPEC_PROFILE) -t gcp://

# render files without project.yml to allow safe removal of crds without removing test project
# then remove kubectl crds
# Reason: you can't use same project id twice, so you dont want to remove
# project when testing parameters other than project 
delete:
	rm -f $(TEMPLATE_FILES)/project.yml.j2.new
	cat `find $(TEMPLATE_FILES)/*.new` > $(RENDER_FILE)
	kubectl delete -f $(RENDER_FILE)
	rm -f $(TEMPLATE_FILES)/*.new
	rm -f $(RENDER_FILE)

cbdelete:
	kubectl delete -f $(RENDER_FILE)
	rm -f $(RENDER_FILE) input.yml logs.txt

# Debuging snippets
logs:
	kubectl get events --sort-by='.lastTimestamp' --namespace gcp-$(GCP_TEST_PROJECT)

#
# "-------------- UTILS "--------------
#

install:
	minikube start --vm-driver=virtualbox
	kubectl create namespace cnrm-system
	kubectl create secret generic gcp-key --from-file key.json --namespace cnrm-system
	make update
	kubectl apply -f install-bundle-gcp-identity/
	rm -rf install-bundle-gcp-identity

update: 
	gsutil cp gs://cnrm/latest/release-bundle.tar.gz release-bundle.tar.gz
	tar -zxvf release-bundle.tar.gz install-bundle-gcp-identity/
	# kubectl apply -f install-bundle-gcp-identity/
	rm release-bundle.tar.gz

uninstall:
	kubectl delete namespace cnrm-system
	minikube delete

reinstall:
	make uninstall
	make install

