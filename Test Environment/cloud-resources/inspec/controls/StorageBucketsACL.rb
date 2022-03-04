#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
if config.key?('storageBuckets')
  storage_config = config.fetch('storageBuckets')
  # rubocop:disable Metrics/BlockLength
  storage_config.each do |bucket_name, bucket_def|
    next unless bucket_def.key?('acls')

    acls = bucket_def.fetch('acls')
    acls.each do |entity_type, entity_def|
      if entity_type == 'primitiveRoles'
        entity_def.each do |project_number, roles_def|
          roles_def.each do |member, role|
            entity = 'project-' + member + '-' + project_number.to_s
            control 'Storage Access Control Lists'
            describe google_storage_bucket_acl(bucket: bucket_name,
                                               entity: entity) do
              its('role') { should eq role }
            end
          end
        end
      else
        entity_def.each do |member, role|
          if entity_type == 'usersByEmail'
            entity = 'user-' + member
          elsif entity_type == 'groupsByEmail'
            entity = 'group-' + member
          elsif entity_type == 'builtinGroups'
            entity = member
          end
          if !entity.nil? && !role.nil?
            control 'Storage Access Control Lists'
            describe google_storage_bucket_acl(bucket: bucket_name,
                                               entity: entity) do
              its('role') { should eq role }
            end
          else
            puts 'Warning: No valid acls found in input.yml'
          end
        end
      end
    end
  end
  # rubocop:enable Metrics/BlockLength
end
