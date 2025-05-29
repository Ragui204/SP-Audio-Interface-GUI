import sys
import struct
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox, QLabel, QSlider, QFrame
)
from PyQt5.QtCore import Qt
import can

# CAN Setup
can_interface = 'can0'
bus = can.interface.Bus(channel=can_interface, bustype='socketcan')

TEENSY_CAN_ID = 0x300

# === Param IDs and Defaults ===
TOGGLE_EFFECTS = {
    "Delay": (32, False),
    "Reverb": (33, False),
    "Chorus": (34, False),
    "Distortion": (35, False)
}

SLIDER_PARAMS = {
    "Input Volume": (11, 1.0),
    "BPM": (12, 1.0),  # 100 = 100 BPM
    "Delay Division": (13, 0.2),
    "Reverb Time": (14, 1.0),
    "Reverb Gain": (15, 0.25),
    "Chorus Gain": (16, 0.25),
    "Chorus LFO Freq": (17, 0.5),
    "Chorus LFO Amp": (18, 1.0),
    "Distortion Gain": (19, 0.25),
    "Dry": (20, 0.4),
    "FX": (21, 0.6)
}

# === CAN Message Sender ===
def send_can_message(param_id, value):
    value_bytes = bytearray(struct.pack('f', value))
    data = bytearray([param_id]) + value_bytes
    msg = can.Message(arbitration_id=TEENSY_CAN_ID, data=data, is_extended_id=False)
    try:
        bus.send(msg)
        print(f"Sent param {param_id} -> {value}")
    except can.CanError as e:
        print(f"CAN send failed: {e}")

# === GUI Application ===
class GuitarEffectGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guitar Effect Control")
        self.setMinimumWidth(400)
        main_layout = QVBoxLayout()

        # --- Effect Toggles ---
        toggle_title = QLabel("Toggle Effects")
        toggle_title.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(toggle_title)

        for name, (param_id, default_state) in TOGGLE_EFFECTS.items():
            row = QHBoxLayout()
            label = QLabel(name)
            toggle = QCheckBox("Enable")
            toggle.setChecked(default_state)
            toggle.stateChanged.connect(lambda state, pid=param_id: send_can_message(pid, 1.0 if state == 2 else 0.0))
            row.addWidget(label)
            row.addWidget(toggle)
            main_layout.addLayout(row)

        # --- Divider Line ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        main_layout.addWidget(line)

        # --- Parameter Sliders ---
        param_title = QLabel("Adjust Parameters")
        param_title.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(param_title)

        for name, (param_id, default_val) in SLIDER_PARAMS.items():
            row = QVBoxLayout()
            label = QLabel(f"{name}: {default_val:.2f}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(int(default_val * 100))

            def make_handler(lbl, pid, effect_name):
                def handler(val):
                    float_val = val / 100.0
                    lbl.setText(f"{effect_name}: {float_val:.2f}")
                    send_can_message(pid, float_val)
                return handler

            slider.valueChanged.connect(make_handler(label, param_id, name))
            row.addWidget(label)
            row.addWidget(slider)
            main_layout.addLayout(row)

        self.setLayout(main_layout)

# === Main Entry Point ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuitarEffectGUI()
    gui.show()
    sys.exit(app.exec_())
    
