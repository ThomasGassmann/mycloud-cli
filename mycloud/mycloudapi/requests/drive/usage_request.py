import json
import time

from mycloud.mycloudapi.requests import Method, MyCloudRequest

REQUEST_URL = 'https://storage.prod.mdl.swisscom.ch/usage?nocache={}'


class UsageRequest(MyCloudRequest):

    def get_method(self):
        return Method.GET

    def get_request_url(self):
        return REQUEST_URL.format(int(time.time()))

    @staticmethod
    async def format_response(response):
        text = await response.text()
        json_data = json.loads(text)
        return json_data
