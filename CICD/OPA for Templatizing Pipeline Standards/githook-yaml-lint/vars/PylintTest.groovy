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
            context: "PyLinter"
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

def call(String pythonVersion="2") {
    pipeline {
        agent {
            node { label 'kre-prod' }
        }
        stages {
            stage('Validate python version') {
                steps {
                    setBuildStatus("Running Pylint", "PENDING")
                    script {
                      env.PYTHON_VERSION = pythonVersion
                      sh("""
                      which python${PYTHON_VERSION}
                      """)
                    }
                }
                post {
                    failure {
                        script {
                          sh("""
                          set +x
                          echo "Wrong pythonVersion parameter value. python${PYTHON_VERSION} not found."
                          echo "List of the python releases available for use:"
                          compgen -c python | grep -E "^python[0-9](\\.[0-9]*)?\$" | sort | uniq
                          """)
                        }
                        setBuildStatus("Job failed with error", "ERROR")
                    }
                }
            }
            stage('Confirm Requirements') {
                // Use environment variables and command flag so it works
                // regardless of pip version on slave
                environment {
                    http_proxy = 'http://proxy.kohls.com:3128'
                    https_proxy = 'http://proxy.kohls.com:3128'
                    HTTP_PROXY = 'http://proxy.kohls.com:3128'
                    HTTPS_PROXY = 'http://proxy.kohls.com:3128'
                }
                steps {
                    script {
                      // each linted repo should have it's own requirements
                      // if requirements are defined, then install
                      sh("""
                      if [ -f './requirements.txt' ]; then
                          pip${PYTHON_VERSION} install -r ./requirements.txt --user --proxy=http://proxy.kohls.com:3128
                      fi
                      """)
                    }
                }
                post {
                    failure {
                        setBuildStatus("Job failed with error", "ERROR")
                    }
                }
            }
            stage('Performing Pylinting') {
                steps {
                    sh("if [ \$(find . -name '*.py' | wc -l) -ne 0 ]; then pylint_runner${PYTHON_VERSION} -v --rcfile=pylintrc; fi")
                }
                post {
                    success {
                        setBuildStatus("Pylint passed", "SUCCESS")
                    }
                    failure {
                        setBuildStatus("Pylint failed", "FAILURE")
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
