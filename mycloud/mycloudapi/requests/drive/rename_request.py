import json

from mycloud.common import get_string_generator, sanitize_path
from mycloud.mycloudapi.object_resource_builder import ObjectResourceBuilder
from mycloud.mycloudapi.requests import Method, MyCloudRequest

REQUEST_URL = 'https://storage.prod.mdl.swisscom.ch/commands/rename'


class RenameRequest(MyCloudRequest):
    def __init__(self, source: str, destination: str, is_file: bool):
        self._destination = sanitize_path(
            destination, force_dir=not is_file, force_file=is_file)
        self._source = sanitize_path(
            source, force_dir=not is_file, force_file=is_file)

    def get_method(self):
        return Method.PUT

    def get_request_url(self):
        return REQUEST_URL

    def get_data_generator(self):
        req = {
            'Source': self._source,
            'Destination': self._destination
        }

        req_json = json.dumps(req)
        return get_string_generator(req_json)
