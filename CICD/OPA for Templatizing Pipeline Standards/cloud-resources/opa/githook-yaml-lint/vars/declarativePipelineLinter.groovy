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
            context: "Declarative Jenkinsfile Linter"
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

def runLinter() {
    vaultSecrets = [
        [
            $class: 'VaultSecret',
            path: 'secret/xpaas/service-account/ad-prd',
            engineVersion: 1,
            secretValues: [
                [$class: 'VaultSecretValue', envVar: 'JENKINS_USERNAME', vaultKey: 'user'],
                [$class: 'VaultSecretValue', envVar: 'JENKINS_PASSWORD', vaultKey: 'pass']
            ]
        ]
    ]

    def declarative_pipeline_validation = libraryResource('./declarative_pipeline_validation.py')
    def declarative_requirements = libraryResource('./declarative_requirements.txt')

    writeFile file: 'declarative_pipeline_validation.py', text: declarative_pipeline_validation
    writeFile file: 'declarative_requirements.txt', text: declarative_requirements

    wrap([$class: 'VaultBuildWrapper', vaultSecrets: vaultSecrets]) {
        sh "pip3 install --user --proxy http://proxy.kohls.com:3128 -r declarative_requirements.txt"
        def status_code = sh(script: "python3 declarative_pipeline_validation.py --work_directory=\$(pwd) " +
            "--username=${JENKINS_USERNAME} --password=${JENKINS_PASSWORD} --jenkins_url=${JENKINS_URL}", returnStatus: true)

        if (status_code != 0) {
            error "Error on declarative jenkinsfile validation"
        }
    }
}

def call() {
    def uuid = UUID.randomUUID().toString().take(5)
    pipeline {
        agent {
            kubernetes {
                cloud "xpaas-jenkins-slaves"
                label "xpaas-jenkinsfile-declarative-linter-${uuid}"
                activeDeadlineSeconds 3600
                serviceAccount "jenkins"
                containerTemplate(
                    name: 'jnlp',
                    image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-python36:latest",
                    alwaysPullImage: true,
                    resourceRequestCpu: '1',
                    resourceRequestMemory: '128Mi'
                )
            }
        }
        stages {
            stage('Set Pending Status') {
                steps {
                    setBuildStatus("Running declarative jenkinsfile linter", "PENDING")
                }
                post {
                    failure {
                        setBuildStatus("Job failed with error", "ERROR")
                    }
                }
            }
            stage('Run linter on declarative pipelines') {
                steps {
                    script {
                        runLinter()
                    }
                }
                post {
                    success{
                        setBuildStatus("Declarative jenkinsfile validation passed successfully", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("Declarative jenkinsfile validation failed", "ERROR")
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
