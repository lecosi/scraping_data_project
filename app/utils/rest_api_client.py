
from typing import Dict, Any
from requests import get, post, Response


class RestAPIClient:

    @staticmethod
    def request_get(
        *,
        url: str,
        headers: Dict[str, Any]
    ) -> Response:
        response = get(
            url=url,
            headers=headers
        )
        return response

    @staticmethod
    def request_post(
        *,
        url: str,
        headers: Dict[str, Any],
        data: Dict[str, Any],
    ) -> Response:
        response = post(
            url=url,
            headers=headers,
            json=data
        )
        return response
