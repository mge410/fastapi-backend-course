import os
from enum import Enum

import requests
from requests import Response

from gateways.BaseHttpClient import BaseHttpClient


class StorageHttpMethods(Enum):
    GET = "GET"
    PUT = "PUT"


class StorageHttpClient(BaseHttpClient):
    @property
    def url(self) -> str:
        return f"https://api.jsonbin.io/v3/b/{os.getenv('JSON_BIN_ID')}"

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "X-Master-Key": os.getenv("JSON_BIN_IO_KEY"),
        }

    @classmethod
    def format_request_body(cls, tasks) -> dict:
        return {"tasks": [task.model_dump() for task in tasks] if tasks else []}

    def send_request(self, method: StorageHttpMethods, body: dict = None) -> Response:
        if method == StorageHttpMethods.GET.value:
            response = requests.get(self.url, json=None, headers=self.headers)
        elif method == StorageHttpMethods.PUT.value:
            response = requests.put(self.url, json=body, headers=self.headers)
        else:
            raise NotImplementedError

        self.check_response_status(response.status_code)

        return response
