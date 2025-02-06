from PyQt5.QtWidgets import QLabel, QProgressBar, QSlider, QVBoxLayout, QHBoxLayout 
from PyQt5.QtCore import Qt

def add_equalizer_controls(layout):
    """ Improved Equalizer with Progress Bars """
    eq_layout = QHBoxLayout()
    eq_bands = ["Bass", "Mid", "Treble"]
    
    for band in eq_bands:
        vbox = QVBoxLayout()
        label = QLabel(f"{band}: 50%")
        label.setAlignment(Qt.AlignCenter)
        progress_bar = QProgressBar()
        progress_bar.setOrientation(Qt.Vertical)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setValue(50)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444;
                background-color: #222;
                width: 35px;
            }
            QProgressBar::chunk {
                background-color: #FFD700;
                width: 35px;
            }
        """)
        slider = QSlider()
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.valueChanged.connect(lambda value, lbl=label, bar=progress_bar, name=band: (bar.setValue(value), lbl.setText(f"{name}: {value}%")))
        
        vbox.addWidget(label)
        vbox.addWidget(progress_bar)
        vbox.addWidget(slider)
        eq_layout.addLayout(vbox)
    
    layout.addLayout(eq_layout)
    layout.setAlignment(eq_layout, Qt.AlignBottom | Qt.AlignLeft)