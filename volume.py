from PyQt5.QtWidgets import QLabel, QSlider, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

def add_volume_controls(layout):
    volume_layout = QHBoxLayout()
    volume_label = QLabel("Volume:")
    volume_slider = QSlider()
    volume_slider.setOrientation(Qt.Horizontal)
    volume_slider.setMinimum(0)
    volume_slider.setMaximum(100)
    volume_slider.setValue(50)

    volume_layout.addWidget(volume_label)
    volume_layout.addWidget(volume_slider)
    layout.addLayout(volume_layout)

    button_layout = QHBoxLayout()
    volume_up_button = QPushButton("Volume Up")
    volume_down_button = QPushButton("Volume Down")
    button_layout.addWidget(volume_down_button)
    button_layout.addWidget(volume_up_button)
    layout.addLayout(button_layout)