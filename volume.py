from PyQt5.QtWidgets import QLabel, QDial, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

def add_volume_controls(layout):
    # Create a vertical layout for the volume control
    volume_layout = QVBoxLayout()

    # Volume Label
    volume_label = QLabel("Volume: 50%")
    volume_label.setAlignment(Qt.AlignCenter)

    # QDial for volume control
    volume_knob = QDial()
    volume_knob.setMinimum(0)
    volume_knob.setMaximum(100)
    volume_knob.setValue(50)
    volume_knob.setNotchesVisible(True)

    # Function to update label text
    def update_volume(value):
        volume_label.setText(f"Volume: {value}%")

    volume_knob.valueChanged.connect(update_volume)  # Update volume label dynamically

    # Add spacer to push the control to the top-right
    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

    # Add widgets to the volume layout
    volume_layout.addWidget(volume_label)
    volume_layout.addWidget(volume_knob)
    volume_layout.addItem(spacer)  # Pushes everything to the top

    # Align to top-right
    layout.addLayout(volume_layout)
    layout.setAlignment(volume_layout, Qt.AlignTop | Qt.AlignRight)
