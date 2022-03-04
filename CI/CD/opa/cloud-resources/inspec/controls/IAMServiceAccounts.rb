#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
if config.key?('iamServiceAccounts')
  sa_def = config.fetch('iamServiceAccounts')
  sa_def.each do |sa, params|
    name = sa
    display_name = params['displayName']
    # rubocop:disable Layout/LineLength
    control 'Service Accounts {{ account.name }} for {{ project.name }} {{ ns.count }}'
    describe google_service_account(name: "projects/#{project_id}/serviceAccounts/#{name}@#{project_id}.iam.gserviceaccount.com") do
      its('display_name') { should eq display_name }
      its('project_id') { should eq project_id }
    end
    # rubocop:enable Layout/LineLength
  end
end
