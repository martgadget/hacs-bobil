"""DataUpdateCoordinator for hacs_bobil."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    HacsBobilApiClientCommunicationError,
    HacsBobilApiClientError,
)
from .const import LOGGER

if TYPE_CHECKING:
    from .data import HacsBobilConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class BlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: HacsBobilConfigEntry
    _last_successful_data: dict[str, Any] | None = None

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            data = await self.config_entry.runtime_data.client.async_get_data()
            # Store successful data for fallback
            self._last_successful_data = data
            return data
        except HacsBobilApiClientCommunicationError as exception:
            # Communication error - preserve last good data if available
            LOGGER.warning(
                "Communication error with heating system: %s. Using cached data.",
                exception,
            )
            if self._last_successful_data is not None:
                return self._last_successful_data
            raise UpdateFailed(exception) from exception
        except HacsBobilApiClientError as exception:
            # Other errors should still fail
            raise UpdateFailed(exception) from exception
