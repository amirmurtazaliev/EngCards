import asyncio

from dataclasses import dataclass
from typing import Any

from aiohttp import ClientResponseError, ClientSession, ClientTimeout

from app.core.config import settings
from app.core.exceptions import (
    NotificationServiceTimeoutError,
    NotificationServiceUnavailableError,
)

@dataclass
class HTTPResponse:
    status: int
    data: Any


class NotifyHTTPClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.notify_service_url
        self.timeout = ClientTimeout(total=5)

    async def send_post_request(self, endpoint_url: str, json: dict) -> HTTPResponse:
        try:
           async with ClientSession(base_url=self.base_url, timeout=self.timeout) as session:
                async with session.post(endpoint_url, json=json) as response:
                    response.raise_for_status()
                    return HTTPResponse(
                        status=response.status,
                        data=await response.json(),
                    )
            
        except asyncio.TimeoutError:
            raise NotificationServiceTimeoutError("Notification service timeout")
        except ClientResponseError as exc:
            raise NotificationServiceUnavailableError(
                f"Notification service returned {exc.status}"
            )
    async def close(self):
        return None