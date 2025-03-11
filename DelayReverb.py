from PyQt5.QtWidgets import (
    QApplication, QLabel, QDial, QVBoxLayout, QGridLayout, QHBoxLayout,
    QWidget, QSizePolicy, QFrame, QSpacerItem
)
from PyQt5.QtCore import Qt

def Delay_Reverb_Controls(layout):
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)

    reverb_layout = QVBoxLayout()
    reverb_container = QWidget()
    reverb_container.setStyleSheet("background-color: #555;")
    reverb_container.setLayout(reverb_layout)

    reverb_label = QLabel("Reverb")
    reverb_label.setAlignment(Qt.AlignCenter)
    reverb_layout.addWidget(reverb_label)
    reverb_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
    reverb_grid = QGridLayout()

    add_plugin(reverb_grid, "Decay", 0, 0)
    add_plugin(reverb_grid, "Size", 0, 1)
    add_plugin(reverb_grid, "Mix", 1, 0, 1, 2)  # Centered Mix control

    reverb_layout.addLayout(reverb_grid)
    main_layout.addWidget(reverb_container)
    main_layout.addItem(QSpacerItem(10, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

    divider = QFrame()
    divider.setFrameShape(QFrame.VLine)
    divider.setFrameShadow(QFrame.Sunken)
    main_layout.addWidget(divider)

    delay_layout = QVBoxLayout()
    delay_container = QWidget()
    delay_container.setStyleSheet("background-color: #555;")
    delay_container.setLayout(delay_layout)

    delay_label = QLabel("Delay")
    delay_label.setAlignment(Qt.AlignCenter)
    delay_layout.addWidget(delay_label)
    delay_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
    delay_grid = QGridLayout()

    add_plugin(delay_grid, "Time", 0, 0)
    add_plugin(delay_grid, "Feedback", 0, 1)
    add_plugin(delay_grid, "Mix", 1, 0, 1, 2)  # Centered Mix control
    add_plugin(delay_grid, "Color", 2, 0, 1, 2)  # Centered Color control

    delay_layout.addLayout(delay_grid)
    main_layout.addWidget(delay_container)

    layout.addLayout(main_layout)
    layout.setAlignment(main_layout, Qt.AlignTop | Qt.AlignRight)

def add_plugin(layout, name, row, col, rowspan=1, colspan=1):
    vbox = QVBoxLayout()
    label = QLabel(name)
    label.setAlignment(Qt.AlignCenter)

    dial = QDial()
    dial.setMinimum(0)
    dial.setMaximum(100)
    dial.setValue(50)
    dial.setNotchesVisible(True)

    dial.setStyleSheet("""
        QDial {
            border: 5px solid #5c5c5c;
            border-radius: 50px;
        }
        QDial::handle {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #ffffff, stop:1 #c0c0c0);
            border: 1px solid #5c5c5c;
            width: 20px;
            height: 20px;
            margin: -5px 0;
            border-radius: 10px;
            box-shadow: 2px 2px 5px #888888;
        }
    """)

    vbox.addWidget(label)
    vbox.addWidget(dial)
    layout.addLayout(vbox, row, col, rowspan, colspan)
