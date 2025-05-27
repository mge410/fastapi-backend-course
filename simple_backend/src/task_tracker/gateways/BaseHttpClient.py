from abc import ABC, abstractmethod

from requests import Response

from exceptions.gateway_response_exception import GatewayResponseException


class BaseHttpClient(ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @property
    @abstractmethod
    def headers(self) -> dict:
        pass

    @classmethod
    def check_response_status(cls, status: int):
        if status != 200:
            raise GatewayResponseException

    @abstractmethod
    def send_request(self, method: str, body) -> Response:
        pass
