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
            context: "Ansible Linter"
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

def call() {
    def uuid = UUID.randomUUID().toString().take(5)
    pipeline {
        agent {
            kubernetes {
                cloud "xpaas-jenkins-slaves"
                label "xpaas-ansible-linter-${uuid}"
                activeDeadlineSeconds 3600
                serviceAccount "jenkins"
                containerTemplate(
                    name: 'jnlp',
                    image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-linters:latest",
                    alwaysPullImage: true,
                    resourceRequestCpu: '1',
                    resourceRequestMemory: '128Mi'
                )
            }
        }
        stages {
            stage('Checkout githook-yaml-lint Repo') {
                steps {
                    setBuildStatus("Running Ansible linter", "PENDING")
                    dir('hooksRepo/') {
                        git branch: "master",
                            credentialsId: 'github-pzxpaas',
                            url: 'https://github.commonmerit.com/xPaaS-Operations/githook-yaml-lint'
                    }
                }
                post {
                    failure {
                        setBuildStatus("Job failed with error", "ERROR")
                    }
                }
            }
            stage('Performing Ansible Linting') {
                steps {
                    script {
                        if (!getRepoURL().contains('openshift-cluster-config')) {
                            sh ("""
                            export EXCLUSIONS=\$(cat .ansible-lint | grep exclusions | sed "s/exclusions: *//")
                            for file in \$(find . \\( -name "*.yml" -not -regex "\$EXCLUSIONS" \\)); do
                                ansible-lint -c ".ansible-lint" -v \$file;
                            done;
                            """)
                        } else {
                            sh ("""
                            export EXCLUSIONS=\$(cat .ansible-lint | grep exclusions | sed "s/exclusions: *//")
                            for file in \$(find . -maxdepth 1 \\( -name "*.yml" -not -regex "\$EXCLUSIONS" \\)); do
                                ansible-lint -c ".ansible-lint" -v \$file;
                            done;
                            """)
                        }
                    }
                }
                post {
                    success {
                        setBuildStatus("Ansible linting passed", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("Ansible linting failed", "FAILURE")
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
