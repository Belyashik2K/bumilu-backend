from collections.abc import Sequence
from typing import (
    Any,
)

import httpx

from app.core.exceptions import BaseInfrastructureException


class ValhallaError(BaseInfrastructureException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ValhallaClient:
    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 5.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def route(
        self,
        *,
        locations: Sequence[dict[str, float | str]],
        costing: str,
        language: str = "ru-RU",
        units: str = "kilometers",
    ) -> dict[str, Any]:
        payload = {
            "locations": locations,
            "costing": costing,
            "directions_options": {
                "language": language,
            },
            "units": units,
        }

        try:
            response = await self._client.post(
                "/route",
                json=payload,
            )
        except httpx.HTTPError as e:
            raise ValhallaError(f"Valhalla is unreachable: {e}") from e

        if response.status_code != 200:
            raise ValhallaError(
                f"Valhalla HTTP error: {response.status_code} {response.text}"
            )

        data = response.json()

        if data.get("trip", {}).get("status") != 0:
            raise ValhallaError(
                f"Valhalla error: {data.get('trip', {}).get('status_message')}"
            )

        return data
