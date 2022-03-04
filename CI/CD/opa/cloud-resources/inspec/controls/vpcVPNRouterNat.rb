#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'

config =  yaml(content: inspec.profile.file('input.yml')).params
project = config.fetch('project')
project_name = project.fetch('name')

if config.key?('vpcs')
  vpcs = config.fetch('vpcs')
  # rubocop:disable Metrics/BlockLength, Layout/LineLength
  vpcs.each do |_vpc_name, vpc_def|
    next unless vpc_def.key?('routerDef')

    vpc_def['routerDef'].each do |router_name, router_def|
      next unless router_def.key?('outbound_nat_gateway')

      describe google_compute_router_nat(project: project_name,
                                         region: router_def['region'],
                                         name: router_def['outbound_nat_gateway']['name'],
                                         router: router_name) do
        it { should exist }
        its('nat_ip_allocate_option') { should cmp 'AUTO_ONLY' }
        # rubocop:disable Style/MultilineTernaryOperator,
        !router_def['outbound_nat_gateway']['min_ports_per_vm'].nil? ? \
          (its('min_ports_per_vm') { should cmp router_def['outbound_nat_gateway']['min_ports_per_vm'] }) : \
          (its('min_ports_per_vm') { should cmp '64' })
        !router_def['outbound_nat_gateway']['tcp_est_timeout'].nil? ? \
          (its('tcp_established_idle_timeout_sec') { should cmp router_def['outbound_nat_gateway']['tcp_est_timeout'] }) : \
          (its('tcp_established_idle_timeout_sec') { should cmp '1200' })
        !router_def['outbound_nat_gateway']['tcp_trans_timeout'].nil? ? \
          (its('tcp_transitory_idle_timeout_sec') { should cmp router_def['outbound_nat_gateway']['tcp_trans_timeout'] }) : \
          (its('tcp_transitory_idle_timeout_sec') { should cmp '30' })
        !router_def['outbound_nat_gateway']['udp_timeout'].nil? ? \
          (its('udp_idle_timeout_sec') { should cmp router_def['outbound_nat_gateway']['udp_timeout'] }) : \
          (its('udp_idle_timeout_sec') { should cmp '30' })
        !router_def['outbound_nat_gateway']['icmp_timeout'].nil? ? \
          (its('icmp_idle_timeout_sec') { should cmp router_def['outbound_nat_gateway']['icmp_timeout'] }) : \
          (its('icmp_idle_timeout_sec') { should cmp '30' })
      end
    end
  end
  # rubocop:enable Metrics/BlockLength, Layout/LineLength, Style/MultilineTernaryOperator
end
