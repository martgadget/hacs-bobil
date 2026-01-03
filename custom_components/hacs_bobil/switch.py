"""Switch platform for hacs_bobil."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .entity import HacsBobilEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import HacsBobilConfigEntry

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="air_heating",
        name="Air Heating",
        icon="mdi:radiator",
    ),
    SwitchEntityDescription(
        key="water_heating",
        name="Water Heating",
        icon="mdi:water-boiler",
    ),
    SwitchEntityDescription(
        key="combined_heating",
        name="Combined Heating",
        icon="mdi:fire",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HacsBobilConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        HacsBobilSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HacsBobilSwitch(HacsBobilEntity, SwitchEntity):
    """hacs_bobil switch class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        status_key = f"{self.entity_description.key}_status"
        return self.coordinator.data.get(status_key, False)

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        client = self.coordinator.config_entry.runtime_data.client
        if self.entity_description.key == "air_heating":
            await client.async_turn_on_air_heating()
        elif self.entity_description.key == "water_heating":
            await client.async_turn_on_water_heating()
        elif self.entity_description.key == "combined_heating":
            await client.async_turn_on_combined_heating()
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        client = self.coordinator.config_entry.runtime_data.client
        if self.entity_description.key == "air_heating":
            await client.async_turn_off_air_heating()
        elif self.entity_description.key == "water_heating":
            await client.async_turn_off_water_heating()
        elif self.entity_description.key == "combined_heating":
            await client.async_turn_off_combined_heating()
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()
