# Bobil Van Heating Control Integration

A Home Assistant custom integration for controlling Bobil Vans Smart Heating Controller through its WIFI web interface.<p>
<b>This is not an official Bobil solution, its provided 'as is' for the hobbyist and home assistant user. If you have issues, please post an issue in 'Issues'.</b>

## Overview

This integration connects to your <a href='https://www.bobilvans.co.uk/product-page/bobil-smart-pro-controller'>Bobil Vans Smart Heating Controller</a> via its web interface, allowing you to monitor temperatures, water levels, and control heating functions directly from Home Assistant.

<img width="1396" height="990" alt="image" src="https://github.com/user-attachments/assets/a492677c-3992-4b28-bbb6-60423b607a79" />
(cards expanded to full width in screenshot)
<p></p>
The integration has been tested with the Bobil Smart Controller for their combined air and water heating unit. There is a new controller version for their hydronic heating solution, which I have not tested (if the web interface is the same, it should also work). 
<p></p>
<img width="480" height="330" alt="image" src="https://github.com/user-attachments/assets/043bc02a-d997-44bd-a265-fdc93434036d" />

To use this integration, you'll need to:

- Get a USB WIFI Adapter to add to your home assistant hardware, or have a spare WIFI interface on the device (e.g Raspberry Pi's with WIFI interfaces as well as wired ones)
- Ensure that your Home Assistant installation main network is NOT using 192.168.4.0/24 as its network. If your camper wifi network uses this range, change it to 192.168.3.0/24 or something else (Bobil's smart controller is hard-wired to use 192.168.4.0 as its network, which cant be changed)

- If you want to control your system remotely, while outside the Van for example, then you'll need:
    - A cellular or wifi device with the HomeAssistant app, or a browser installed 
    - An internet connection that is active in your Van, either 3G/4G cellular, or Starlink for example
    - A Home Assistant <a href='https://www.nabucasa.com/'>Nabu Casa</a> account and subscription (or other remote access solution) 

## SAFETY WARNING
<b>Combined with the above remote access facility, this plug-in will give you remote control of your heating and hot water system. You must be certain that your system is installed safely, and securely within the vehicle, as it will be able to operate unattended, when you could in theory be a very long way from your vehicle, and unaware of any faults that may develop with it. Be aware of serious hazards such are fire, or toxic exhaust fumes. The author is not responsbile for any damage that may occur. </b>

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

## FAQ

- <b>Its really slow, why?</b>
  This is because the web interface only updates every 10 seconds, you could change this in the code if you wanted to, but polling the controller too often my cause it to hang
- <b>Why cant you enter a temperature or use one of the nice HA dials?</b>
  The Bobil controller only exposes an 'up' and 'down' button for temperature, its not possible to enter a temperature in the supplied UI, so the add-on cant provide that
- <b>It hangs/errors when the heater is cooling</b>
  The controller locks out its web interface when the 5 minute heater cooling cycle has started. This causes the web-ui to reject imput
- <b>The Home Assistant UI is out of sync with the controller</b>
  Unfortunatley (see <a href='https://www.bobilvans.co.uk/_files/ugd/67186c_97aa2a0390314611bbb46604494b5f5b.pdf'>Bobil documentation</a>), the controller UI and its web-ui dont always
  know what the last action was. If you make a change on the controller locally in the vehicle, the    web UI doesnt 'know', hence may reflect the wrong status.
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


