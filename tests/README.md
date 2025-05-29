# Tests – AudioLink

This directory contains standalone testing scripts used throughout development of the **AudioLink** system. These tests validate the performance and functionality of various modules, including hardware communication, audio signal routing, and UI behavior.

## Purpose

These test files helped us:

- Debug core features in isolation
- Validate proper integration across Teensy, Raspberry Pi, and CAN bus
- Quickly iterate during development cycles

## File Descriptions

- `DrumTest.py` – Manually triggers drum samples and confirms audio playback routing
- `GuitarTest.py` – Tests real-time input from guitar jack and validates signal through effect chain
- *(Add more descriptions as additional tests are created)*

## Usage

These tests are intended for local use during development. Run them from the root directory:

```bash
python3 tests/DrumTest.py

