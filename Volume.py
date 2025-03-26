from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
from can_handler import send_can_message  # Import CAN communication

# Default values for volume
DEFAULT_VOLUME = {
    "Master Volume": 1.0
}

def add_volume_controls(layout, teensy_id):
    volume_layout = QVBoxLayout()
    
    # Master Volume
    master_label = QLabel("Master Volume")
    master_label.setAlignment(Qt.AlignCenter)

    master_slider = QSlider(Qt.Horizontal)
    master_slider.setMinimum(0)
    master_slider.setMaximum(100)
    master_slider.setValue(int(DEFAULT_VOLUME["Master Volume"] * 100))  # Scale to 0-100

    # Send CAN message when adjusted
    master_slider.valueChanged.connect(lambda value: send_can_message(teensy_id, "Master Volume", value / 100.0))

    # Add slider to layout
    volume_layout.addWidget(master_label)
    volume_layout.addWidget(master_slider)

    layout.addLayout(volume_layout)
