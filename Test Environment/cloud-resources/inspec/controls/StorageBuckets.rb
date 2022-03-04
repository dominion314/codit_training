#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
if config.key?('storageBuckets')
  storage_config = config.fetch('storageBuckets')
  storage_config.each do |bucket_name, bucket_def|
    control "Bucket existance #{bucket_name}"
    describe google_storage_bucket(name: bucket_name) do
      it { should exist }
      if bucket_def.key?('location')
        location = bucket_def.fetch('location').upcase
        its('location') { should eq location }
      end
      if bucket_def.key?('storageClass')
        storage_class = bucket_def.fetch('storageClass')
        its('storage_class') { should eq storage_class }
      else
        its('storage_class') { should eq 'STANDARD' }
      end
      if bucket_def.key?('retentionPolicy')
        retention_policy = bucket_def.fetch('retentionPolicy')
        retention_policy.each do |policy_key, value|
          if policy_key == 'isLocked'
            its('retention_policy.is_locked') { should eq value }
          end
          if policy_key == 'retentionPeriod'
            its('retention_policy.retention_period') { should eq value.to_s }
          end
        end
      end
    end
  end
end
