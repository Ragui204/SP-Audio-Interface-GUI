from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QHBoxLayout, QProgressBar, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

def add_equalizer_controls(layout):
    # Create a horizontal layout to place bars side by side
    eq_layout = QHBoxLayout()

    # Equalizer Bands (Bass, Mid, Treble)
    eq_bands = [
        ("Bass", 50),
        ("Mid", 50),
        ("Treble", 50)
    ]

    for band, default_value in eq_bands:
        vbox = QVBoxLayout()
        label = QLabel(f"{band}: {default_value}%")
        label.setAlignment(Qt.AlignCenter)

        # QProgressBar for the equalizer bar
        progress_bar = QProgressBar()
        progress_bar.setOrientation(Qt.Vertical)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setValue(default_value)
        progress_bar.setTextVisible(False)  # Hide text inside the bar

        # Function to dynamically update progress bar color
        def update_progress_bar(value, bar=progress_bar, lbl=label, name=band):
            bar.setValue(value)
            lbl.setText(f"{name}: {value}%")

            # Change the fill color dynamically
            color_intensity = int((value / 100) * 255)  # Scale 0-255
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 2px solid #333;
                    border-radius: 5px;
                    background-color: #222;
                    width: 30px;
                }}
                QProgressBar::chunk {{
                    background-color: rgb({color_intensity}, {255 - color_intensity}, 0); /* Dynamic color */
                    width: 30px;
                }}
            """)

        # QSlider to adjust the value
        slider = QSlider(Qt.Vertical)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(default_value)
        slider.valueChanged.connect(update_progress_bar)  # Connect slider to bar update

        # Add widgets to the layout
        vbox.addWidget(label)
        vbox.addWidget(progress_bar)
        vbox.addWidget(slider)

        eq_layout.addLayout(vbox)  # Add each EQ band layout to main horizontal layout

    # Spacer to push equalizer to bottom-left
    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout.addItem(spacer)  # Pushes everything up
    layout.addLayout(eq_layout)
    layout.setAlignment(eq_layout, Qt.AlignBottom | Qt.AlignLeft)
