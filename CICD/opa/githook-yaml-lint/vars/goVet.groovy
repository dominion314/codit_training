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
            context: "govet"
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

def call(def version) {
    def uuid = UUID.randomUUID().toString().take(5)
    pipeline {
        agent {
            kubernetes {
                cloud "xpaas-jenkins-slaves"
                label "xpaas-go-linter-${uuid}"
                activeDeadlineSeconds 3600
                serviceAccount "jenkins"
                containerTemplate(
                    name: 'jnlp',
                    image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-go:latest",
                    alwaysPullImage: true,
                    resourceRequestCpu: '1',
                    resourceRequestMemory: '256Mi',
                )
            }
        }
        stages {
            stage('Analyzing Go source code') {
                steps {
                    setBuildStatus("Running go vet validation", "PENDING")
                    sh("""
                    export GOROOT=/opt/golang/"${version}"/go
                    export GOPATH=$HOME/go"${version}"
                    export PATH=$GOROOT/bin:$GOPATH/bin:"${PATH}"
                    go vet \$(go list ./... | grep -v /vendor/)
                    """)
                }
                post {
                    success {
                        setBuildStatus("Go Vet CI successful", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("Go Vet CI failed", "FAILURE")
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
