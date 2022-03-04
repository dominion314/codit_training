#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
# rubocop:disable Metrics/BlockLength
if config.key?('pubSubTopics')
  pubsub_topics = config.fetch('pubSubTopics')
  pubsub_topics.each do |topic_name, topic_def|
    next unless topic_def.key?('permissions')

    permissions = topic_def.fetch('permissions')
    control "PubSub Topic IAM: #{topic_name} in project: #{project_id}"
    google_pubsub_topic_iam_policy(project: project_id, name: topic_name)
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
# rubocop:enable Metrics/BlockLength
