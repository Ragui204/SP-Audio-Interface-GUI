# AudioLink

## 🎧 Overview
AudioLink is a real-time multi-input audio interface for musicians, built for low-latency performance. It supports two MIDI inputs, two guitar jacks, and outputs processed audio through a stereo system. The device includes EQ, reverb, delay, and modulation effects with touch UI control.

Built on: **Teensy 4.1 + Raspberry Pi 5 + SGTL5000 Audio Shield + MCP2515 CAN bus**

---

## 🗂 Repository Structure

```
AudioLink/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── block_diagram.png
│   ├── system_overview.md
│   └── pitch_deck.pdf
├── firmware/
│   ├── teensy/
│   │   └── main_teensy_audio.ino
│   ├── rpi/
│   │   └── can_controller.py
│   └── shared/
│       └── audio_samples/
│           ├── piano_c4.wav
│           └── kick.wav
├── hardware/
│   ├── schematics/
│   │   └── teensy_clone_custom.sch
│   ├── pcb_layout/
│   │   └── board.kicad_pcb
│   └── bom.csv
├── team_notes/
│   ├── project_lead/
│   │   └── timeline.md
│   ├── electrical/
│   │   └── codec_routing_notes.md
│   ├── software/
│   │   └── canbus_parser_devlog.md
│   └── audio_design/
│       └── reverb_delay_mixer_tests.md
└── tests/
    └── audio_latency_test.md
```

---

## 👥 Team Members & Roles
- **[Your Name]** – Project Lead, Firmware Architect
- **[Member 2]** – Electrical Engineering, PCB & Power Design
- **[Member 3]** – DSP & Audio Effect Chain Developer
- **[Member 4]** – Raspberry Pi Middleware & UI Integrator

---

## 🚀 Getting Started
### Prerequisites
- Teensyduino 1.59+
- Arduino IDE or PlatformIO
- Python 3.x (for RPi CAN)
- KiCad (for PCB design)

### To Build Firmware:
```bash
cd firmware/teensy
# Open in Arduino IDE or compile with Teensy CLI
```

### To Run CAN Controller:
```bash
cd firmware/rpi
python3 can_controller.py
```

---

## 🧠 Features
- Polyphonic MIDI synth engine (16 voices)
- Real-time guitar FX chain with EQ/Delay/Reverb/Bitcrusher
- CAN-based low-latency communication between Pi and Teensy
- OLED/Touchscreen control interface

---

## 🏆 Awards
**Best Senior Project 2025 - Computer & Electrical Engineering - CSUF ECS Expo**

---

## 📜 License
MIT License (see LICENSE file for details)

---

## ✨ Special Thanks
Thanks to mentors, faculty, and contributors who helped us bring AudioLink to life!
