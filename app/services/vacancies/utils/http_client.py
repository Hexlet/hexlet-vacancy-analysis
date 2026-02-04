import asyncio
from abc import ABC, abstractmethod

import aiohttp


class HTTPClientInterface(ABC):
    @abstractmethod
    async def get(self, url: str, params: dict[str, any] = None) -> any:
        pass


class HTTPClient(HTTPClientInterface):
    CONCURRENT_LIMIT = 10

    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        timeout: int = 10,
    ):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    async def fetch(self, session, url, semaphore, params):
        async with semaphore:
            async with session.get(url, params=params, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()

    async def get(
        self,
        urls: list[str],
        params: dict[str, any] = None,
    ) -> any:
        semaphore = asyncio.Semaphore(self.CONCURRENT_LIMIT)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(
            timeout=timeout, raise_for_status=True
        ) as session:
            tasks = [self.fetch(session, url, semaphore, params) for url in urls]
            return await asyncio.gather(*tasks, return_exceptions=True)
