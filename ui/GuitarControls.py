from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDial, QCheckBox,
    QGroupBox, QPushButton, QSizePolicy, QFrame, QGridLayout, QSpacerItem,
    QDialog, QSpinBox
)
from PyQt5.QtCore import Qt
from can_handler import send_can_message
import time

last_send_times = {}

DEFAULT_VALUES = {
    "Input Volume": 1.0,
    "BPM": 120,
    "NUMBER_OF_DELAYS": 3,
    "DELAY_GAIN": 0.25,
    "REVERB_TIME": 4.0,
    "REVERB_GAIN": 0.25,
    "CHORUS_GAIN": 0.25,
    "BASE_DELAY_MS": 10.0,
    "MOD_DEPTH_MS": 3.0,
    "MOD_RATE_HZ": 0.5,
    "NUMBER_OF_VOICES": 4,
    "BITCRUSHER_BITS": 6,
    "BITCRUSHER_GAIN": 0.25,
    "DRY_SIGNAL": 0.1,
    "FX": 0.9
}

def add_plugin(parent_layout, name, teensy_id, default):
    dial = QDial()
    dial.setMinimum(0)
    dial.setMaximum(100)
    dial.setValue(int(default * 100) if isinstance(default, float) else default * 14)
    dial.setNotchesVisible(True)
    dial.setFixedSize(80, 60)

    label = QLabel(name)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 12px; color: white; padding: 0px; margin: 0px;")

    container = QVBoxLayout()
    container.setSpacing(2)
    container.setContentsMargins(2, 2, 2, 2)
    container.setAlignment(Qt.AlignHCenter)
    container.addWidget(label)
    container.addWidget(dial)
    parent_layout.addLayout(container)

    def throttled_send(value, param=name):
        now = time.time()
        if last_send_times.get(param, 0) + 0.05 < now:
            send_val = value / 100.0 if isinstance(default, float) else int(value / 14.3)
            send_can_message(teensy_id, param, send_val)
            last_send_times[param] = now

    dial.valueChanged.connect(lambda value: throttled_send(value))

plugin_states = {
    "Delay": False,
    "Reverb": False,
    "Chorus": False,
    "Distortion": False,
    "Final Mix": True
}

def show_chorus_voice_dialog(teensy_id):
    dialog = QDialog()
    dialog.setWindowTitle("Select Chorus Voices")
    dialog.setFixedSize(360, 240)
    dialog.setStyleSheet("background-color: #2b2b2b; color: white;")

    layout = QVBoxLayout()

    label = QLabel("Tap a number of voices to use:")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 20px;")
    layout.addWidget(label)

    button_layout = QHBoxLayout()
    button_style = "font-size: 24px; padding: 20px; background-color: #444; color: white; border-radius: 12px;"

    for i in range(1, 5):
        btn = QPushButton(str(i))
        btn.setFixedSize(70, 70)
        btn.setStyleSheet(button_style)
        btn.clicked.connect(lambda _, val=i: (send_can_message(teensy_id, "NUMBER_OF_VOICES", val), dialog.accept()))
        button_layout.addWidget(btn)

    layout.addLayout(button_layout)
    dialog.setLayout(layout)
    dialog.exec_()

def show_delay_settings_dialog(teensy_id):
    dialog = QDialog()
    dialog.setWindowTitle("Configure Delay")
    dialog.setFixedSize(420, 320)
    dialog.setStyleSheet("background-color: #2b2b2b; color: white;")

    layout = QVBoxLayout()

    label1 = QLabel("Select Delay Division:")
    label1.setAlignment(Qt.AlignCenter)
    label1.setStyleSheet("font-size: 18px;")
    layout.addWidget(label1)

    division_layout = QHBoxLayout()
    for div in [1, 2, 4, 8, 16]:
        btn = QPushButton(str(div))
        btn.setFixedSize(60, 60)
        btn.setStyleSheet("font-size: 20px; background-color: #444; color: white; border-radius: 8px;")
        btn.clicked.connect(lambda _, val=div: send_can_message(teensy_id, "DIVISION_MODE", val))
        division_layout.addWidget(btn)
    layout.addLayout(division_layout)

    label2 = QLabel("Select Number of Delays:")
    label2.setAlignment(Qt.AlignCenter)
    label2.setStyleSheet("font-size: 18px; margin-top: 10px; margin-bottom: 10px;")

    layout.addWidget(label2)

    delay_layout = QHBoxLayout()
    for count in [1, 2, 3]:
        btn = QPushButton(str(count))
        btn.setFixedSize(60, 60)
        btn.setStyleSheet("font-size: 20px; background-color: #444; color: white; border-radius: 8px;")
        btn.clicked.connect(lambda _, val=count: send_can_message(teensy_id, "NUMBER_OF_DELAYS", val))
        delay_layout.addWidget(btn)
    layout.addLayout(delay_layout)

    confirm_btn = QPushButton("Confirm and Turn ON Delay")
    confirm_btn.setFixedSize(300, 40)
    confirm_btn.setStyleSheet("font-size: 20px; background-color: #2a82da; color: white; border-radius: 10px;")
    confirm_btn.clicked.connect(lambda: (send_can_message(teensy_id, "Delay Toggle", 1.0), dialog.accept()))
    layout.addWidget(confirm_btn, alignment=Qt.AlignCenter)

    dialog.setLayout(layout)
    dialog.exec_()


def toggle_plugin(plugin_name, button, teensy_id):
    plugin_states[plugin_name] = button.isChecked()
    print(f"{plugin_name} ON: {plugin_states[plugin_name]}")

    toggle_ids = {
        "Delay": "Delay Toggle",
        "Reverb": "Reverb Toggle",
        "Chorus": "Chorus Toggle",
        "Distortion": "Distortion Toggle"
    }

    if plugin_name in toggle_ids:
        send_can_message(teensy_id, toggle_ids[plugin_name], 1.0 if plugin_states[plugin_name] else 0.0)

        if plugin_name == "Chorus" and plugin_states[plugin_name]:
            show_chorus_voice_dialog(teensy_id)
        elif plugin_name == "Delay" and plugin_states[plugin_name]:
            show_delay_settings_dialog(teensy_id)


def create_section(title, controls, teensy_id):
    layout = QVBoxLayout()
    container = QWidget()
    container.setStyleSheet("background-color: #444; border-radius: 8px; padding: 6px;")
    container.setLayout(layout)

    title_button = QPushButton(title)
    title_button.setCheckable(True)
    title_button.setChecked(plugin_states[title])
    title_button.setStyleSheet("""
        QPushButton {
            font-size: 16px;
            font-weight: bold;
            color: white;
            background-color: #666;
            border: none;
            padding: 6px;
            border-radius: 4px;
        }
        QPushButton:checked {
            background-color: #2a82da;
        }
    """)
    title_button.clicked.connect(lambda: toggle_plugin(title, title_button, teensy_id))

    layout.addWidget(title_button)

    knob_layout = QVBoxLayout()
    knob_layout.setSpacing(2)
    knob_layout.setAlignment(Qt.AlignHCenter)
    for control, default in controls:
        add_plugin(knob_layout, control, teensy_id, default)

    layout.addLayout(knob_layout)
    return container

def create_guitar_tab(teensy_id):
    page = QWidget()
    main_layout = QHBoxLayout()
    main_layout.setSpacing(10)
    main_layout.setContentsMargins(10, 10, 10, 10)

    main_layout.addWidget(create_section("Delay", [("BPM", DEFAULT_VALUES["BPM"]), ("NUMBER_OF_DELAYS", DEFAULT_VALUES["NUMBER_OF_DELAYS"]), ("DELAY_GAIN", DEFAULT_VALUES["DELAY_GAIN"])], teensy_id))
    main_layout.addWidget(create_section("Reverb", [("REVERB_TIME", DEFAULT_VALUES["REVERB_TIME"]), ("REVERB_GAIN", DEFAULT_VALUES["REVERB_GAIN"])], teensy_id))
    main_layout.addWidget(create_section("Chorus", [("CHORUS_GAIN", DEFAULT_VALUES["CHORUS_GAIN"]), ("BASE_DELAY_MS", DEFAULT_VALUES["BASE_DELAY_MS"]), ("MOD_DEPTH_MS", DEFAULT_VALUES["MOD_DEPTH_MS"]), ("MOD_RATE_HZ", DEFAULT_VALUES["MOD_RATE_HZ"])], teensy_id))
    main_layout.addWidget(create_section("Distortion", [("BITCRUSHER_GAIN", DEFAULT_VALUES["BITCRUSHER_GAIN"]), ("BITCRUSHER_BITS", DEFAULT_VALUES["BITCRUSHER_BITS"])], teensy_id))
    main_layout.addWidget(create_section("Final Mix", [("DRY_SIGNAL", DEFAULT_VALUES["DRY_SIGNAL"]), ("FX", DEFAULT_VALUES["FX"])], teensy_id))

    page.setLayout(main_layout)
    return page
