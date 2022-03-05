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
            context: "Cerberus Schema Files Linter"
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

def call(String schemaFolder) {
    def uuid = UUID.randomUUID().toString().take(5)
    pipeline {
        agent {
            kubernetes {
                cloud "xpaas-jenkins-slaves"
                label "xpaas-cerberus-schema-files-validator-${uuid}"
                activeDeadlineSeconds 3600
                serviceAccount "jenkins"
                containerTemplate(
                    name: 'jnlp',
                    image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-linters:latest",
                    alwaysPullImage: true,
                    resourceRequestCpu: '1',
                    resourceRequestMemory: '128Mi',
                    resourceLimitCpu: '1',
                    resourceLimitMemory: '700Mi'
                )
            }
        }
        stages {
            stage('Performing Cerberus Schema Linting') {
                steps {
                    setBuildStatus("Running Cerberus Schema validation ", "PENDING")
                    script {
                        env.SCHEMA_FOLDER = schemaFolder
                        def script = libraryResource('./cerberus_schema_linter.py')
                        def requirements = libraryResource('./cerberus_schema_linter_requirements.txt')
                        writeFile file: 'requirements.txt', text: requirements
                        writeFile file: 'script.py', text: script
                        
                        sh("""
                          pip3 install -r requirements.txt --user --proxy=http://proxy.doms.com:3128
                          python3 script.py ${SCHEMA_FOLDER}
                          """)
                    }
                }
                post {
                    success {
                        setBuildStatus("Validation of Cerberus schemas passed!", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("Validation of Cerberus schemas failed!", "FAILURE")
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
