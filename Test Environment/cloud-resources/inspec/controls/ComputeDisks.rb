#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
if config.key?('computeDisks')
  compute_disks = config.fetch('computeDisks')
  compute_disks.each do |disk_name, disk_params|
    disk_zone = disk_params['zone']
    next if disk_params.key?('replicaZone')

    control "Compute disks #{disk_name} existance check"
    describe google_compute_disk(project: project_id,
                                 name: disk_name,
                                 zone: disk_zone) do
      it { should exist }
      if disk_params.key?('description')
        its('description') { should match disk_params['description'] }
      end
      if disk_params.key?('size')
        its('size_gb') { should match disk_params['size'].to_s }
      end
      if disk_params.key?('type')
        its('type') { should match disk_params['type'] }
      end
    end
  end
end
