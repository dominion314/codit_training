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
            context: "Schema Validation"
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

def call(String schemasRepo, String schemasRootDir) {
    pipeline {
        agent {
            kubernetes {
                cloud "xpaas-jenkins-slaves"
                label "xpaas-ansible-linter"
                activeDeadlineSeconds 3600
                serviceAccount "jenkins"
                containerTemplate(
                    name: 'jnlp',
                    image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-linters:latest",
                    alwaysPullImage: true,
                    resourceRequestCpu: '200m',
                    resourceRequestMemory: '128Mi'
                )
            }
        }
        stages {
            stage('Cloning schemas-repository') {
                steps {
                    setBuildStatus("Running schema validation", "PENDING")
                    dir('../schemas-repository') {
                        git branch: "master",
                            credentialsId: 'github-pzxpaas',
                            url: schemasRepo
                    }
                }
            }
            stage('Perform Cerberus check') {
                steps {
                    script {
                        def checks = [:]
                        def cerberus_validation = libraryResource('./cerberus_validation.py')
                        writeFile file: 'cerberus_validation.py', text: cerberus_validation
                        def manifests = sh(script: "find . -name \"validation_manifest.json\"", returnStdout: true)
                                          .trim()
                                          .split('\n')
                                          .toList()
                        for (manifest in manifests) {
                            def manifest_path = manifest
                            checks[manifest_path] = {
                                sh """python3 cerberus_validation.py \
                                      --manifest_file ${manifest_path} \
                                      --schemas_dir ../schemas-repository/${schemasRootDir}
                                   """
                            }
                        }
                        try {
                            parallel checks
                            setBuildStatus("Schema validation passed", "SUCCESS")
                        } catch (Exception e) {
                            setBuildStatus("Schema validation failed", "FAILURE")
                            throw e
                        }
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
