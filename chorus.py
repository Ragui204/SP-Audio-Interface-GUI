from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt

def add_chorus_controls(layout):
    chorus_layout = QVBoxLayout()
    chorus_label = QLabel("Chorus")
    chorus_slider = QSlider()
    chorus_slider.setOrientation(Qt.Horizontal)
    chorus_slider.setMinimum(0)
    chorus_slider.setMaximum(100)
    chorus_slider.setValue(50)

    chorus_layout.addWidget(chorus_label)
    chorus_layout.addWidget(chorus_slider)
    layout.addLayout(chorus_layout)