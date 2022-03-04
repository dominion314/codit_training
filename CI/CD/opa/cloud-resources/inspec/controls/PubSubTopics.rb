#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
if config.key?('pubSubTopics')
  pubsub_topics = config.fetch('pubSubTopics')
  pubsub_topics.each do |topic_name, _topic_def|
    control "PubSub topic #{topic_name} existance check for #{project_id}"
    describe google_pubsub_topic(project: project_id, name: topic_name) do
      it { should exist }
    end
  end
end
