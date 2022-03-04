#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
if config.key?('iamPolicyMembers')
  iam_defs = config.fetch('iamPolicyMembers')
  iam_defs.each do |iam_resource_type, members_map|
    members_map.each do |member, role_list|
      role_list['roles'].each do |role|
        if iam_resource_type == 'usersByEmail'
          member_type = 'user:'
        elsif iam_resource_type == 'serviceAccountsByEmail'
          member_type = 'serviceAccount:'
        elsif iam_resource_type == 'groupsByEmail'
          member_type = 'group:'
        end
        control "IAM_Bindings for #{project_id}"
        # rubocop:disable Layout/LineLength
        describe google_project_iam_binding(project: project_id, role: "roles/#{role}") do
          its('members') { should include member_type + member }
        end
        # rubocop:enable Layout/LineLength
      end
    end
  end
end
