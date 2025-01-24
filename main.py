from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt

app = QApplication([])
window = QWidget()
window.setWindowTitle("MIDI-Audio Controller")

layout = QVBoxLayout()
layout.addWidget(QLabel("MIDI-Audio Controller"))

# Volume control layout
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

# Buttons for Volume control
button_layout = QHBoxLayout()
volume_up_button = QPushButton("Volume Up")
volume_down_button = QPushButton("Volume Down")
button_layout.addWidget(volume_down_button)
button_layout.addWidget(volume_up_button)

layout.addLayout(button_layout)

window.setLayout(layout)
window.show()
app.exec()
