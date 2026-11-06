# Setup Guide

This guide explains how to set up Shalya on a Windows development machine.

## Prerequisites

### Software

- Python 3.10 or later
- Git
- Visual Studio Code
- PlatformIO IDE extension for VS Code
- USB drivers for your ESP32 board, if required

### Hardware

- ESP32 development board
- Adafruit MCP4728 four-channel DAC
- Toy drone and its original remote controller
- Connecting wires and appropriate power connections

## 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/thetubelight/shalya.git
cd shalya
```

## 2. Set Up the Python Backend

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If you are using Command Prompt instead of PowerShell:

```cmd
.venv\Scripts\activate.bat
```

Upgrade pip and install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure the ESP32

The ESP32 firmware requires Wi-Fi credentials and the IP address of the machine running the Python backend.

Navigate to:

```text
esp32-drone/include/
```

Create a local configuration file by copying the sample:

```powershell
Copy-Item config.example.hpp config.hpp
```

Open `config.hpp` and update the values:

```cpp
#pragma once

#include <cstdint>

constexpr char WIFI_SSID[] = "YOUR_WIFI_NAME";
constexpr char WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";

constexpr char WS_HOST[] = "YOUR_IP";

constexpr uint16_t WS_PORT = 8765;
```

Replace the placeholders:

| Variable | Description |
|---|---|
| `WIFI_SSID` | Name of your Wi-Fi network |
| `WIFI_PASSWORD` | Password of your Wi-Fi network |
| `WS_HOST` | Local IPv4 address of the computer running the Python backend |
| `WS_PORT` | WebSocket server port; must match the backend configuration |

**Important:** The ESP32 and the computer running the backend must be connected to the same network.

### Finding your computer's IP address

On Windows, open Command Prompt and run:

```cmd
ipconfig
```

Find the IPv4 address under the network adapter currently connected to your Wi-Fi network.

Use that address for `WS_HOST`.

Do not use `127.0.0.1` or `localhost`, as these refer to the device itself rather than your computer from the ESP32's perspective.

If Windows Firewall blocks the connection, allow the backend application or its listening port through the firewall.

> **Security:** Never commit your actual `config.hpp` file. It contains Wi-Fi credentials and local network configuration. Only `config.sample.hpp` should be tracked by Git.

## 4. Build and Upload the ESP32 Firmware

Open the `esp32-drone` directory in VS Code.

Make sure the PlatformIO extension is installed and has finished initializing.

Using the PlatformIO toolbar, or the PlatformIO sidebar:

1. Build the firmware.
2. Connect the ESP32 through USB.
3. Select the appropriate serial port if required.
4. Upload the firmware.
5. Open the Serial Monitor to inspect startup messages.

PlatformIO automatically downloads the dependencies specified in `platformio.ini` during the build process.

## 5. Run Shalya

Start the Python backend from the repository root:

```bash
python -m backend.main
```

After starting the backend:

1. Power on the ESP32.
2. Check the ESP32 Serial Monitor for Wi-Fi and WebSocket connection messages.
3. Verify that the backend is receiving or transmitting control data as expected.
4. Test the control inputs under controlled conditions.

The backend must be running before the ESP32 attempts to establish its WebSocket connection, unless the firmware implements automatic reconnection.

## 6. Troubleshooting

| Problem | Things to check |
|---|---|
| Python module not found | Confirm that the virtual environment is activated and dependencies are installed. |
| ESP32 cannot connect to Wi-Fi | Verify the SSID and password in `config.hpp`. |
| WebSocket connection fails | Check `WS_HOST`, `WS_PORT`, backend status and firewall settings. |
| PlatformIO build fails | Check the installed PlatformIO extension and dependency configuration. |
| DAC output is incorrect | Verify I2C wiring, DAC connections, channel assignments and output calibration. |

## 7. Local Files and Git

The following files and directories are local development files and should not be committed:

- `.venv/` — Python virtual environment
- `esp32-drone/.pio/` — PlatformIO build files
- `esp32-drone/include/config.hpp` — Local configuration containing Wi-Fi credentials

The sample configuration file, `esp32-drone/include/config.sample.hpp`, should be committed so that other developers can create their own local configuration.

---

**Note:** Shalya is an experimental hardware-control prototype. Its emergency-stop and communication-loss safety mechanisms are not yet complete. Do not attempt flight until these mechanisms, output limits and calibration have been implemented and tested.