# System Service

This directory contains the `.service` file used to configure AudioLink as a systemd-managed auto-start service on Linux-based systems (e.g., Raspberry Pi OS).

## `.service`

The `.service` file defines how and when the AudioLink application should be launched on boot. It ensures the system starts the software stack automatically without requiring manual user input.

### Key Features:
- Auto-launches `main.py` after boot
- Runs in the background
- Can be enabled or disabled via `systemctl`

## Installation Instructions

1. Copy the file to the systemd directory:
   ```bash
   sudo cp .service /etc/systemd/system/audiolink.service
