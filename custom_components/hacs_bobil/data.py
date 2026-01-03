"""Custom types for hacs_bobil."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import HacsBobilApiClient
    from .coordinator import BlueprintDataUpdateCoordinator


type HacsBobilConfigEntry = ConfigEntry[HacsBobilData]


@dataclass
class HacsBobilData:
    """Data for the Blueprint integration."""

    client: HacsBobilApiClient
    coordinator: BlueprintDataUpdateCoordinator
    integration: Integration
