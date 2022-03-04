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
            context: "Network Integrity Validation"
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

def call(String vlanFile, String asnFile) {
    def uuid = UUID.randomUUID().toString().take(5)
    def buildStable = 'string'
    pipeline {
        agent {
            kubernetes {
                cloud "xpaas-jenkins-slaves"
                label "cne-networkvar-check"
                activeDeadlineSeconds 3600
                serviceAccount "jenkins"
                containerTemplate(
                    name: 'jnlp',
                    image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-network-devops:latest",
                    alwaysPullImage: true,
                    resourceRequestCpu: '1',
                    resourceRequestMemory: '1Gi'
                )
            }
        }
        options {
            ansiColor('xterm')
        }
        environment {
            HTTP_PROXY = "http://proxy-gcp-central.kohls.com:8080"
            HTTPS_PROXY = "http://proxy-gcp-central.kohls.com:8080"
            http_proxy = "http://proxy-gcp-central.kohls.com:8080"
            https_proxy = "http://proxy-gcp-central.kohls.com:8080"
        }
        stages { 
            stage('Validate python version') {
                steps {
                    setBuildStatus("Running python version check", "PENDING")
                    script {
                      sh("""
                      python --version
                      python3 --version
                      """)
                    }
                }
                post {
                    failure {
                        script {
                          sh("""
                          echo 'Python check failed, either python3 or python2 are not in the image'
                          """)
                        }
                        setBuildStatus("Job failed with error", "ERROR")
                    }
                }
            }
            stage('Network integrity check') {
                steps {
                    setBuildStatus("Network Integrity Check", "PENDING")
                    script{
                        def validationScript = libraryResource('network_integrity_check/run.py')
                        writeFile file: 'validationScript.py', text: validationScript

                        sh("""
                        python3 validationScript.py ${vlanFile} ${asnFile}
                        """)
                    }
                }
                post {
                    success {
                        setBuildStatus("Network Integrity Check", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("Network Integrity Check", "FAILURE")
                    }
                }
            }
        }
        post {
            always {
                cleanWs(
                    skipWhenFailed: true,
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
