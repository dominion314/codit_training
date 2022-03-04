#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'

config =  yaml(content: inspec.profile.file('input.yml')).params
project = config.fetch('project')
project_name = project.fetch('name')

default_fw = config.fetch('DefaultFirewall') if config.key?('DefaultFirewall')

if config.key?('vpcs')
  vpcs = config.fetch('vpcs')
  vpcs.each do |vpc_name, vpc_def|
    default_fw.each do |default_fw_name, default_fw_def|
      describe google_compute_firewall(project: project_name,
                                       name: vpc_name + '-' \
                                       + default_fw_name) do
        it { should exist }
        its('direction') { should eq default_fw_def['direction'] }
        its('priority') { should eq default_fw_def['priority'] }
      end
    end
    next unless vpc_def.key?('firewallRules')

    vpc_def['firewallRules'].each do |firewall_name, firewall_def|
      next if default_fw[firewall_name]

      describe google_compute_firewall(project: project_name,
                                       name: vpc_name + '-' + firewall_name) do
        it { should exist }
        its('direction') { should eq firewall_def['direction'] }
        its('priority') { should eq firewall_def['priority'] }
      end
    end
  end
end
