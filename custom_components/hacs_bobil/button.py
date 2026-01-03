"""Button platform for hacs_bobil."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from .entity import HacsBobilEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import HacsBobilConfigEntry

ENTITY_DESCRIPTIONS = (
    ButtonEntityDescription(
        key="temp_up",
        name="Temperature Up",
        icon="mdi:thermometer-chevron-up",
    ),
    ButtonEntityDescription(
        key="temp_down",
        name="Temperature Down",
        icon="mdi:thermometer-chevron-down",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HacsBobilConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    async_add_entities(
        HacsBobilButton(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HacsBobilButton(HacsBobilEntity, ButtonEntity):
    """hacs_bobil button class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"

    async def async_press(self, **_: Any) -> None:
        """Handle the button press."""
        client = self.coordinator.config_entry.runtime_data.client
        if self.entity_description.key == "temp_up":
            await client.async_temp_up()
        elif self.entity_description.key == "temp_down":
            await client.async_temp_down()
        await self.coordinator.async_request_refresh()
