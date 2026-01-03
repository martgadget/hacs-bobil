"""API Client for Van Heating System."""

from __future__ import annotations

import re
import socket
from datetime import UTC, datetime
from typing import Any

import aiohttp
import async_timeout

from .const import (
    ENDPOINT_AIR_OFF,
    ENDPOINT_AIR_ON,
    ENDPOINT_COMBINED_OFF,
    ENDPOINT_COMBINED_ON,
    ENDPOINT_TEMP_DOWN,
    ENDPOINT_TEMP_UP,
    ENDPOINT_WATER_OFF,
    ENDPOINT_WATER_ON,
)


class HacsBobilApiClientError(Exception):
    """Exception to indicate a general API error."""


class HacsBobilApiClientCommunicationError(
    HacsBobilApiClientError,
):
    """Exception to indicate a communication error."""


class HacsBobilApiClient:
    """API Client for Van Heating System."""

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._host = host
        self._session = session
        self._base_url = f"http://{host}"

    async def async_get_data(self) -> dict[str, Any]:
        """Get data from the heating system by parsing HTML."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(self._base_url)
                response.raise_for_status()
                html = await response.text()

                return self._parse_html(html)

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise HacsBobilApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise HacsBobilApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:
            msg = f"Error parsing data - {exception}"
            raise HacsBobilApiClientError(
                msg,
            ) from exception

    def _parse_html(self, html: str) -> dict[str, Any]:
        """Parse HTML to extract sensor values and statuses."""
        data: dict[str, Any] = {}

        # Extract air temperature
        match = re.search(r"AIR TEMP:\s*([-\d.]+)&deg;C", html)
        if match:
            data["air_temperature"] = float(match.group(1))

        # Extract air temperature target
        match = re.search(r"AIR TEMP TARGET:\s*([-\d.]+)&deg;C", html)
        if match:
            data["air_temperature_target"] = float(match.group(1))

        # Extract water tank temperature
        match = re.search(r"WATER TANK TEMP:\s*([-\d.]+)&deg;C", html)
        if match:
            data["water_tank_temperature"] = float(match.group(1))

        # Extract water level
        match = re.search(r"WATER LEVEL:\s*([-\d.]+)%", html)
        if match:
            data["water_level"] = float(match.group(1))

        # Extract system number
        match = re.search(r"SYSTEM NO:\s*(\d+)", html)
        if match:
            data["system_number"] = match.group(1)

        # Extract air heating status
        match = re.search(r"AIR HEATING STATUS:\s*(ON|OFF)", html)
        if match:
            data["air_heating_status"] = match.group(1) == "ON"

        # Extract water heating status
        match = re.search(r"WATER HEATING STATUS:\s*(ON|OFF)", html)
        if match:
            data["water_heating_status"] = match.group(1) == "ON"

        # Extract combined heating status
        match = re.search(r"AIR AND WATER HEATING STATUS:\s*(ON|OFF)", html)
        if match:
            data["combined_heating_status"] = match.group(1) == "ON"

        # Add timestamp of successful fetch
        data["last_update"] = datetime.now(UTC)

        return data

    async def _send_command(self, endpoint: str) -> None:
        """Send a command to the heating system."""
        try:
            async with async_timeout.timeout(10):
                url = f"{self._base_url}{endpoint}"
                response = await self._session.get(url)
                response.raise_for_status()

        except TimeoutError as exception:
            msg = f"Timeout error sending command - {exception}"
            raise HacsBobilApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error sending command - {exception}"
            raise HacsBobilApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:
            msg = f"Unexpected error sending command - {exception}"
            raise HacsBobilApiClientError(
                msg,
            ) from exception

    async def async_turn_on_air_heating(self) -> None:
        """Turn on air heating."""
        await self._send_command(ENDPOINT_AIR_ON)

    async def async_turn_off_air_heating(self) -> None:
        """Turn off air heating."""
        await self._send_command(ENDPOINT_AIR_OFF)

    async def async_turn_on_water_heating(self) -> None:
        """Turn on water heating."""
        await self._send_command(ENDPOINT_WATER_ON)

    async def async_turn_off_water_heating(self) -> None:
        """Turn off water heating."""
        await self._send_command(ENDPOINT_WATER_OFF)

    async def async_turn_on_combined_heating(self) -> None:
        """Turn on combined heating."""
        await self._send_command(ENDPOINT_COMBINED_ON)

    async def async_turn_off_combined_heating(self) -> None:
        """Turn off combined heating."""
        await self._send_command(ENDPOINT_COMBINED_OFF)

    async def async_temp_up(self) -> None:
        """Increase temperature target."""
        await self._send_command(ENDPOINT_TEMP_UP)

    async def async_temp_down(self) -> None:
        """Decrease temperature target."""
        await self._send_command(ENDPOINT_TEMP_DOWN)
