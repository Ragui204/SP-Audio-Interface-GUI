from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt

def add_volume_controls(layout):
    volume_layout = QVBoxLayout()
    volume_label = QLabel("volume")
    volume_slider = QSlider()
    volume_slider.setOrientation(Qt.Horizontal)
    volume_slider.setMinimum(0)
    volume_slider.setMaximum(100)
    volume_slider.setValue(50)

    volume_layout.addWidget(volume_label)
    volume_layout.addWidget(volume_slider)
    layout.addLayout(volume_layout)