#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'

config =  yaml(content: inspec.profile.file('input.yml')).params
project = config.fetch('project')
project_name = project.fetch('name')

if config.key?('vpcs')
  vpcs = config.fetch('vpcs')
  vpcs.each do |vpc_name, vpc_def|
    describe google_compute_network(project: project_name, name: vpc_name) do
      it { should exist }
      its('auto_create_subnetworks') { should be false }
      its('routing_config.routing_mode') { should eq vpc_def['routingMode'] }
    end
    next unless vpc_def.key?('subnets')

    vpc_def['subnets'].each do |subnet_name, subnet_def|
      describe google_compute_subnetwork(project: project_name,
                                         region: subnet_def['region'],
                                         name: vpc_name + '-' + subnet_name) do
        it { should exist }
        its('ip_cidr_range') { should eq subnet_def['network']['ip'] }
        its('region') { should match subnet_def['region'] }
      end
    end
  end
end
