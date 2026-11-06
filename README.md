# Shalya

**A modular, multi-input control system for a toy drone using an ESP32 and an external DAC.**

Shalya is an experimental drone-control project that connects software-based input systems to the physical controls of a toy drone.

The system uses a Python backend to process control inputs and an ESP32-based client to translate control commands into analog voltage signals through a four-channel DAC. These signals interface with the joystick potentiometer inputs of the drone's original remote controller.

The initial implementation focuses on keyboard-based control. The long-term objective is to support multiple input methods through a common control architecture.

> **Project status:** Early prototype. Keyboard-based control, WebSocket communication and DAC output have been implemented. Reliable flight, calibration and safety mechanisms remain under development.

## Architecture

Shalya currently follows a client-server architecture.

```text
             KEYBOARD INPUT
                   |
                   v
           Python Backend
                   |
             Control Loop
                   |
                   v
          WebSocket Server
                   |
             JSON Messages
                   |
                   v
               ESP32
                   |
              I2C Bus
                   |
                   v
             MCP4728 DAC
                   |
                   v
        Drone Remote Joystick Inputs
```

### Python Backend

The backend is responsible for:

- Receiving keyboard input.
- Processing and updating control-axis values.
- Maintaining the current control state.
- Transmitting control data to the ESP32 over WebSockets.

### ESP32 Client

The ESP32 receives control messages from the backend, parses the JSON data and updates the DAC outputs accordingly.

### Analog Output

An Adafruit MCP4728 four-channel, 12-bit DAC generates analog voltage signals corresponding to the four control axes.

The DAC outputs interface with the joystick potentiometer inputs of the drone's original remote controller.

## Control Axes

Shalya currently supports four control axes:

| Axis | Description |
|---|---|
| Roll | Left/right movement |
| Pitch | Forward/backward movement |
| Throttle | Up/down movement |
| Yaw | Rotational movement |

The backend represents each axis using a normalized value between `-1.0` and `+1.0`, with `0.0` representing the neutral position.

The ESP32 maps these normalized values to DAC output values.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python |
| Communication | WebSockets |
| Message format | JSON |
| Microcontroller | ESP32 |
| Firmware framework | Arduino |
| Firmware build system | PlatformIO |
| DAC | Adafruit MCP4728 |
| DAC communication | I2C |

## Hardware

The current prototype uses:

- ESP32 development board
- Adafruit MCP4728 four-channel, 12-bit DAC
- Toy drone and original remote controller
- Connecting wires and appropriate power connections

The ESP32 communicates with the MCP4728 over I2C.

| Signal | ESP32 GPIO |
|---|---|
| SDA | GPIO 21 |
| SCL | GPIO 22 |

The DAC channel assignments are:

| DAC channel | Control axis |
|---|---|
| A | Roll |
| B | Pitch |
| C | Throttle |
| D | Yaw |

Refer to the hardware wiring documentation before connecting the components.

## Getting Started

See the [Setup Guide](docs/setup.md) for installation, configuration and execution instructions.

**Repository:** [github.com/thetubelight/shalya](https://github.com/thetubelight/shalya)

Clone the project:

```bash
git clone https://github.com/thetubelight/shalya.git
cd shalya
```

## Current Implementation Status

| Feature | Status |
|---|---|
| Keyboard input | Implemented |
| Four-axis control state | Implemented |
| Backend control processing | Implemented |
| WebSocket communication | Implemented |
| ESP32 JSON message handling | Implemented |
| MCP4728 DAC output | Implemented |
| Reliable and repeatable flight | Not yet established |
| Emergency stop / failsafe | Not yet implemented |
| Gamepad input | Planned |
| Hand gesture input | Planned |
| Telemetry and visual feedback | Planned |

Implementation status refers to the current code. It does not imply that every feature has been validated under real flight conditions.

## Future Development

The planned development direction includes:

- Improve control responsiveness and consistency.
- Calibrate DAC output ranges against the physical remote controller.
- Implement emergency-stop and communication-loss handling.
- Introduce a common input-controller interface.
- Add gamepad-based control.
- Integrate computer vision and hand gesture recognition.
- Add telemetry and visual feedback.

## Safety and Limitations

Shalya is an experimental hardware-control prototype.

The current implementation does not yet provide a complete emergency-stop or failsafe mechanism. Network interruptions, unexpected input values, incorrect calibration or firmware errors may result in unintended control signals.

Do not attempt flight until output limits, calibration, emergency-stop behaviour and communication-loss handling have been implemented and tested under controlled conditions.

Always account for the electrical characteristics of the original remote controller when connecting external circuitry.

## Project Goals

The long-term goal is to develop a modular control system in which different input methods can operate the same underlying drone-control pipeline.

Input acquisition, control processing, communication and hardware interfacing are intended to remain separate components, allowing individual parts of the system to be developed and tested independently.