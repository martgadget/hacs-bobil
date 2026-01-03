"""Binary sensor platform for hacs_bobil."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import HacsBobilEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import HacsBobilConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="air_heating_status",
        name="Air Heating",
        device_class=BinarySensorDeviceClass.HEAT,
        icon="mdi:radiator",
        entity_registry_enabled_default=False,
    ),
    BinarySensorEntityDescription(
        key="water_heating_status",
        name="Water Heating",
        device_class=BinarySensorDeviceClass.HEAT,
        icon="mdi:water-boiler",
        entity_registry_enabled_default=False,
    ),
    BinarySensorEntityDescription(
        key="combined_heating_status",
        name="Combined Heating",
        device_class=BinarySensorDeviceClass.HEAT,
        icon="mdi:fire",
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HacsBobilConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        HacsBobilBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HacsBobilBinarySensor(HacsBobilEntity, BinarySensorEntity):
    """hacs_bobil binary_sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get(self.entity_description.key, False)
