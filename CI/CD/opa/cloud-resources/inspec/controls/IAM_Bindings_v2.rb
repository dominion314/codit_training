#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
# rubocop:disable Metrics/BlockLength
if config.key?('iamPolicyMembersV2')
  iam_defs = config.fetch('iamPolicyMembersV2')
  iam_defs.each do |iam_resource_type, members_map|
    members_map.each do |member, roles_list|
      roles_list.each do |role_detail|
        if iam_resource_type == 'usersByEmail'
          member_type = 'user:'
        elsif iam_resource_type == 'serviceAccountsByEmail'
          member_type = 'serviceAccount:'
        elsif iam_resource_type == 'groupsByEmail'
          member_type = 'group:'
        end
        control "IAM Member Bindings for #{project_id}"
        # rubocop:disable Layout/LineLength
        role = if role_detail.key?('OrgId')
                 "organizations/#{role_detail['OrgId']}/roles/#{role_detail['role']}"
               else
                 "roles/#{role_detail['role']}"
               end
        if role_detail.key?('condition')
          condition = role_detail.fetch('condition')
          title = condition['title']
          expression = condition['expression']
          describe google_project_iam_binding(project: project_id, role: role, condition: { title: title }) do
            its('members') { should include member_type + member }
            its('condition.title') { should cmp title }
            its('condition.expression') { should cmp expression }
          end
        else
          describe google_project_iam_binding(project: project_id, role: role) do
            its('members') { should include member_type + member }
          end
        end
        # rubocop:enable Layout/LineLength
      end
    end
  end
end
# rubocop:enable Metrics/BlockLength
