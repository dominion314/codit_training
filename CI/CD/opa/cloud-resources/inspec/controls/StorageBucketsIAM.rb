#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
# rubocop:disable Metrics/BlockLength
if config.key?('storageBuckets')
  storage_buckets = config.fetch('storageBuckets')
  storage_buckets.each do |bucket_name, bucket_def|
    next unless bucket_def.key?('permissions')

    permissions = bucket_def.fetch('permissions')
    control 'Storage Bucket IAM:' do
      title 'Role then member bindings for each bucket'
      describe google_storage_bucket_iam_policy(bucket: bucket_name) do
        it { should exist }
      end

      google_storage_bucket_iam_policy(bucket: bucket_name)
        .bindings.each do |binding|
        describe.one do
          describe binding do
            permissions.each do |entity_type, entity_def|
              entity_def.each do |member, role_def|
                roles = role_def.fetch('roles')
                roles.each do |role|
                  next unless binding.role == "roles/#{role}"

                  its('role') { should include "roles/#{role}" }
                  if entity_type == 'usersByEmail'
                    its('members') { should include "user:#{member}" }
                  end
                  if entity_type == 'groupsByEmail'
                    its('members') { should include "group:#{member}" }
                  end
                  if entity_type == 'serviceAccountsByEmail'
                    its('members') { should include "serviceAccount:#{member}" }
                  end
                end
              end
            end
          end
        end
      end
    end
  end
end
# rubocop:enable Metrics/BlockLength
