#!/usr/bin/env groovy

void setBuildStatus(String message, String state) {
    repoUrl = getRepoURL()
    commitSha = getCommitSha()
    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [
            $class: "ManuallyEnteredRepositorySource",
            url: repoUrl
        ],
        commitShaSource: [
            $class: "ManuallyEnteredShaSource",
            sha: commitSha
        ],
        contextSource: [
            $class: "ManuallyEnteredCommitContextSource",
            context: "Unit Tests KCC GCP Resources  Linter"
        ],
        errorHandlers: [[
            $class: "ChangingBuildStatusErrorHandler",
            result: "UNSTABLE"
        ]],
        statusResultSource: [
            $class: "ConditionalStatusResultSource",
            results: [[
                $class: "AnyBuildResult",
                message: message,
                state: state
            ]]
        ]
    ]);
}

def getRepoURL() {
  sh "git config --get remote.origin.url > .git/remote-url"
  return readFile(".git/remote-url").trim()
}

def getCommitSha() {
  sh "git rev-parse HEAD > .git/current-commit"
  return readFile(".git/current-commit").trim()
}

def call(String unitTestSuiteDefinitionFile, String unitTestName) {
    def uuid = UUID.randomUUID().toString().take(5)
    pipeline {
        agent {
            node {
                label 'cpa-inspec'
            }
        }
        options {
            ansiColor('xterm')
        }
        environment {
            SA_GKE_CLUSTER = credentials('kcc_ut_gke')
            GOOGLE_APPLICATION_CREDENTIALS = credentials('kcc_ut_inspec')
            HTTP_PROXY="http://proxy.commonmerit.com:3128"
            HTTPS_PROXY="http://proxy.commonmerit.com:3128"
            http_proxy="http://proxy.commonmerit.com:3128"
            https_proxy="http://proxy.commonmerit.com:3128"
            KUBECONFIG="${HOME}/.kube/config"

        }

        stages {
            stage('Performing Unit Tests (KCC GCP Resources)') {
                steps {
                    setBuildStatus("Running Unit Tests (KCC GCP Resources)", "PENDING")
                    script {
                        env.UNIT_TEST_SUITE_DEF = unitTestSuiteDefinitionFile
                        env.UNIT_TEST_SUITE_NAME = unitTestName
                        def main_script = libraryResource('kcc_unit_testing/run_unit_suit.py')
                        def requirements = libraryResource('kcc_unit_testing/requirements.txt')
                        def render_script = libraryResource('kcc_unit_testing/render.py')
                        def inspec_file = libraryResource('kcc_unit_testing/inspec.yml')
                        def ansible_filter_ipaddr = libraryResource('kcc_unit_testing/ansible_filters_ipaddr.py')
                        def ansible_filter_regex_search = libraryResource('kcc_unit_testing/ansible_filters_regex_search.py')
                        
                        writeFile file: 'requirements.txt', text: requirements
                        writeFile file: 'main_script.py', text: main_script
                        writeFile file: 'render_script.py', text: render_script
                        writeFile file: 'inspec.yml', text: inspec_file
                        writeFile file: 'ansible_filters_ipaddr.py', text: ansible_filter_ipaddr 
                        writeFile file: 'ansible_filters_regex_search.py', text: ansible_filter_regex_search

                        env.INSPEC_PROFILE = "${WORKSPACE}/inspec_profile"

                        // install python requirements
                        sh("""
                          pip3 install -r requirements.txt --user --proxy=http://proxy-gcp-central.commonmerit.com:8080
                          """)

                        sh ("""
                            inspec --version
                            which inspec
                            rm -rf ${INSPEC_PROFILE}
                            inspec init profile --platform gcp ${INSPEC_PROFILE} --chef-license accept
                            rm  ${INSPEC_PROFILE}/controls/example.rb
                            cp inspec.yml ${INSPEC_PROFILE}
                            mkdir ${INSPEC_PROFILE}/files
                        """)

                        // authentication gcloud 
                        sh ("""
                            gcloud auth activate-service-account --key-file ${env.SA_GKE_CLUSTER}
                        """)
                        
                        // run main processor
                        sh("""
                            python3 ${WORKSPACE}/main_script.py  --log-file=/tmp/run_test_suite.log --unit-test-suite-definition=${UNIT_TEST_SUITE_DEF} --kubectl-binary=kubectl --yq-binary=yq  --suite-names=${UNIT_TEST_SUITE_NAME} --result_kcc_file=/tmp/kcc.yml --inspec-profile=${INSPEC_PROFILE} --render-script-path=${WORKSPACE}/render_script.py
                        """) 
                    }
                }
                post {
                    success {
                        sh "cat /tmp/run_test_suite.log"
                        setBuildStatus("Validation of Unit Tests (KCC GCP Resources) completed", "SUCCESS")
                    }
                    failure {
                        sh "cat /tmp/run_test_suite.log"
                        setBuildStatus("Validation of Unit Tests (KCC GCP Resources) failed", "FAILURE")
                    }
                }
            }
        }
        post {
            always {
                cleanWs(
                    cleanWhenAborted: true,
                    cleanWhenFailure: true,
                    cleanWhenNotBuilt: true,
                    cleanWhenSuccess: true,
                    cleanWhenUnstable: true,
                    deleteDirs: true
                )
            }
        }
    }
}
