import os
from enum import Enum
import requests
from requests import Response

from gateways.BaseHttpClient import BaseHttpClient

class CloudFlareMethods(Enum):
    POST = "POST"

class CloudFlareHttpClient(BaseHttpClient):
    @property
    def url(self) -> str:
        return f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUD_FLARE_ACCOUNT_ID')}/ai/run/@cf/meta/llama-3-8b-instruct"

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('CLOUD_FLARE_KEY')}",
        }

    @classmethod
    def format_request_body(cls, prompt: str) -> dict:
        return {"prompt": prompt}

    def send_request(self, method: str = CloudFlareMethods.POST, body: dict = None) -> Response:
        if method == CloudFlareMethods.POST.value:
            response = requests.post(self.url, json=body, headers=self.headers)
        else:
            raise NotImplementedError

        return response
