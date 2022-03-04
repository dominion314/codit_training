#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
if config.key?('bigQueryDatasets')
  big_query_dataset_def = config.fetch('bigQueryDatasets')
  # rubocop:disable Metrics/BlockLength
  big_query_dataset_def.each do |dataset, dataset_params|
    data_set_name = dataset
    friendly_name = dataset_params['friendly_name']
    description = dataset_params['description']
    expiration = dataset_params['defaultTableExpirationMs']
    control "BigQuery Dataset #{data_set_name} existance check"
    describe google_bigquery_dataset(project: project_id,
                                     name: data_set_name) do
      it { should exist }
      its('friendly_name') { should eq friendly_name }
      its('description') { should eq description }
      its('name') { should eq data_set_name }
      its('default_table_expiration_ms') { should cmp expiration }
    end
    control "BigQuery Dataset #{data_set_name} access check"
    access_def = dataset_params.fetch('permissions')
    access_def.each do |acl_type_by_email, email_list|
      email_list.each do |email, roles_map|
        roles_map['roles'].each do |role|
          if role == 'roles/bigquery.dataOwner'
            role = 'OWNER'
          elsif role == 'roles/bigquery.dataViewer'
            role = 'READER'
          elsif role == 'roles/bigquery.dataEditor'
            role = 'WRITER'
          end
          if acl_type_by_email == 'usersByEmail'
            describe.one do
              google_bigquery_dataset(project: project_id, name: data_set_name)
                .access.each do |dataset_access|
                describe dataset_access do
                  its('role') { should eq role }
                  its('user_by_email') { should eq email }
                end
              end
            end
          end
          if acl_type_by_email == 'serviceAccountsByEmail'
            describe.one do
              google_bigquery_dataset(project: project_id, name: data_set_name)
                .access.each do |dataset_access|
                describe dataset_access do
                  its('role') { should eq role }
                  its('user_by_email') { should eq email }
                end
              end
            end
          end
          next unless acl_type_by_email == 'groupsByEmail'

          describe.one do
            google_bigquery_dataset(project: project_id, name: data_set_name)
              .access.each do |dataset_access|
              describe dataset_access do
                its('role') { should eq role }
                its('group_by_email') { should eq email }
              end
            end
          end
        end
      end
    end
  end
  # rubocop:enable Metrics/BlockLength
end
