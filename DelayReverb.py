from PyQt5.QtWidgets import (
    QApplication, QLabel, QDial, QVBoxLayout, QGridLayout, QHBoxLayout,
    QWidget, QSizePolicy, QFrame, QSpacerItem
)
from PyQt5.QtCore import Qt
import can  # ✅ Add import for CAN messaging

def Delay_Reverb_Controls(layout, bus=None, can_address=None):
    """
    Adds volume controls and other plugin controls to the layout.
    This version supports CAN messaging for reverb controls.
    """
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)

    # Reverb
    reverb_layout = QVBoxLayout()
    reverb_container = QWidget()
    reverb_container.setStyleSheet("background-color: #555;")
    reverb_container.setLayout(reverb_layout)

    reverb_label = QLabel("Reverb")
    reverb_label.setAlignment(Qt.AlignCenter)
    reverb_layout.addWidget(reverb_label)
    reverb_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
    reverb_grid = QGridLayout()

    # ✅ Add CAN-enabled dials
    add_plugin(reverb_grid, "Decay", 0, 0, bus, can_address, 0x02)
    add_plugin(reverb_grid, "Size", 0, 1, bus, can_address, 0x03)
    add_plugin(reverb_grid, "Mix", 0, 2, bus, can_address, 0x04)
    add_plugin(reverb_grid, "Color", 1, 0, bus, can_address, 0x05)
    add_plugin(reverb_grid, "Mod", 1, 1, bus, can_address, 0x06)
    add_plugin(reverb_grid, "Speed", 1, 2, bus, can_address, 0x07)

    reverb_layout.addLayout(reverb_grid)
    main_layout.addWidget(reverb_container)
    main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

    # Add divider
    divider = QFrame()
    divider.setFrameShape(QFrame.VLine)
    divider.setFrameShadow(QFrame.Sunken)
    main_layout.addWidget(divider)

    # Delay
    delay_layout = QVBoxLayout()
    delay_container = QWidget()
    delay_container.setStyleSheet("background-color: #555;")
    delay_container.setLayout(delay_layout)

    delay_label = QLabel("Delay")
    delay_label.setAlignment(Qt.AlignCenter)
    delay_layout.addWidget(delay_label)
    delay_layout.addItem(QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Fixed))
    delay_grid = QGridLayout()

    # ✅ Add CAN-enabled dials (optional — you can disable CAN for delay if you want)
    add_plugin(delay_grid, "Time", 0, 0, bus, can_address, 0x08)
    add_plugin(delay_grid, "Feedback", 0, 1, bus, can_address, 0x09)
    add_plugin(delay_grid, "Mix", 0, 2, bus, can_address, 0x0A)
    add_plugin(delay_grid, "Color", 1, 0, bus, can_address, 0x0B)
    add_plugin(delay_grid, "Mod", 1, 1, bus, can_address, 0x0C)

    delay_layout.addLayout(delay_grid)
    main_layout.addWidget(delay_container)

    layout.addLayout(main_layout)
    layout.setAlignment(main_layout, Qt.AlignTop | Qt.AlignRight)

def add_plugin(layout, name, row, col, bus, can_address, command):
    """
    Adds a plugin control (dial) with optional CAN messaging support.
    """
    vbox = QVBoxLayout()
    label = QLabel(name)
    label.setAlignment(Qt.AlignCenter)

    dial = QDial()
    dial.setMinimum(0)
    dial.setMaximum(100)
    dial.setValue(50)
    dial.setNotchesVisible(True)

    # ✅ Send CAN message on value change
    if bus and can_address:
        dial.valueChanged.connect(lambda value: send_can_message(bus, can_address, command, value))

    # Styling preserved from original code
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
    layout.addLayout(vbox, row, col)

def send_can_message(bus, address, command, value):
    """
    Send a CAN message for a specific control.
    Data structure: [command, value]
    """
    message = can.Message(arbitration_id=address, data=[command, value], is_extended_id=False)
    try:
        bus.send(message)
        print(f"Sent CAN Message: Address=0x{address:X}, Command=0x{command:02X}, Value={value}")
    except can.CanError as e:
        print(f"CAN Error: {e}")
