# Firmware – Audio Effects

This folder contains firmware for the Teensy-based audio processing system, which handles real-time audio effects for connected instruments (e.g., guitars or MIDI devices). The firmware is written in C++ using the Teensy Audio Library and interfaces via CAN bus for real-time control through the GUI.

## Features

- Real-time digital signal processing (DSP) for guitar and MIDI instruments.
- Configurable effects such as:
  - **Delay**
  - **Reverb**
  - **Chorus**
  - **Distortion**
  - **Bitcrusher**
- Input and output managed through the Teensy Audio Shield (I2S).
- MIDI handling via USBHost_t36 library for USB-connected keyboards.
- CAN bus communication using MCP2515 transceiver to receive effect settings from the Raspberry Pi GUI.

## Directory Structure

```
└── firmware/
    ├── audio_effects              
    ├── guitar        
    ├── midi
    ├── tests           
    └── README.md             # This file
```

## Dependencies

- [Teensy Audio Library](https://www.pjrc.com/teensy/td_libs_Audio.html)
- [MCP_CAN_lib](https://github.com/coryjfowler/MCP_CAN_lib) – for MCP2515 CAN transceiver
- `USBHost_t36` – for USB MIDI device support

## Hardware Requirements

- Teensy 4.1
- Teensy Audio Shield
- MCP2515 CAN transceiver
- External preamp (for guitar input)
- SD card (optional, for sample playback)

## Communication Protocol

- CAN ID range for audio settings:
  - `0x300–0x31F` for Guitar 1
  - `0x400–0x41F` for Guitar 2
- Each effect parameter is mapped to a unique CAN ID.
- GUI sends encoded values which are decoded by the Teensy to apply live changes.

## Setup

1. Install the required libraries via Arduino Library Manager or GitHub.
2. Connect Teensy with Audio Shield and MCP2515 per the provided schematic.
3. Compile and upload the firmware via Arduino IDE.
4. Launch the GUI on Raspberry Pi to control audio parameters.

## Future Improvements

- Dynamic sample loading
- Preset saving and recall
- Additional effect modules (e.g., flanger, compressor)
