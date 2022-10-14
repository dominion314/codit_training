#pylint: disable=import-error,C0301,C0303,C0114,C0411,C0103
import requests 
import argparse
import sys
import json

# Testing variables that can be helpful - eunomia being kubectl proxied
# gitRef = "master"
# gitRepo = "EnterpriseDevOps/CPE-GoogleCloud-Templates"
# eunomiaUrl = "http://localhost:8080/webhook/"

headers = {"Content-type": "application/json",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "User-Agent": "GitHub-Hookshot/d88a271",
                "X-GitHub-Delivery": "1a37afc2-97ee-11eb-9ffe-1b8ffb123724",
                "X-GitHub-Enterprise-Host": "github.commonmerit.com",
                "X-GitHub-Enterprise-Version": "2.21.5",
                "X-GitHub-Event": "push"}

payload =   {"ref": "refs/heads/replace-me",
                "before": "6113728f27ae82c7b1a177c8d03f9e96e0adf246",
                "after": "0000000000000000000000000000000000000000",
                "created": False,
                "deleted": True,
                "forced": False,
                "base_ref": None,
                "compare": "https://github.com/Codertocat/Hello-World/compare/6113728f27ae...000000000000",
                "commits": [],
                "head_commit": None,
                "repository": {
                    "id": 186853002,
                    "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
                    "name": "Hello-World",
                    "full_name": "replace-me",
                    "private": False,
                    "owner": {
                    "name": "Codertocat",
                    "email": "21031067+Codertocat@users.noreply.github.com",
                    "login": "Codertocat",
                    "id": 21031067,
                    "node_id": "MDQ6VXNlcjIxMDMxMDY3",
                    "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/Codertocat",
                    "html_url": "https://github.com/Codertocat",
                    "followers_url": "https://api.github.com/users/Codertocat/followers",
                    "following_url": "https://api.github.com/users/Codertocat/following{/other_user}",
                    "gists_url": "https://api.github.com/users/Codertocat/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/Codertocat/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/Codertocat/subscriptions",
                    "organizations_url": "https://api.github.com/users/Codertocat/orgs",
                    "repos_url": "https://api.github.com/users/Codertocat/repos",
                    "events_url": "https://api.github.com/users/Codertocat/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/Codertocat/received_events",
                    "type": "User",
                    "site_admin": False
                    },
                    "html_url": "https://github.com/Codertocat/Hello-World",
                    "description": None,
                    "fork": False,
                    "url": "https://github.com/Codertocat/Hello-World",
                    "forks_url": "https://api.github.com/repos/Codertocat/Hello-World/forks",
                    "keys_url": "https://api.github.com/repos/Codertocat/Hello-World/keys{/key_id}",
                    "collaborators_url": "https://api.github.com/repos/Codertocat/Hello-World/collaborators{/collaborator}",
                    "teams_url": "https://api.github.com/repos/Codertocat/Hello-World/teams",
                    "hooks_url": "https://api.github.com/repos/Codertocat/Hello-World/hooks",
                    "issue_events_url": "https://api.github.com/repos/Codertocat/Hello-World/issues/events{/number}",
                    "events_url": "https://api.github.com/repos/Codertocat/Hello-World/events",
                    "assignees_url": "https://api.github.com/repos/Codertocat/Hello-World/assignees{/user}",
                    "branches_url": "https://api.github.com/repos/Codertocat/Hello-World/branches{/branch}",
                    "tags_url": "https://api.github.com/repos/Codertocat/Hello-World/tags",
                    "blobs_url": "https://api.github.com/repos/Codertocat/Hello-World/git/blobs{/sha}",
                    "git_tags_url": "https://api.github.com/repos/Codertocat/Hello-World/git/tags{/sha}",
                    "git_refs_url": "https://api.github.com/repos/Codertocat/Hello-World/git/refs{/sha}",
                    "trees_url": "https://api.github.com/repos/Codertocat/Hello-World/git/trees{/sha}",
                    "statuses_url": "https://api.github.com/repos/Codertocat/Hello-World/statuses/{sha}",
                    "languages_url": "https://api.github.com/repos/Codertocat/Hello-World/languages",
                    "stargazers_url": "https://api.github.com/repos/Codertocat/Hello-World/stargazers",
                    "contributors_url": "https://api.github.com/repos/Codertocat/Hello-World/contributors",
                    "subscribers_url": "https://api.github.com/repos/Codertocat/Hello-World/subscribers",
                    "subscription_url": "https://api.github.com/repos/Codertocat/Hello-World/subscription",
                    "commits_url": "https://api.github.com/repos/Codertocat/Hello-World/commits{/sha}",
                    "git_commits_url": "https://api.github.com/repos/Codertocat/Hello-World/git/commits{/sha}",
                    "comments_url": "https://api.github.com/repos/Codertocat/Hello-World/comments{/number}",
                    "issue_comment_url": "https://api.github.com/repos/Codertocat/Hello-World/issues/comments{/number}",
                    "contents_url": "https://api.github.com/repos/Codertocat/Hello-World/contents/{+path}",
                    "compare_url": "https://api.github.com/repos/Codertocat/Hello-World/compare/{base}...{head}",
                    "merges_url": "https://api.github.com/repos/Codertocat/Hello-World/merges",
                    "archive_url": "https://api.github.com/repos/Codertocat/Hello-World/{archive_format}{/ref}",
                    "downloads_url": "https://api.github.com/repos/Codertocat/Hello-World/downloads",
                    "issues_url": "https://api.github.com/repos/Codertocat/Hello-World/issues{/number}",
                    "pulls_url": "https://api.github.com/repos/Codertocat/Hello-World/pulls{/number}",
                    "milestones_url": "https://api.github.com/repos/Codertocat/Hello-World/milestones{/number}",
                    "notifications_url": "https://api.github.com/repos/Codertocat/Hello-World/notifications{?since,all,participating}",
                    "labels_url": "https://api.github.com/repos/Codertocat/Hello-World/labels{/name}",
                    "releases_url": "https://api.github.com/repos/Codertocat/Hello-World/releases{/id}",
                    "deployments_url": "https://api.github.com/repos/Codertocat/Hello-World/deployments",
                    "created_at": 1557933565,
                    "updated_at": "2019-05-15T15:20:41Z",
                    "pushed_at": 1557933657,
                    "git_url": "git://github.com/Codertocat/Hello-World.git",
                    "ssh_url": "git@github.com:Codertocat/Hello-World.git",
                    "clone_url": "https://github.com/Codertocat/Hello-World.git",
                    "svn_url": "https://github.com/Codertocat/Hello-World",
                    "homepage": None,
                    "size": 0,
                    "stargazers_count": 0,
                    "watchers_count": 0,
                    "language": "Ruby",
                    "has_issues": True,
                    "has_projects": True,
                    "has_downloads": True,
                    "has_wiki": True,
                    "has_pages": True,
                    "forks_count": 1,
                    "mirror_url": None,
                    "archived": False,
                    "disabled": False,
                    "open_issues_count": 2,
                    "license": None,
                    "forks": 1,
                    "open_issues": 2,
                    "watchers": 0,
                    "default_branch": "master",
                    "stargazers": 0,
                    "master_branch": "master"
                },
                "pusher": {
                    "name": "Codertocat",
                    "email": "21031067+Codertocat@users.noreply.github.com"
                },
                "sender": {
                    "login": "Codertocat",
                    "id": 21031067,
                    "node_id": "MDQ6VXNlcjIxMDMxMDY3",
                    "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/Codertocat",
                    "html_url": "https://github.com/Codertocat",
                    "followers_url": "https://api.github.com/users/Codertocat/followers",
                    "following_url": "https://api.github.com/users/Codertocat/following{/other_user}",
                    "gists_url": "https://api.github.com/users/Codertocat/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/Codertocat/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/Codertocat/subscriptions",
                    "organizations_url": "https://api.github.com/users/Codertocat/orgs",
                    "repos_url": "https://api.github.com/users/Codertocat/repos",
                    "events_url": "https://api.github.com/users/Codertocat/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/Codertocat/received_events",
                    "type": "User",
                    "site_admin": False
                }
            }

def main():
    """
    Main entry point
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--eunomia_url", required=True, help="URL of Eunomia Service")
    arg_parser.add_argument("--git_ref", required=True, help="Branch name of GitLab push event")
    arg_parser.add_argument("--git_repo", required=True, help="Project name of GitLab push event")
    args = arg_parser.parse_args()

    payload["ref"] = "refs/heads/" + args.git_ref
    payload["repository"]["full_name"] = args.git_repo

    print("===============================================================")
    print("Eunomia Webhook Post URL: " + args.eunomia_url)
    print("Git Reference: " + args.git_ref)
    print("Git Repository: " + args.git_repo)
    print("Submited post ..........")

    try:
        response = requests.post(args.eunomia_url, data=json.dumps(payload), headers=headers)
        responseStatusCode = str(response.status_code)
        print("Status Code: " + responseStatusCode) 

    except requests.exceptions.RequestException as e:
        responseStatusCode = ""
        print("Request Error: " + str(e))

    if responseStatusCode == "200":
        print("Webhook Status: SUCCEEDED")
        print("===============================================================")
        sys.exit(0)
    else:
        print("Webhook Status: FAILED")
        print("===============================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
