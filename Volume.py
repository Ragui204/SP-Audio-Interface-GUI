from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
import can

def send_can_message(bus, address, volume):
    """Send CAN message to adjust volume."""
    if address is None:
        return  # 🎸 Skip sending CAN for Guitar tabs
    message = can.Message(arbitration_id=address, data=[volume], is_extended_id=False)
    try:
        bus.send(message)
        print(f"Sent CAN Message: Address=0x{address:X}, Volume={volume}")
    except can.CanError as e:
        print(f"CAN Error: {e}")

def add_volume_controls(layout, bus, can_address):
    volume_layout = QVBoxLayout()
    volume_label = QLabel("Volume")
    volume_slider = QSlider()
    volume_slider.setOrientation(Qt.Horizontal)
    volume_slider.setMinimum(0)
    volume_slider.setMaximum(100)
    volume_slider.setValue(50)

    volume_slider.valueChanged.connect(lambda value: send_can_message(bus, can_address, value))

    volume_layout.addWidget(volume_label)
    volume_layout.addWidget(volume_slider)
    layout.addLayout(volume_layout)
