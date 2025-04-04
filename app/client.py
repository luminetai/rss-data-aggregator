import aiohttp
import backoff

class ClientError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class Client:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = aiohttp.ClientSession()
        return cls._instance

    @backoff.on_exception(backoff.expo, [aiohttp.ClientError, aiohttp.ClientConnectorError], max_tries=3)
    async def request(self, method: str, url: str, headers: dict = None, data: dict = None):
        try:
            async with self.session.request(method, url, headers=headers, data=data) as response:
                if response.status != 200:
                    raise ClientError(f"Request to {url} failed with status {response.status}")
                return await response.text()
        except aiohttp.ClientError as e:
            raise ClientError(f"Client error occurred while requesting {url}: {e}")
        except Exception as e:
            raise ClientError(f"Unexpected error during request to {url}: {e}")

    async def close(self):
        if self.session is not None and not self.session.closed:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()