from PyQt5.QtWidgets import (
    QLabel,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QWidget,
    QFrame,
)
from PyQt5.QtCore import Qt

def add_equalizer_controls(layout):
    """
    Adds equalizer controls with frequencies, similar to the image.
    """
    # Create a container for the EQ, spacer, and title with a background
    eq_container = QVBoxLayout()
    eq_background = QFrame()
    eq_background.setStyleSheet("background-color: #555;")
    eq_container.addWidget(eq_background)

    # Add a title label for the EQ
    title_layout = QHBoxLayout()
    title_label = QLabel("Equalizer")
    title_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
    title_layout.addWidget(title_label)
    eq_container.addLayout(title_layout)

    eq_layout = QHBoxLayout()
    eq_bands = [
        "31Hz", "125Hz", "500Hz", "2kHz", "8kHz",
        "16kHz"
    ]

    for band in eq_bands:
        vbox = QVBoxLayout()
        label = QLabel(band)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        slider = QSlider(Qt.Vertical)
        slider.setMinimum(-10)
        slider.setMaximum(10)
        slider.setValue(0)
        slider.setStyleSheet("""
            QSlider::groove:vertical {
                background-color: #444;
                width: 25px; 
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                background-color: #00FF00;
                border: 1px solid #5c5c5c;
                height: 15px; 
                margin: -2px 0;
                border-radius: 5px;
            }
            QSlider {
                min-height: 150px;  /* Changed from 200px */
                padding: 1px; 
                margin: 2px; 
            }
        """)
        vbox.addWidget(label)
        vbox.addWidget(slider)
        eq_layout.addLayout(vbox)

    eq_container.addLayout(eq_layout)

    # Spacer below the EQ
    spacer = QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Preferred)
    eq_container.addItem(spacer)

    layout.addLayout(eq_container)
    layout.setAlignment(eq_layout, Qt.AlignBottom | Qt.AlignLeft)