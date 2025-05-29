# UI Module – AudioLink

This directory contains Python modules that define the graphical and hardware user interface for **AudioLink**, including interactive controls, visual feedback, and user-driven parameter adjustments.

## Purpose

The UI module provides real-time control over audio effects and input channels. It runs on the Raspberry Pi touchscreen display and connects via middleware to the DSP engines on Teensy microcontrollers.

## File Overview

- `DelayReverb.py` – Reverb and delay effect UI handlers
- `GuitarControls.py` – Effect toggles and sliders for guitar input channel(s)
- `NavigationBar.py` – Top bar navigation UI component
- `Pads.py` – Drum pad interface to trigger one-shot samples
- `Volume.py` – Mixer level controls for each instrument or effect chain
- `ui_setup.py` – Initializes GUI window and routes pages/layouts
- `waveform.py` – Visualizes waveform or meter display (if applicable)

## Dependencies

- `tkinter` (or appropriate GUI library you are using)
- Python 3.7+
- Raspberry Pi OS or compatible Linux environment

## Notes

This UI is designed to be lightweight, intuitive, and touch-optimized. All modules in this directory can be modified or extended to support additional views, controls, or hardware devices.

> Developed with modularity in mind — each file can operate independently or be imported into the `ui_setup.py` main screen system.
