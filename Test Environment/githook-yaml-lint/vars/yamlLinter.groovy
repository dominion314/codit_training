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
            context: "YAML Linter"
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
            node { label 'kre-prod' }
        }
        stages {
            stage('Checkout githook-yaml-lint Repo') {
                steps {
                    setBuildStatus("Running YAML linter", "PENDING")
                    dir('hooksRepo/') {
                        git branch: "master",
                            credentialsId: 'github-nzbldqc',
                            url: 'https://github.doms.com/ReliabilityEngineering/githook-yaml-lint'
                    }
                }
                post {
                    failure {
                        setBuildStatus("Job failed with error", "ERROR")
                    }
                }
            }
            stage('Performing YAML Linting') {
                steps {
                    script{
                        def config = libraryResource('./yamllint_custom_config.yml')
                        writeFile file: 'config.yml', text:config
                        sh("""
                        yamllint -c ./config.yml .
                        if [ \$? -eq 2 ]; then exit 0; fi
                        """)
                    }
                }
                post {
                    success {
                        setBuildStatus("YAML linting passed", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("YAML linting failed", "FAILURE")
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
