#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'

config =  yaml(content: inspec.profile.file('input.yml')).params
project = config.fetch('project')
project_name = project.fetch('name')

if config.key?('vpcs')
  vpcs = config.fetch('vpcs')
  vpcs.each do |_vpc_name, vpc_def|
    next unless vpc_def.key?('routerDef')

    vpc_def['routerDef'].each do |_router_name, router_def|
      next unless router_def.key?('ha_vpn_gateways_to_transit')

      # rubocop:disable Layout/LineLength
      router_def['ha_vpn_gateways_to_transit'].each do |tunnel_name, _tunnel_def|
        tunnel0 = tunnel_name + '-tu0-a'
        # hard coded to only test customer side of tunnel
        tunnel1 = tunnel_name + '-tu1-a'
        # hard coded to only test customer side of tunnel
        describe google_compute_vpn_tunnel(project: project_name,\
                                           region: router_def['region'],\
                                           name: tunnel0) do
          it { should exist }
          its('status') { should eq 'ESTABLISHED' }
        end
        describe google_compute_vpn_tunnel(project: project_name,\
                                           region: router_def['region'],\
                                           name: tunnel1) do
          it { should exist }
          its('status') { should eq 'ESTABLISHED' }
        end
      end
      # rubocop:enable Layout/LineLength
    end
  end
end
