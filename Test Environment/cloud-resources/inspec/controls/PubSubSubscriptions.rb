#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config =  yaml(content: inspec.profile.file('input.yml')).params

project = config.fetch('project')
project_name = project.fetch('name')
if config.key?('pubSubSubscriptions')
  subscriptions = config.fetch('pubSubSubscriptions')
  default_labels = (if config.key?('defaultLabels')
                      config.fetch('defaultLabels')
                    end)
  # rubocop:disable Metrics/BlockLength, Layout/LineLength
  subscriptions.each do |sub_name, sub_def|
    control 'pubSubScriptions'
    describe google_pubsub_subscription(project: project_name, name: sub_name) do
      it { should exist }
      its('topic') { should eq 'projects/' + project_name + '/topics/' + sub_def['topicName'] }
      if sub_def.key?('labels') && !default_labels.nil?
        all_labels = default_labels.merge(sub_def['labels'])
        its('labels') { should include all_labels }
      end
      if sub_def.key?('labels') && default_labels.nil?
        its('labels') { should include sub_def.key?('labels') }
      end
      if !sub_def.key?('labels') && !default_labels.nil?
        its('labels') { should include default_labels }
      end
      if sub_def.key?('ackDeadlineSeconds')
        its('ack_deadline_seconds') { should eq sub_def['ackDeadlineSeconds'] }
      end
      if sub_def.key?('messageRetentionDuration')
        its('message_retention_duration') { should eq sub_def['messageRetentionDuration'] }
      end
      if sub_def.key?('retainAckedMessages')
        if sub_def['retainAckedMessages'] == false # Google returns nil instead of false
          its('retain_acked_messages') { should eq sub_def['retainAckedMessages'] || nil }
        else
          its('retain_acked_messages') { should eq sub_def['retainAckedMessages'] }
        end
      end
      if sub_def.key?('expirationPolicy')
        expiration_policy = sub_def['expirationPolicy']
        unless expiration_policy['ttl'].nil?
          ttl_no_s = expiration_policy['ttl'].tr('s', '')
          ttl_format_decimal = format('%<ttl>0.3f', ttl: ttl_no_s)
          ttl_format_decimal_with_s = ttl_format_decimal + 's'
          its('expiration_policy.ttl') { should eq ttl_format_decimal_with_s }
        end
      end
      if sub_def.key?('pushConfig')
        push_config = sub_def['pushConfig']
        unless push_config['pushEndpoint'].nil?
          its('push_config.push_endpoint') { should eq push_config['pushEndpoint'] }
        end
        unless push_config['attributes'].nil?
          its('push_config.attributes') { should eq push_config['attributes'] }
        end
      end
    end
  end
  # rubocop:enable Metrics/BlockLength, Layout/LineLength
end
