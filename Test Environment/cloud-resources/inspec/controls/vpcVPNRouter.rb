#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'

config =  yaml(content: inspec.profile.file('input.yml')).params
project = config.fetch('project')
project_name = project.fetch('name')

if config.key?('vpcs')
  vpcs = config.fetch('vpcs')
  # rubocop:disable Metrics/BlockLength
  vpcs.each do |_vpc_name, vpc_def|
    next unless vpc_def.key?('routerDef')

    asn_vars = config.fetch('ha_vpn_to_global_transit_asn')
    vpc_def['routerDef'].each do |router_name, router_def|
      x = 0
      describe google_compute_router(project: project_name,
                                     region: router_def['region'],
                                     name: router_name) do
        it { should exist }
        its('bgp.asn') { should eq asn_vars[project_name][router_name] }
        its('bgp.advertiseMode') { should eq router_def['advertiseMode'] }

        if vpc_def.key?('subnets')
          vpc_def['subnets'].each do |_subnet_name, subnet_def|
            next unless subnet_def['advertiseRoutes']

            x += 1
            if subnet_def.key?('secondary')
              subnet_def['secondary'].each do
                x += 1 # Add one to subnet count for each secondary
              end
            end
            next unless subnet_def.key?('gke')

            subnet_def['gke'].each do
              # Add two to subnet count for pod+service subnet per cluster
              x += 2
            end
          end
          its('bgp.advertised_ip_ranges.count') { should eq x }
        end
      end
    end
  end
  # rubocop:enable Metrics/BlockLength
end
