# AudioLink

**A portable real-time multi-instrument digital audio processor for musicians**

---

## Overview
AudioLink is a real-time digital audio interface that accepts MIDI and analog guitar inputs, applies DSP effects, and outputs high-quality stereo audio. Designed for stage and studio use, it's built around the Raspberry Pi 5 and Teensy 4.1 microcontrollers.

---

## Team Members
- **Corey Hoang** – Project Lead, Embedded Systems Engineer, Firmware Architect, DSP & Audio Effect Chain Developer  
- **Jonathan Dittloff** – Embedded Systems Engineer, Electrical Engineering, PCB & Power Design & CAD Engineer  
- **Rolando Aguirre** – Embedded Systems Engineer, Raspberry Pi Middleware & UI Integrator & Developer  

---

## Repository Structure
```
AudioLink/
├── README.md            # This file
├── LICENSE
├── .gitignore
├── docs/                # Pitch deck, poster, and final report
│   ├── ECS_Expo_Poster.pdf
│   └── Project_Report.pdf
├── firmware/            # Teensy 4.1 code
│   ├── audio_effects/
│   ├── guitar/
│   ├── midi/
│   └── tests/
├── hardware/            # Schematics, PCB, and 3D models
│   ├── CAD_files/
│   ├── PCB_layouts/
│   ├── circuit_schematics/
│   └── tests/
├── middleware/          # Raspberry Pi middleware for UI and coordination
│   ├── can/
│   ├── config/
│   ├── tests/
│   ├── ui/
│   └── main.py/
├── team_notes/          # Individual logs or documentation
│   ├── corey_notes.md
│   ├── jonathan_notes.md
│   └── rolando_notes.md
└── tests/               # Audio, integration, and latency tests
    ├── test_logs/
    ├── test_plans.md
    └── performance_metrics.csv
```

---

## Key Features
- Dual analog guitar inputs with independent DSP chains
- Dual USB MIDI input support
- Real-time effects: EQ, delay, reverb, chorus, bitcrusher
- Touchscreen UI for effect and volume control
- CAN bus communication between Teensy and Raspberry Pi
- Analog stereo output for amp or PA system

---

## Getting Started
```bash
# Clone the repository
$ git clone https://github.com/<your_team>/AudioLink.git

# Navigate to Teensy firmware
$ cd AudioLink/firmware/main

# Open in Arduino IDE or PlatformIO
```

---

## License
This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

---

## Recognition
**Best Senior Project (Computer & Electrical Engineering)**  
CSUF ECS Expo 2025

