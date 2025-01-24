from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from volume import add_volume_controls
from equalizer import add_equalizer_controls
from chorus import add_chorus_controls

def create_window():
    window = QWidget()
    window.setWindowTitle("MIDI-Audio Controller")
    layout = QVBoxLayout()
    layout.addWidget(QLabel("MIDI-Audio Controller"))

    add_volume_controls(layout)
    add_equalizer_controls(layout)
    add_chorus_controls(layout)

    window.setLayout(layout)
    return window