"""Constants for hacs_bobil."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "hacs_bobil"
ATTRIBUTION = "Data provided by Bobil Van Heating System"

# Configuration
CONF_HOST = "host"

# API Endpoints
ENDPOINT_AIR_ON = "/f1on"
ENDPOINT_AIR_OFF = "/f1off"
ENDPOINT_WATER_ON = "/f2on"
ENDPOINT_WATER_OFF = "/f2off"
ENDPOINT_COMBINED_ON = "/f3on"
ENDPOINT_COMBINED_OFF = "/f3off"
ENDPOINT_TEMP_UP = "/f4on"
ENDPOINT_TEMP_DOWN = "/f5on"
