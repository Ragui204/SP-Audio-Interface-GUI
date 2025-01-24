from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

def add_midi_pads(layout):
    # Create a vertical layout to hold the label and grid
    pads_layout = QVBoxLayout()

    # Add label for MIDI pads
    label = QLabel("MIDI Control Pads")
    label.setAlignment(Qt.AlignCenter)
    pads_layout.addWidget(label)

    # Create a grid layout for the 2x4 MIDI pads
    grid_layout = QGridLayout()

    # Create 8 MIDI pads
    for i in range(8):
        button = QPushButton(f"Pad {i+1}")
        button.setFixedSize(80, 80)  # Square buttons
        button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border: 2px solid #333;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:pressed {
                background-color: #777;
            }
        """)

        # Add buttons to the grid (2 rows, 4 columns)
        grid_layout.addWidget(button, i // 4, i % 4)

    # Add the grid layout to the vertical layout
    pads_layout.addLayout(grid_layout)

    # **Spacer at the bottom to push everything to the top-left**
    bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout.addLayout(pads_layout)
    layout.addItem(bottom_spacer)  # Pushes everything up
    layout.setAlignment(pads_layout, Qt.AlignTop | Qt.AlignLeft)
