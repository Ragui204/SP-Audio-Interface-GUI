from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout, QDialog
from PyQt5.QtCore import Qt, QTimer
import can
from can_handler import send_can_message, bus, can


SAMPLE_NAMES = {
0: "Kick",
1: "Snare",
2: "Hat",
3: "Clap"
}

class MidiPads(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(350, 150)  
        self.pad_buttons = []
        self.selected_pad = None
        self.midi_mapping = {}  # Store mappings of GUI pads to MIDI notes
        self.init_pads()
        self.setup_can_listener()  # Start listening for MIDI notes via CAN
        self.selected_sample_type = None  # Holds the selected drum sample type


    def init_pads(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        label = QLabel("🎛️ MIDI Control Pads")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        pad_layout = QGridLayout()
        pad_layout.setContentsMargins(5, 5, 5, 5)
        pad_layout.setSpacing(5)

        for i in range(8):
            button = QPushButton(f"Pad {i+1}")
            button.setStyleSheet(self.get_default_style())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(40, 40)
            button.clicked.connect(lambda checked, index=i: self.open_midi_assignment(index))
            self.pad_buttons.append(button)
            pad_layout.addWidget(button, i // 4, i % 4)

        main_layout.addLayout(pad_layout)
        self.setLayout(main_layout)

    def get_default_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #444, stop:1 #222);
                color: white;
                border: 3px solid #111;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: #666;
            }
        """

    def open_midi_assignment(self, pad_index):
        """Opens a popup window for MIDI assignment."""
        self.selected_pad = pad_index
        self.pad_buttons[pad_index].setStyleSheet("background: #44cc44; color: black; border: 3px solid #228822;")
        dialog = MidiAssignmentDialog(self, pad_index)
        dialog.exec_()

    def assign_drum_sample(self, midi_note, sample_type):
        if bus:
            data = bytearray([midi_note, sample_type]) + bytearray(6)
            msg = can.Message(arbitration_id=0x301, data=data, is_extended_id=False)
            try:
                bus.send(msg)
                print(f"🔁 Sent Assignment: MIDI Note {midi_note} -> Sample {sample_type}")
            except can.CanError as e:
                print(f"CAN Error (Assignment): {e}")



    def setup_can_listener(self):
        """Starts listening for incoming CAN MIDI pad assignments."""
        try:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
            self.listener = QTimer(self)
            self.listener.timeout.connect(self.read_can_messages)
            self.listener.start(100)  # Check for messages every 100ms
        except Exception as e:
            print(f"Failed to start CAN listener: {e}")

    def read_can_messages(self):
        try:
            msg = self.bus.recv(timeout=0.1)
            if msg:
                print(f"[CAN] Received: {hex(msg.arbitration_id)} Data: {list(msg.data)}")

            if msg and msg.arbitration_id == 0x300:
                midi_note = msg.data[0]
                if self.selected_pad is not None and self.selected_sample_type is not None:
                    sample_name = SAMPLE_NAMES.get(self.selected_sample_type, "Unknown")
                    
                    # Save assignment
                    self.midi_mapping[midi_note] = self.selected_sample_type
                    self.assign_drum_sample(midi_note, self.selected_sample_type)
                    
                    # Update GUI label
                    button = self.pad_buttons[self.selected_pad]
                    button.setText(f"Pad {self.selected_pad + 1}\nMIDI {midi_note}: {sample_name}")
                    button.setStyleSheet(self.get_default_style())

                    print(f"🟢 Assigned MIDI Note {midi_note} to Sample Type {self.selected_sample_type} ({sample_name})")

                    # Reset state
                    self.selected_pad = None
                    self.selected_sample_type = None
        except Exception as e:
            print(f"Error reading CAN: {e}")



class MidiAssignmentDialog(QDialog):
    """Dialog to select a sample and assign it to a MIDI note."""
    def __init__(self, parent, pad_index):
        super().__init__(parent)
        self.setWindowTitle("Assign Drum Sample")
        self.setGeometry(100, 100, 300, 300)
        self.pad_index = pad_index
        self.parent = parent
        self.sample_type = None  # 0 = kick, 1 = snare, etc.

        layout = QVBoxLayout(self)

        label = QLabel("Select Drum Sample:")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        sample_buttons = [("Kick", 0), ("Snare", 1), ("Hat", 2), ("Clap", 3)]
        for name, sample_id in sample_buttons:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, s=sample_id: self.sample_chosen(s))
            layout.addWidget(btn)

        self.info = QLabel("Then press a pad on your MIDI device.")
        self.info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info)

        self.show()

    def sample_chosen(self, sample_type):
        self.sample_type = sample_type
        self.parent.selected_sample_type = sample_type
        print(f"🎵 Selected Sample Type {sample_type} for GUI Pad {self.pad_index}")

