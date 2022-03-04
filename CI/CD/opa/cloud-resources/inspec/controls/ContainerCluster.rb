#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
if config.key?('clusters')
  container_cluster = config.fetch('clusters')
  # rubocop:disable Metrics/BlockLength
  # rubocop:disable Layout/LineLength
  container_cluster.each do |cluster|
    cluster_name = cluster['name']
    location_name = cluster['location']
    network = cluster['network']
    network_split = network.split('/')
    subnetwork = cluster['subnetwork']
    subnetwork_split = subnetwork.split('/')

    control "Check #{cluster} Configuration"
    describe google_container_cluster(project: project_id,
                                      location: location_name,
                                      name: cluster_name) do
      it { should exist }
      condition = true
      if cluster.key?('horizontalPodAutoscaling')
        hor_pod_auto = cluster.fetch('horizontalPodAutoscaling')
        condition = nil unless hor_pod_auto['disabled'].nil?
        its('addons_config.horizontal_pod_autoscaling.disabled') { should eq condition }
      end
      condition = true
      if cluster.key?('httpLoadBalancing')
        http_load_balance = cluster.fetch('httpLoadBalancing')
        condition = nil unless http_load_balance['disabled'].nil?
        its('addons_config.http_load_balancing.disabled') { should eq condition }
      end
      condition = true
      if cluster.key?('networkPolicyConfig')
        network_policy_config = cluster.fetch('networkPolicyConfig')
        condition = nil unless network_policy_config['disabled'].nil?
        its('addons_config.network_policy_config.disabled') { should eq condition }
      end
      if cluster.key?('defaultMaxPodsPerNode')
        its('default_max_pods_constraint.max_pods_per_node') { should eq cluster['defaultMaxPodsPerNode'] }
      end
      if cluster.key?('enableKubernetesAlpha')
        its('enable_kubernetes_alpha') { should eq cluster['enableKubernetesAlpha'] }
      end
      if cluster.key?('initialNodeCount')
        its('initial_node_count') { should eq cluster['initialNodeCount'] }
      end
      its('ip_allocation_policy.cluster_secondary_range_name') { should eq cluster['podSubnetwork'] }
      its('ip_allocation_policy.services_secondary_range_name') { should eq cluster['serviceSubnetwork'] }
      if cluster.key?('loggingService')
        its('logging_service') { should eq cluster['loggingService'] }
      end
      if cluster.key?('minMasterVersion')
        its('min_master_version') { should eq cluster['minMasterVersion'] }
      end
      if cluster.key?('monitoringService')
        its('monitoring_service') { should eq cluster['monitoringService'] }
      end
      if cluster.key?('network')
        its('network') { should eq network_split[network_split.length - 1] }
      end
      if cluster.key?('nodeVersion')
        its('current_node_version') { should eq cluster['nodeVersion'] }
      end
      if cluster.key?('nodeLocations')
        node_locations = cluster.fetch('nodeLocations')
        its('locations.sort') { should cmp node_locations.sort }
      end
      if cluster.key?('subnetwork')
        its('subnetwork') { should eq subnetwork_split[subnetwork_split.length - 1] }
      end
      if cluster.key?('masterIpv4CidrBlock')
        its('private_cluster_config.master_ipv4_cidr_block') { should eq cluster['masterIpv4CidrBlock'] }
      end
      if cluster.key?('releaseChannel')
        its('release_channel.channel') { should eq cluster['releaseChannel'] }
      end
    end
    next unless cluster.key?('nodePools')

    container_node_pool = cluster.fetch('nodePools')
    container_node_pool.each do |nodepool|
      describe google_container_node_pool(project: project_id,
                                          location: nodepool['location'],
                                          cluster_name: cluster_name,
                                          nodepool_name: nodepool['name']) do
        it { should exist }
        its('autoscaling.min_node_count') { should eq nodepool['minNodeCount'] }
        its('autoscaling.max_node_count') { should eq nodepool['maxNodeCount'] }
        if nodepool.key?('initialNodeCount')
          its('initial_node_count') { should eq nodepool['initialNodeCount'] }
        end
        if nodepool.key?('autoRepair')
          its('management.auto_repair') { should eq nodepool['autoRepair'] }
        end
        if nodepool.key?('autoUpgrade')
          its('management.auto_upgrade') { should eq nodepool['autoUpgrade'] }
        end
        if nodepool.key?('autoRepair')
          its('management.auto_repair') { should eq nodepool['autoRepair'] }
        end
        if nodepool.key?('maxPodsPerNode')
          its('max_pods_constraint.max_pods_per_node') { should eq nodepool['maxPodsPerNode'].to_s }
        end
        if nodepool.key?('diskSizeGb')
          its('config.disk_size_gb') { should eq nodepool['diskSizeGb'] }
        end
        if nodepool.key?('diskType')
          its('config.disk_type') { should eq nodepool['diskType'] }
        end
        if nodepool.key?('machineType')
          its('config.machine_type') { should eq nodepool['machineType'] }
        end
        if nodepool.key?('imageType')
          its('config.image_type') { should eq nodepool['imageType'] }
        end
        if nodepool.key?('oauthScopes')
          oauth_scopes = nodepool.fetch('oauthScopes')
          its('config.oauth_scopes.sort') { should cmp oauth_scopes.sort }
        end
      end
    end
  end
end
# rubocop:enable Metrics/BlockLength
# rubocop:enable Layout/LineLength
