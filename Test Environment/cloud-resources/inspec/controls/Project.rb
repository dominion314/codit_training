#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config =  yaml(content: inspec.profile.file('input.yml')).params
project = config.fetch('project')

if project['managed']
  control 'Validate project configurations'
  describe google_compute_project_info(project: project['name']) do
    it { should exist }
  end
  if project.key?('folderId')
    describe google_project(project: project['name']) do
      its('parent.type') { should eq 'folder' }
      its('parent.id') { should eq project['folderId'] }
    end
  end
  if project.key?('labels')
    labels = project.fetch('labels')
    describe google_project(project: project['name']) do
      its('labels') { should include labels }
    end
  end
  if project.key?('defaultNetwork')
    if project['defaultNetwork']
      describe google_compute_network(project: project['name'],
                                      name: 'default') do
        it { should exist }
      end
    end
  end
end
