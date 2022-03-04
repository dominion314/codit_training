#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project = config.fetch('project')

if project.key?('labels')
  labels = project.fetch('labels')
  describe google_project(project: project['name']) do
    its('labels') { should include labels }
  end
end
