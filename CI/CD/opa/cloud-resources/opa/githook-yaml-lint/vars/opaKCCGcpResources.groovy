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
            context: "Open Policy Agent Validation"
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

def call(String opaRepo, String opaPolicyFolder, String localOpaConfig) {
    pipeline {
        agent {
            node {
                label 'cpa-inspec'
                // Will be switching this pipeline to label that will correspond to image with opa in place.
            }
        }
        options {
            ansiColor('xterm')
        }
        environment {
            HTTP_PROXY="http://proxy-gcp-central.kohls.com:8080"
            HTTPS_PROXY="http://proxy-gcp-central.kohls.com:8080"
            http_proxy="http://proxy-gcp-central.kohls.com:8080"
            https_proxy="http://proxy-gcp-central.kohls.com:8080"
        }

        stages {
            stage('Cloning opa-repository') {
                steps {
                    setBuildStatus("Running OPA Validation", "PENDING")
                    dir('../opa-repository') {
                        git branch: "master",
                            credentialsId: 'github-nzbldqc',
                            url: opaRepo
                    }
                }
            }
            stage('Locate OPA binary and prepare environment') {
                steps {
                    sh("""
                    mkdir /tmp/opa
                    touch /tmp/opa.log
                    touch /tmp/report.txt
                    opa_binary=`which opa` || true
                    if [ -n \"\$opa_binary\" ]; then
                    echo "Found opa binary in the system"
                    ln -s \$opa_binary /tmp/opa/opa
                    else
                    echo "opa binary is not found in the system. Will download..."
                    curl -L -o /tmp/opa/opa.tgz https://cicd-nexus.kohls.com:8443/nexus/service/local/repositories/cmfc-nexus-thirdparty/content/com/kohls/infrastructure/open-policy-agent/0.17.3/open-policy-agent-0.17.3.tar.gz
                    cd /tmp/opa; tar -xzvf opa.tgz; chmod 755 opa
                    fi
                    ls -la /tmp/opa/opa
                    """)
                }
            }
            stage('OPA Validation') {
                steps {
                    setBuildStatus("Running OPA Validation", "PENDING")
                    script {
                        def main_script = libraryResource('opa_validation/opa_linter.py')
                        def requirements = libraryResource('opa_validation/requirements.txt')
                        def runner_script = libraryResource('opa_validation/opa_run.py')
                        
                        writeFile file: 'requirements.txt', text: requirements
                        writeFile file: 'main_script.py', text: main_script
                        writeFile file: 'runner_script.py', text: runner_script

                        // install python requirements
                        // Todo: will bring those requirements in image to minimize installation of deps in pipeline.
                        sh("""
                          pip3 install -r requirements.txt --user --proxy=http://proxy-gcp-central.kohls.com:8080
                          """)

                        sh("""
                        cd ${WORKSPACE}/../opa-repository/${opaPolicyFolder}
                        python3 ${WORKSPACE}/main_script.py --log_file=/tmp/opa.log --report_file=/tmp/report.txt --opa_binary=/tmp/opa/opa --opa_config=${WORKSPACE}/${localOpaConfig} --opa_runner=${WORKSPACE}/runner_script.py --opa_suite_definition=policy_suite.yml
                        """) 
                    }
                }
                post {
                    success {
                        sh "cat /tmp/report.txt"
                        sh "cat /tmp/opa.log"
                        sh "cp /tmp/opa.log ${WORKSPACE}"
                        sh "cp /tmp/report.txt ${WORKSPACE}"
                        archiveArtifacts artifacts: 'opa.log', fingerprint: true
                        archiveArtifacts artifacts: 'report.txt', fingerprint: true
                        setBuildStatus("OPA Validation completed", "SUCCESS")
                    }
                    failure {
                        sh "cat /tmp/report.txt"
                        sh "cat /tmp/opa.log"
                        sh "cp /tmp/opa.log ${WORKSPACE}"
                        sh "cp /tmp/report.txt ${WORKSPACE}"
                        archiveArtifacts artifacts: 'opa.log', fingerprint: true
                        archiveArtifacts artifacts: 'report.txt', fingerprint: true
                        setBuildStatus("OPA Validation failed", "FAILURE")
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
