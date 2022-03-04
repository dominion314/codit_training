#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
config = yaml(content: inspec.profile.file('input.yml')).params
project_id = config.fetch('project').fetch('name')
if config.key?('vpcs')
  vpcs = config.fetch('vpcs')
  vpcs.each do |vpc_name, vpc_def|
    vpc_def.fetch('subnets').each do |subnet_name, subnet_def|
      region_var = config.fetch('vpcs').fetch(vpc_name).fetch('subnets')
                         .fetch(subnet_name).fetch('region')
      subnet_def.fetch('permissions').each do |iam_type, email_list|
        email_list.each do |email|
          if iam_type == 'usersByEmail'
            member_type = 'user:'
          elsif iam_type == 'serviceAccountsByEmail'
            member_type = 'serviceAccount:'
          elsif iam_type == 'groupsByEmail'
            member_type = 'group:'
          end
          control "IAMPolicySubnets  #{project_id}, #{vpc_name}, #{subnet_name}"
          google_compute_subnetwork_iam_policy(project: project_id,
                                               region: region_var,
                                               name: subnet_name)
            .bindings.each do |binding|
            describe binding do
              its('role') { should eq 'roles/compute.networkUser' }
              its('members') { should include member_type + email }
            end
          end
        end
      end
    end
  end
end
