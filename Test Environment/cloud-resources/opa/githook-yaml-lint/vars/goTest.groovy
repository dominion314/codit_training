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
            context: "gotest"
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
                    setBuildStatus("Running go test", "PENDING")
                    // The default HTTP_PROXY and HTTPS_PROXY environment variables
                    // are required to remain set to allow downloading Go packages from
                    // the Internet. The NO_PROXY environment variable must be set to
                    // allow tests to conntenct to HTTP endpoint within the Kohl's network.
                    //
                    // * 127.0.0.1     - IPv4 localhost
                    // * 10.0.0.0/8    - all Kohls internal IP address space
                    // * 100.64.0.0/10 - CGN address space used for OpenShift Pods and Services
                    // * 172.16.0.0/12 - private IP address space used for GKE Pod and Services
                    // * ::            - IPv6 localhost
                    // * *.kohls.com   - Include any internal Kohl's DNS names
                    //
                    // See https://godoc.org/golang.org/x/net/http/httpproxy for info abot Go Lang
                    // NO_PROXY environment variable usage.
                    sh("""
                    unset no_proxy
                    export NO_PROXY="127.0.0.1,10.0.0.0/8,100.64.0.0/10,172.16.0.0/12,::,*.kohls.com"
                    export GOROOT=/opt/golang/"${version}"/go
                    export GOPATH=$HOME/go"${version}"
                    export PATH=$GOROOT/bin:$GOPATH/bin:"${PATH}"
                    go test -v -race ./...
                    """)
                }
                post {
                    success {
                        setBuildStatus("Go Test CI successful", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("Go Test CI failed", "FAILURE")
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
