from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt

def add_equalizer_controls(layout):
    eq_layout = QVBoxLayout()
    eq_label = QLabel("Equalizer")
    eq_slider = QSlider()
    eq_slider.setOrientation(Qt.Horizontal)
    eq_slider.setMinimum(0)
    eq_slider.setMaximum(100)
    eq_slider.setValue(50)

    eq_layout.addWidget(eq_label)
    eq_layout.addWidget(eq_slider)
    layout.addLayout(eq_layout)