import json
from mycloud.mycloudapi.helper import get_object_id, raise_if_invalid_cloud_path
from mycloud.mycloudapi.request import MyCloudRequest, Method


REQUEST_URL = 'https://storage.prod.mdl.swisscom.ch/metadata?p='


class MetadataRequest(MyCloudRequest):
    def __init__(self, object_resource: str, ignore_not_found=False, ignore_bad_request=False):
        if not object_resource.endswith('/'):
            object_resource += '/'
        raise_if_invalid_cloud_path(object_resource)
        self.object_resource = object_resource
        self.ignore_404 = ignore_not_found
        self.ignore_400 = ignore_bad_request

    def get_method(self):
        return Method.GET

    def get_request_url(self):
        resource = get_object_id(self.object_resource)
        return REQUEST_URL + resource

    def ignore_not_found(self):
        return self.ignore_404

    def ignore_bad_request(self):
        return self.ignore_400

    def is_query_parameter_access_token(self):
        return True

    @staticmethod
    def format_response(response):
        if response.status_code == 404:
            return ([], [])
        json_data = json.loads(response.text)
        files = MetadataRequest._get_files(json_data)
        dirs = MetadataRequest._get_directories(json_data)
        return (dirs, files)

    @staticmethod
    def _get_files(json):
        if 'Files' in json:
            files = json['Files']
            return files
        return []

    @staticmethod
    def _get_directories(json):
        if 'Directories' in json:
            directories = json['Directories']
            return directories
        return []