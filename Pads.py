from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

def add_midi_pads(layout):
    """ Updated MIDI Pads with 3D effect and proper positioning """
    pad_layout = QGridLayout()
    label = QLabel("🎛️ MIDI Control Pads")
    label.setStyleSheet("font-size: 20px; font-weight: bold;")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)

    for i in range(8):
        button = QPushButton(f"Pad {i+1}")
        button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #666, stop:1 #222);
                color: white;
                border: 4px solid #111;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover { background: #888; }
            QPushButton:pressed { background: #444; }
        """)
        
        # Make the button resize with the layout
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        pad_layout.addWidget(button, i // 4, i % 4)

    layout.addLayout(pad_layout)
    layout.setAlignment(pad_layout, Qt.AlignTop | Qt.AlignLeft)