import json
import time
from mycloudapi.helper import get_object_id, raise_if_invalid_cloud_path
from mycloudapi.request import MyCloudRequest, Method


REQUEST_URL = 'https://storage.prod.mdl.swisscom.ch/changes/files/?p={}&$limit={}&nocache={}'


class ChangeRequest(MyCloudRequest):

    def __init__(self, object_resource: str, top: int):
        raise_if_invalid_cloud_path(object_resource)
        self.object_resource = object_resource
        self.top = top

    def get_method(self):
        return Method.GET

    def get_request_url(self):
        return REQUEST_URL.format(get_object_id(self.object_resource), self.top, time.time())

    @staticmethod
    def format_response(response):
        json_data = json.loads(response.text)
        return json_data
