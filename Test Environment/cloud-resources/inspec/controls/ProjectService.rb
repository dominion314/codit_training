#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config =  yaml(content: inspec.profile.file('input.yml')).params

project = config.fetch('project')
project_name = project.fetch('name')

if config.key?('serviceAPIs')
  service_apis = config.fetch('serviceAPIs')

  service_apis.each do |api_name, _api_def|
    control 'Check Service APIs'
    describe google_project_service(project: project_name, name: api_name) do
      it { should exist }
      its('state') { should cmp 'ENABLED' }
    end
  end
end
