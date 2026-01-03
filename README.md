# Bobil Van Heating Control Integration

A Home Assistant custom integration for controlling Bobil Vans Smart Heating Controller through its WIFI web interface.

## Overview

This integration connects to your <a href='https://www.bobilvans.co.uk/product-page/bobil-smart-pro-controller'>Bobil Vans Smart Heating Controller</a> via its web interface, allowing you to monitor temperatures, water levels, and control heating functions directly from Home Assistant.

<img width="480" height="330" alt="image" src="https://github.com/user-attachments/assets/043bc02a-d997-44bd-a265-fdc93434036d" />

To use this integration, you'll need to:

- Get a USB WIFI Adapter to add to your home assistant hardware, or have a spare WIFI interface on the device (e.g Raspberry Pi's with WIFI interfaces as well as wired ones)
- Ensure that your Home Assistant installation main network is NOT using 192.168.4.0/24 as its network. If your camper wifi network uses this range, change it to 192.168.3.0/24 or something else (Bobil's smart controller is hard-wired to use 192.168.4.0 as its network, which cant be changed)

## Features

- Full control of all Bobil Functions, Air, Combined, Hot Water modes
- Control of Target Temperature
- Syncs to the Web Interface of the Bobil Controller, Updates every 10 seconds
- Preserves last known state when the heating system is temporarily unreachable
- Shows all data which is available on the Controller Web Page at http://192.168.4.1

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

### Add the Bobil WIFI Network

1. Press 'Menu' on the Bobil controller until it shows you its WIFI SSID and Password
2. Connect your compatible USB Wifi interface to the hardware running Home Assistant.
3. Navigate to Settings/System/Network in Home Assistant
4. Locate the WIFI network adapter (usually wlan0)
5. Browse for the Bobil Network
6. Enter the password
7. Accept the default settings *dont set a default gateway*

If you have 'Terminal' installed in HA, you can go there now, and check you can ping 192.168.4.1 to see if the Bobil Controller has connected.
The controller itself will also show 'WIFI' on its home screen. The above address should 'ping'.

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
4. Enter 192.168.4.1 as the IP address of the Controller.
5. Click **Submit**

The integration will validate the connection and create all entities automatically.

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

## Support

For issues, feature requests, or contributions, please visit:
- **Issues**: https://github.com/martynah/hacs-bobil/issues
- **Documentation**: https://github.com/martynah/hacs-bobil

## License

See the [LICENSE](LICENSE) file for details.

