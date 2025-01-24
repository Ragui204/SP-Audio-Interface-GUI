from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

def add_navigation_bar(layout, window):
    # Create a horizontal layout for the navigation bar
    nav_layout = QHBoxLayout()

    # Sections for MIDI1, MIDI2, Guitar1, Guitar2
    sections = [
        ("MIDI1", window.show_midi1),
        ("MIDI2", window.show_midi2),
        ("Guitar1", window.show_guitar1),
        ("Guitar2", window.show_guitar2)
    ]

    for label, function in sections:
        button = QPushButton(label)
        button.setFixedSize(150, 50)  # Adjust button size
        button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: 2px solid #222;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        button.clicked.connect(function)  # Connect button to GUI switch
        nav_layout.addWidget(button)

    layout.addLayout(nav_layout)
    layout.setAlignment(Qt.AlignTop)  # Keep it at the top
