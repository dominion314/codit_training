#!/usr/bin/env groovy
@Library("openshift-operations@master") _
import com.commonmerit.xpaas.openshift.*

void setBuildStatus(String message, String state, String context) {
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
            context: "${context}"
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

def runConfigValidation(String context) {
    def checks = [:]
    def clusterList = defaults.getClusterList([clusterConfigDir:".", noCheckoutFirst:true])
    def exclusions = readFile('tests/config-validation/exclusions.txt')
    String responseTime = "30"
    stash name: "workspace-stash", includes: "**/*"
    for (int x = 0; x < clusterList.size(); x++) {
        // https://issues.jenkins-ci.org/browse/JENKINS-38268
        def cluster = clusterList[x]
        if (!(cluster =~ exclusions)) {
            def podName = "config-validation-${BRANCH_NAME}-${BUILD_NUMBER}"
            checks["${cluster}-config-validation"] = {
                podTemplate(
                    cloud: 'xpaas-jenkins-slaves',
                    name: podName,
                    label: podName,
                    namespace: 'xpaas-jenkins-slaves',
                    nodeUsageMode: 'EXCLUSIVE',
                    idleMinutes: 1,
                    slaveConnectTimeout: 600,
                    activeDeadlineSeconds: 3600,
                    containers: [
                        containerTemplate(
                            name: 'jnlp',
                            alwaysPullImage: true,
                            image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-xpaas-operations-311:latest",
                            resourceRequestCpu: '1',
                            resourceRequestMemory: '256Mi'
                        )
                    ]
                ) {
                    node(podName) {
                        unstash name: "workspace-stash"
                        dir('tests/config-validation/openshift-resources-jinja-processing') {
                            git branch: "master",
                                credentialsId: 'github-pzxpaas',
                                url: 'https://github.commonmerit.com/Ansible/openshift-resources-jinja-processing'
                        }
                        sh "ansible-playbook tests/config-validation/validate-config.yml \
                                            -e cluster_name=${cluster} -e dump_location=dump -T ${responseTime}"
                        stash name: cluster, includes: "**/*"
                    }
                }
            }
        }
    }

    try {
        parallel checks
        setBuildStatus("Config validation passed", "SUCCESS", context)
    } catch (Exception e) {
        setBuildStatus("Config validation failed", "FAILURE", context)
        throw e
    }

}

def runProductionChangeCheck(String context) {
    def checks = [:]
    def impactedClusters = []
    def clusterList = defaults.getClusterList([clusterConfigDir:".", noCheckoutFirst:true])
    def exclusions = readFile('tests/config-validation/exclusions.txt')
    def config_validation_file_content = libraryResource('./config_validation.py')
    stash name: "workspace-stash", includes: "**/*"
    for (int x = 0; x < clusterList.size(); x++) {
        // https://issues.jenkins-ci.org/browse/JENKINS-38268
        def cluster = clusterList[x]
        if (!(cluster =~ exclusions) && cluster.contains('prd')) {
            def podName = "config-production-validation-${BRANCH_NAME}-${BUILD_NUMBER}"
            checks["${cluster}-prod-check"] = {
                podTemplate(
                    cloud: 'xpaas-jenkins-slaves',
                    name: podName,
                    label: podName,
                    namespace: 'xpaas-jenkins-slaves',
                    nodeUsageMode: 'EXCLUSIVE',
                    idleMinutes: 1,
                    slaveConnectTimeout: 600,
                    activeDeadlineSeconds: 3600,
                    containers: [
                        containerTemplate(
                            name: 'jnlp',
                            alwaysPullImage: true,
                            image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-ansible-installer:latest",
                            resourceRequestCpu: '2',
                            resourceRequestMemory: '256Mi'
                        )
                    ]
                ) {
                    node(podName) {
                        unstash name: "workspace-stash"
                        def workspace_dir = env.WORKSPACE.replace("/" + env.WORKSPACE.split("/")[-1], "")
                        def master_config_path = workspace_dir + "/openshift-cluster-config-master"
                        dir("${workspace_dir}/openshift-resources-jinja-processing") {
                            git branch: "master",
                                credentialsId: 'github-pzxpaas',
                                url: 'https://github.commonmerit.com/Ansible/openshift-resources-jinja-processing'
                        }

                        dir(master_config_path) {
                            git branch: "master",
                                credentialsId: 'github-pzxpaas',
                                url: 'https://github.commonmerit.com/xPaaS-Operations/openshift-cluster-config'
                        }
                        dir(workspace_dir){
                            writeFile file: 'config_validation.py', text:config_validation_file_content

                            def statusCode = sh(script: "python3 config_validation.py --master_config_path ${master_config_path} " +
                                    "--pr_config_path ${env.WORKSPACE} --cluster_name ${cluster}", returnStatus: true)

                            if(statusCode == 2) {
                                impactedClusters.add(cluster)
                                error "Affects production cluster: ${cluster}"
                            } else if(statusCode != 0){
                                error "Error on cluster ${cluster}"
                            }
                        }
                    }
                }
            }
        }
    }
    try {
        parallel checks
        setBuildStatus("Change doesn't affect production clusters", "SUCCESS", context)
    } catch (Exception e) {
        if(impactedClusters) {
            print("Change affects production clusters:\n" + impactedClusters.join("\n"))
            setBuildStatus("Change affects production clusters", "FAILURE", context)
        }
        throw e
    }
}

def runYamlLint(String context){
    def checks = [:]
    def clusterList = defaults.getClusterList([clusterConfigDir:".", noCheckoutFirst:true])
    def exclusions = readFile('tests/config-validation/exclusions.txt')
    def config = libraryResource('./yamllint_config.yml')
    for (int x = 0; x < clusterList.size(); x++) {
        def cluster = clusterList[x]
        if (!(cluster =~ exclusions)){
              def podName = "config-yaml-validation-${BRANCH_NAME}-${BUILD_NUMBER}"
              checks["${cluster}-yaml-lint"] = {
                  podTemplate(
                      cloud: 'xpaas-jenkins-slaves',
                      name: podName,
                      label: podName,
                      namespace: 'xpaas-jenkins-slaves',
                      nodeUsageMode: 'EXCLUSIVE',
                      idleMinutes: 1,
                      slaveConnectTimeout: 600,
                      activeDeadlineSeconds: 3600,
                      containers: [
                          containerTemplate(
                              name: 'jnlp',
                              alwaysPullImage: true,
                              image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-linters:latest",
                              resourceRequestCpu: '2',
                              resourceRequestMemory: '128Mi'
                          )
                      ]
                  ) {
                      node(podName) {
                          unstash name: cluster
                          writeFile file: 'config.yml', text:config
                          // yamllint exits with 2 when there are any warnings
                          sh("""
                          yamllint -c ./config.yml ./tests/config-validation/dump
                          if [ \$? -eq 2 ]; then exit 0; fi
                          """)
                          }
                      }
              }
        }
    }
    try {
        parallel checks
        setBuildStatus("Config yaml linting passed", "SUCCESS", context)
    } catch (Exception e) {
        setBuildStatus("Config yaml linting failed", "FAILURE", context)
        throw e
    }
}

def runPromLint(String context){
    def checks = [:]
    def clusterList = defaults.getClusterList([clusterConfigDir:".", noCheckoutFirst:true])
    def exclusions = readFile('tests/config-validation/exclusions.txt')
    for (int x = 0; x < clusterList.size(); x++) {
        def cluster = clusterList[x]
        if (!(cluster =~ exclusions)){
              def podName = "config-prometheus-validation-${BRANCH_NAME}-${BUILD_NUMBER}"
              checks["${cluster}-prom-lint"] = {
                  podTemplate(
                      cloud: 'xpaas-jenkins-slaves',
                      name: podName,
                      label: podName,
                      namespace: 'xpaas-jenkins-slaves',
                      nodeUsageMode: 'EXCLUSIVE',
                      idleMinutes: 1,
                      slaveConnectTimeout: 600,
                      activeDeadlineSeconds: 3600,
                      containers: [
                          containerTemplate(
                              name: 'jnlp',
                              alwaysPullImage: true,
                              image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-linters:latest",
                              resourceRequestCpu: '200m',
                              resourceRequestMemory: '128Mi'
                          )
                      ]
                  ) {
                      node(podName) {
                          unstash name: cluster
                          sh("""
                          if [[ -d "tests/config-validation/dump/PrometheusRule" ]]; then
                              for filename in tests/config-validation/dump/PrometheusRule/*.yml; do
                                  yq read \$filename spec > output
                                  promtool check rules output
                              done
                          fi
                          if [[ -d "tests/config-validation/dump/alertmanager-configuration" ]]; then
                              for filename in tests/config-validation/dump/alertmanager-configuration/*.yml; do
                                  amtool check-config \$filename
                              done
                          fi
                          """)
                      }
                    }
              }
        }
    }
    try {
        parallel checks
        setBuildStatus("Prometheus rules, Alertmanager linting passed", "SUCCESS", context)
    } catch (Exception e) {
        setBuildStatus("Prometheus rules, Alertmanager linting failed", "FAILURE", context)
        throw e
    }
}

def call() {
    podTemplate(
        cloud: 'xpaas-jenkins-slaves',
        name: "config-validation-runner-${BRANCH_NAME}-${BUILD_NUMBER}",
        label: "config-validation-runner-${BRANCH_NAME}-${BUILD_NUMBER}",
        namespace: 'xpaas-jenkins-slaves',
        serviceAccount: 'jenkins',
        nodeUsageMode: 'EXCLUSIVE',
        idleMinutes: 1,
        slaveConnectTimeout: 600,
        activeDeadlineSeconds: 3600,
        containers: [
            containerTemplate(
                name: 'jnlp',
                image: "docker-registry.default.svc:5000/k-images/k-rhel7-jenkins-slave-linters:latest",
                alwaysPullImage: true,
                resourceRequestCpu: '1',
                resourceRequestMemory: '128Mi'
            )
        ]
    ) {
        ansiColor('xterm') {
            node ("config-validation-runner-${BRANCH_NAME}-${BUILD_NUMBER}") {
                checkout scm
                String configValidationContext = "Config Validation"
                String configYamlLinterContext = "Config Yaml Linter"
                String configPromLinterContext = "Prometheus Rules, Alertmanager Config Check"
                String productionCheckContext = "Production Change Check"

                stage(configValidationContext){
                    setBuildStatus("Waiting for ${configValidationContext} to finish first", "PENDING", configYamlLinterContext)
                    setBuildStatus("Waiting for ${configValidationContext} to finish first", "PENDING", configPromLinterContext)
                    setBuildStatus("Waiting for ${configValidationContext} to finish first", "PENDING", productionCheckContext)
                    setBuildStatus("Running ${configValidationContext}", "PENDING", configValidationContext)
                    runConfigValidation(configValidationContext)
                }

                stage("${configYamlLinterContext}, ${configPromLinterContext}, ${productionCheckContext}"){
                    parallel(
                        "${configYamlLinterContext}": {
                            stage(configYamlLinterContext) {
                                runYamlLint(configYamlLinterContext)
                            }
                        },
                        "${configPromLinterContext}": {
                            stage(configPromLinterContext) {
                                runPromLint(configPromLinterContext)
                            }
                        },
                        "${productionCheckContext}": {
                            stage(productionCheckContext) {
                                runProductionChangeCheck(productionCheckContext)
                            }
                        }
                    )
                }

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
