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
            context: "InSpec Testing"
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
    def podImageName = "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-inspec:latest"
    podTemplate(
        cloud: 'xpaas-jenkins-slaves',
        name: "xpaas-jenkins-slaves-inspec",
        label: "xpaas-jenkins-slaves-inspec",
        namespace: 'xpaas-jenkins-slaves',
        nodeUsageMode: 'EXCLUSIVE',
        idleMinutes: 1,
        slaveConnectTimeout: 60,
        activeDeadlineSeconds: 3600,
        containers: [
            containerTemplate(
                name: 'jnlp',
                image: podImageName,
                alwaysPullImage: true,
                resourceRequestCpu: '1',
                resourceRequestMemory: '128Mi'
            )
        ]
    ) {
        ansiColor('xterm') {
            node("xpaas-jenkins-slaves-inspec") {
                stage("Get Config") {
                  checkout scm
                  setBuildStatus("Running Inspec Testing", "PENDING")
                }
                try {
                    stage("Validating Inspec Tests") {
                        def checks = [:]
                        projectLists = ["commonmeritqa-cpa-inspec"]
                        for (int x = 0; x < projectLists.size(); x++) {
                            def project = projectLists[x]
                            checks[project] = {
                                podTemplate(
                                    cloud: 'xpaas-jenkins-slaves',
                                    name: "xpaas-jenkins-slaves-${project}",
                                    label: "xpaas-jenkins-slaves-${project}",
                                    namespace: 'xpaas-jenkins-slaves',
                                    nodeUsageMode: 'EXCLUSIVE',
                                    idleMinutes: 1,
                                    slaveConnectTimeout: 60,
                                    activeDeadlineSeconds: 3600,
                                    containers: [
                                        containerTemplate(
                                            name: 'jnlp',
                                            image: podImageName,
                                            alwaysPullImage: true,
                                            resourceRequestCpu: '1',
                                            resourceRequestMemory: '128Mi'
                                        )
                                    ]
                                ){
                                    withEnv(["GOOGLE_APPLICATION_CREDENTIALS=${WORKSPACE}/gcp-sa_key.json"]) {
                                        node("xpaas-jenkins-slaves-${project}") {
                                            stage("GCloud Authentication for ${project}") {
                                                checkout scm
                                                vaultSecrets = [
                                                    [
                                                        $class: 'VaultSecret',
                                                        path: 'secret/xpaas/openshift/gcp/commonmerit-cpe-kcc-lle/inspec',
                                                        engineVersion: 1,
                                                        secretValues: [
                                                            [$class: 'VaultSecretValue', envVar: 'GCP_JSON_CREDS', vaultKey: 'key']
                                                        ]
                                                    ]
                                                ]
                                                wrap([$class: 'VaultBuildWrapper', vaultSecrets: vaultSecrets]) {
                                                    writeFile file: GOOGLE_APPLICATION_CREDENTIALS, text: GCP_JSON_CREDS
                                                    sh 'gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}'
                                                }
                                            }
                                            stage("Perform Inspec Testing for ${project}") {
                                                testResource("${project}")
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        parallel checks
                    }
                    setBuildStatus("InSpec testing passed", "SUCCESS")
                    cleanWs(
                        cleanWhenAborted: true,
                        cleanWhenFailure: true,
                        cleanWhenNotBuilt: true,
                        cleanWhenSuccess: true,
                        cleanWhenUnstable: true,
                        deleteDirs: true
                    )
                }
                catch (Exception e) {
                    setBuildStatus("InSpec testing failed", "FAILURE")
                    cleanWs(
                        cleanWhenAborted: true,
                        cleanWhenFailure: true,
                        cleanWhenNotBuilt: true,
                        cleanWhenSuccess: true,
                        cleanWhenUnstable: true,
                        deleteDirs: true
                    )
                    throw e
                }
            }
        }
    }
}

def testResource(String project_name) {
    dir("inspec") {
        sh """
        mkdir -p files
        touch ../test_vars/gcp_project/${project_name}/ignore.yml
        yq merge --allow-empty ../test_vars/gcp_project/${project_name}/*.yml >files/input.yml
        inspec exec . -t gcp:// --chef-license=accept-silent
        """
    }
}
