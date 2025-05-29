from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QFrame, QGridLayout
from PyQt5.QtCore import Qt
from can_handler import send_can_message

WAVEFORMS = ["Sine", "Square", "Triangle", "Sawtooth"]

def add_waveform_selector(layout, teensy_id):
    container = QVBoxLayout()
    frame = QFrame()
    frame.setStyleSheet("background-color: #555; border-radius: 8px; padding: 5px;")
    frame_layout = QVBoxLayout(frame)

    label = QLabel("Waveform")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
    frame_layout.addWidget(label)

    grid_layout = QGridLayout()
    buttons = []

    def set_selected(index):
        for i, btn in enumerate(buttons):
            if i == index:
                btn.setStyleSheet("""
                    background-color: #00CC66;
                    color: black;
                    font-weight: bold;
                    border-radius: 6px;
                    padding: 10px;
                """)
            else:
                btn.setStyleSheet("""
                    background-color: #333;
                    color: white;
                    border-radius: 6px;
                    padding: 10px;
                """)
        send_can_message(teensy_id, "Waveform", index)

    for i, name in enumerate(WAVEFORMS):
        btn = QPushButton(name)
        btn.setMinimumSize(55, 30)
        btn.clicked.connect(lambda checked, idx=i: set_selected(idx))
        buttons.append(btn)
        row, col = divmod(i, 2)
        grid_layout.addWidget(btn, row, col)

    set_selected(0)  # Default to Sine
    frame_layout.addLayout(grid_layout)
    container.addWidget(frame)
    layout.addLayout(container)
