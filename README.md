# Bobil Van Heating Control Integration

A Home Assistant custom integration for controlling Bobil van heating systems through their web interface.

## Overview

This integration connects to your Bobil van heating system via its web interface, allowing you to monitor temperatures, water levels, and control heating functions directly from Home Assistant.

## Features

- **Real-time Monitoring**: Updates every 10 seconds
- **Resilient**: Preserves last known state when the heating system is temporarily unreachable
- **Comprehensive Entities**: Sensors, binary sensors, switches, and buttons for complete control

## Entities Created

### Sensors (6)
- **Air Temperature** - Current cabin air temperature
- **Air Temperature Target** - Target temperature setting
- **Water Tank Temperature** - Water tank temperature
- **Water Level** - Water tank level percentage
- **System Number** - Heating system identifier
- **Last Update** - Timestamp of last successful data fetch

### Binary Sensors (3)
- **Air Heating** - Air heating system status (ON/OFF)
- **Water Heating** - Water heating system status (ON/OFF)
- **Combined Heating** - Combined air and water heating status (ON/OFF)

### Switches (3)
- **Air Heating** - Control air heating system
- **Water Heating** - Control water heating system
- **Combined Heating** - Control combined heating mode

### Buttons (2)
- **Temperature Up** - Increase target temperature
- **Temperature Down** - Decrease target temperature

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/martynah/hacs-bobil`
6. Select category: "Integration"
7. Click "Add"
8. Find "Bobil Van Heating" in the integration list and install it
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/hacs_bobil` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Bobil Van Heating" or "HACS Bobil"
4. Enter the IP address or hostname of your van heating system
   - Example: `192.168.1.100` or `heating.local`
   - The integration assumes port 80 (standard HTTP)
5. Click **Submit**

The integration will validate the connection and create all entities automatically.

## Requirements

- Your van heating system must be accessible on your network
- The web interface must be reachable via HTTP (port 80)
- No authentication is required (assumes private network)

## How It Works

The integration scrapes the HTML web interface of your Bobil van heating system to extract:
- Temperature readings
- Water levels
- Heating system statuses

Control commands are sent via HTTP GET requests to the heating system's endpoints:
- `/f1on`, `/f1off` - Air heating
- `/f2on`, `/f2off` - Water heating
- `/f3on`, `/f3off` - Combined heating
- `/f4on` - Temperature up
- `/f5on` - Temperature down

## Troubleshooting

### Connection Issues
- Verify the IP address or hostname is correct
- Ensure the heating system's web interface is accessible from your Home Assistant instance
- Check that the heating system is powered on and connected to your network

### Data Not Updating
- The integration polls every 10 seconds
- If the heating system is unreachable, the integration will preserve the last known state
- Check the Home Assistant logs for error messages

## Development

This integration is developed using the Home Assistant custom component development template with:
- Full type hints
- Ruff linting
- DevContainer support
- Python 3.13 compatibility

### Running Locally

```bash
# Clone the repository
git clone https://github.com/martynah/hacs-bobil
cd hacs-bobil

# Open in VS Code with DevContainers
code .

# Start Home Assistant
scripts/develop
```

## Support

For issues, feature requests, or contributions, please visit:
- **Issues**: https://github.com/martynah/hacs-bobil/issues
- **Documentation**: https://github.com/martynah/hacs-bobil

## License

See the [LICENSE](LICENSE) file for details.
