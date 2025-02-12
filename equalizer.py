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
    eq_background.setStyleSheet("background-color: #555;")  # Example background color and rounded corners
    eq_container.addWidget(eq_background)  # Add the background frame to the container

    # Add a title label for the EQ
    title_layout = QHBoxLayout()  # Layout for the title
    title_label = QLabel("Equalizer")
    title_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
    title_layout.addWidget(title_label)
    eq_container.addLayout(title_layout)  # Add the title layout to the container

    eq_layout = QHBoxLayout()
    eq_bands = [
        "20 Hz",
        "32 Hz",
        "64 Hz",
        "125 Hz",
        "250 Hz",
        "500 Hz",
        "1 kHz",
        "2 kHz",
        "4 kHz",
        "8 kHz",
        "16 kHz",
        "20 kHz",
    ]

    for band in eq_bands:
        vbox = QVBoxLayout()
        label = QLabel(band)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        slider = QSlider(Qt.Vertical)
        slider.setMinimum(-10)
        slider.setMaximum(10)
        slider.setValue(0)
        slider.setStyleSheet(
            """
            QSlider::groove:vertical {
                background-color: #444;
                width: 50px;
                border-radius: 3px;
            }

            QSlider::handle:vertical {
                background-color: #00FF00;
                border: 1px solid #5c5c5c;
                height: 10px;
                margin: -2px 0;
                border-radius: 5px;
            }

            QSlider {
                min-height: 1000px;
                padding: 2px;
                margin: 5px;
            }
        """
        )
        vbox.addWidget(label)
        vbox.addWidget(slider)
        eq_layout.addLayout(vbox)

    eq_container.addLayout(eq_layout)

    # Add a stretchable spacer below the EQ within the background frame
    spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    eq_container.addItem(spacer)

    # Add the container to the main layout
    layout.addLayout(eq_container)
    layout.setAlignment(eq_layout, Qt.AlignBottom | Qt.AlignLeft)