from os import system
import yaml
import requests # pip3 install requests
import json

class CommentPrint:
    def __init__(self, token, merge_request_id, project_id, base_url='https://gitlab.com/api/v4/'):
        self.base_url = base_url
        self.project_id = project_id
        self.merge_request_id = merge_request_id
        self.token = token
        self.anchor = ""

        url = self.base_url + "projects/{}/merge_requests/{}/notes?body=".format(self.project_id, self.merge_request_id)
        headers = {'PRIVATE-TOKEN' : self.token}
        response = requests.request("GET", url, headers=headers)
        self.posted_comments = json.loads(response.text)

        if 'message' in self.posted_comments:
            if self.posted_comments['message'] == '401 Unauthorized':
                print("Error 401 returned, token is invalid.")
                print(self.posted_comments['message'])
                exit()

    def write_to_comment(self, comment):
        """Creates and appends MR comment."""
        if self.anchor != "":
            payload = {"body": self.get_comment(self.anchor) + '<BR>' + comment}
            url = self.base_url + "projects/{}/merge_requests/{}/notes/{}".format(self.project_id, self.merge_request_id, self.anchor)
            response = requests.request("PUT", url, headers={'PRIVATE-TOKEN' : self.token}, data=payload)
        else:
            try:
                url = self.base_url + "projects/{}/merge_requests/{}/notes".format(self.project_id, self.merge_request_id)
                response = requests.request("POST", url, headers={'PRIVATE-TOKEN' : self.token}, data={"body": comment})
                json_response = json.loads(response.text)
                self.anchor = json_response['id']
            except KeyError as try_error:
                print("Error, unable to post:", try_error)
                print("json_response=",json_response)

    def post_comment(self, comment):
        """Post a Message to a Merge Request"""
        try:
            url = self.base_url + "projects/{}/merge_requests/{}/notes".format(self.project_id, self.merge_request_id)
            response = requests.request("POST", url, headers={'PRIVATE-TOKEN' : self.token}, data={"body": comment})
            json_response = json.loads(response.text)
            print('Inserted Comment Anchor', json_response['id'])
            self.anchor = json_response['id']
        except KeyError as try_error:
            print("Error, unable to post:", try_error)
            print("json_response=",json_response)

    def append_comment_by_id(self, comment_id, comment):
        """Append a Message to a Merge Request"""
        payload = {"body": self.get_comment(comment_id) + '<BR>' + comment}
        url = self.base_url + "projects/{}/merge_requests/{}/notes/{}".format(self.project_id, self.merge_request_id, comment_id)
        requests.request("PUT", url, headers={'PRIVATE-TOKEN' : self.token}, data=payload)
        #json_response = json.loads(response.text)

    def replace_comment_by_id(self, comment_id, comment):
        """Replace a Message to a Merge Request"""
        payload = {"body": comment}
        url = self.base_url + "projects/{}/merge_requests/{}/notes/{}".format(self.project_id, self.merge_request_id, comment_id)
        requests.request("PUT", url, headers={'PRIVATE-TOKEN' : self.token}, data=payload)
        #json_response = json.loads(response.text)

    def get_comment(self, comment_id):
        """Get a Message to a Merge Request"""
        url = self.base_url + "projects/{}/merge_requests/{}/notes/{}".format(self.project_id, self.merge_request_id, comment_id)
        headers = {'PRIVATE-TOKEN' : self.token}
        response = requests.request("GET", url, headers=headers)
        json_response= json.loads(response.text)
        return json_response['body']
