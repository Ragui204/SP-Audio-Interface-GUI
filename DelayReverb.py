from PyQt5.QtWidgets import QLabel, QDial, QVBoxLayout, QGridLayout, QHBoxLayout, QWidget, QSizePolicy, QFrame, QSpacerItem, QPushButton
from PyQt5.QtCore import Qt
from can_handler import send_can_message  # Import CAN communication

# Mapping shortened UI names to correct CAN parameter names
CAN_PARAM_MAPPING = {
    "Size": "Reverb Size",
    "Decay": "Reverb Decay",
    "Mix": "Reverb Mix",
    "Time": "Delay Time",
    "Color": "Delay Color"
}

# Default values from Teensy variables (converted to integers for dials)
DEFAULT_VALUES = {
    "Size": int(0.0 * 100),
    "Decay": int(0.0 * 100),
    "Mix": int(0.0 * 100),
    "Time": int(0),  # Time in milliseconds (0-1200ms)
    "Color": int(0.0 * 100)
}

# Store dials in a dictionary for reset functionality
dials_dict = {}

def add_plugin(layout, name, row, col, teensy_id, initial_value=None, rowspan=1, colspan=1):
    vbox = QVBoxLayout()
    label = QLabel(name)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

    dial = QDial()

    # Adjust range for "Time" dial
    if name == "Time":
        dial.setMinimum(0)
        dial.setMaximum(1200)  # Set max to 1200ms
        dial.setValue(int(initial_value) if initial_value is not None else 0)
    else:
        dial.setMinimum(0)
        dial.setMaximum(100)
        dial.setValue(int(initial_value) if initial_value is not None else 0)

    dial.setNotchesVisible(True)
    dial.setFixedSize(82, 81)  # **Size remains unchanged**

    # Ensure correct CAN parameter is used
    can_param = CAN_PARAM_MAPPING.get(name, name)

    # Send CAN message when value changes
    dial.valueChanged.connect(lambda value: send_can_message(teensy_id, can_param, value if name == "Time" else value / 100.0))

    # Store dial for reset functionality
    dials_dict[name] = dial

    vbox.addWidget(label)
    vbox.addWidget(dial)
    layout.addLayout(vbox, row, col, rowspan, colspan)

def create_reset_button(section_name, section_dials, teensy_id):
    """Creates a reset button that resets all dials in a section without changing layout."""
    reset_button = QPushButton(f"Reset {section_name}")
    reset_button.setStyleSheet("font-size: 14px; padding: 5px; background-color: #555; color: white; border-radius: 5px;")
    
    def reset_values():
        for dial_name in section_dials:
            if dial_name in dials_dict:
                default_value = DEFAULT_VALUES.get(dial_name, 0)
                dials_dict[dial_name].setValue(default_value)  # Reset UI
                send_can_message(teensy_id, CAN_PARAM_MAPPING.get(dial_name, dial_name), default_value if dial_name == "Time" else default_value / 100.0)
    
    reset_button.clicked.connect(reset_values)
    return reset_button

def Delay_Reverb_Controls(layout, teensy_id):
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(3, 3, 3, 3)
    main_layout.setSpacing(5)

    # Reverb Section
    reverb_layout = QVBoxLayout()
    reverb_container = QWidget()
    reverb_container.setStyleSheet("background-color: #444; border-radius: 8px; padding: 3px; min-height: 35px;")
    reverb_container.setLayout(reverb_layout)

    reverb_label = QLabel("Reverb")
    reverb_label.setAlignment(Qt.AlignCenter)
    reverb_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
    reverb_layout.addWidget(reverb_label)

    reverb_grid = QGridLayout()
    add_plugin(reverb_grid, "Size", 1, 0, teensy_id, DEFAULT_VALUES["Size"])
    add_plugin(reverb_grid, "Decay", 1, 1, teensy_id, DEFAULT_VALUES["Decay"])
    add_plugin(reverb_grid, "Mix", 2, 1, teensy_id, DEFAULT_VALUES["Mix"])

    reverb_layout.addLayout(reverb_grid)

    # Add reset button below the section (No size change)
    reverb_reset_layout = QVBoxLayout()
    reverb_reset_layout.addWidget(create_reset_button("Reverb", ["Size", "Decay", "Mix"], teensy_id))
    reverb_reset_layout.setAlignment(Qt.AlignCenter)  # Center reset button
    reverb_layout.addLayout(reverb_reset_layout)

    main_layout.addWidget(reverb_container)

    main_layout.addItem(QSpacerItem(2, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

    divider = QFrame()
    divider.setFrameShape(QFrame.VLine)
    divider.setFrameShadow(QFrame.Sunken)
    main_layout.addWidget(divider)

    # Delay Section
    delay_layout = QVBoxLayout()
    delay_container = QWidget()
    delay_container.setStyleSheet("background-color: #444; border-radius: 8px; padding: 3px; min-height: 35px;")
    delay_container.setLayout(delay_layout)

    delay_label = QLabel("Delay")
    delay_label.setAlignment(Qt.AlignCenter)
    delay_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
    delay_layout.addWidget(delay_label)

    delay_grid = QGridLayout()
    add_plugin(delay_grid, "Time", 1, 0, teensy_id, DEFAULT_VALUES["Time"])
    add_plugin(delay_grid, "Mix", 1, 1, teensy_id, DEFAULT_VALUES["Mix"])
    add_plugin(delay_grid, "Color", 2, 1, teensy_id, DEFAULT_VALUES["Color"])

    delay_layout.addLayout(delay_grid)

    # Add reset button below the section (No size change)
    delay_reset_layout = QVBoxLayout()
    delay_reset_layout.addWidget(create_reset_button("Delay", ["Time", "Mix", "Color"], teensy_id))
    delay_reset_layout.setAlignment(Qt.AlignCenter)  # Center reset button
    delay_layout.addLayout(delay_reset_layout)

    main_layout.addWidget(delay_container)

    layout.addLayout(main_layout)
