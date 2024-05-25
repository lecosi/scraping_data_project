
from typing import Dict, Any
import httpx


class RestAPIClient:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def request_get(
        self,
        *,
        url: str,
        headers: Dict[str, Any]
    ) -> httpx.Response:
        return await self.client.get(
            url=url,
            headers=headers
        )

    async def request_post(
        self,
        *,
        url: str,
        headers: Dict[str, Any],
        data: Dict[str, Any],
    ) -> httpx.Response:
        return await self.client.post(
            url=url,
            headers=headers,
            json=data
        )
