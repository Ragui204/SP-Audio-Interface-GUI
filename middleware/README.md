# Middleware

This folder contains the core modules and runtime logic that drive the AudioLink device. Middleware bridges communication between the user interface (UI), hardware peripherals (CAN bus, audio), and audio DSP pipeline.

## Folder Structure

- `can/` – Handles CAN bus message parsing and transmission
- `config/` – Contains audio mapping configuration files (e.g., pad mappings)
- `dsp/` – Custom DSP effect handlers and audio processing components
- `tests/` – Unit and integration tests for middleware functionality
- `ui/` – UI event routing and navigation logic for touchscreen control
- `main.py` – The root execution script for launching all system modules

## Development Notes

- This structure supports modularity and easier debugging when expanding AudioLink functionality.
- If cloning or contributing, start at `main.py` for the runtime entry point.
- External dependencies should be handled through virtual environment management (e.g., `venv/` not included in repo).

> **Note:** This is an active development repository for a prototype audio hardware system. Namespaces, paths, and APIs are subject to change as we prepare for formal patent review and optimization.

