from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QSizePolicy, QFileDialog, QDialog, QVBoxLayout, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

class MidiPads:
    def __init__(self, layout):
        self.pad_buttons = []
        self.selected_pad = None
        self.pad_midi_mapping = {}  # Store MIDI mappings
        self.pad_sound_mapping = {}  # Store sound file mappings
        self.init_pads(layout)
    
    def init_pads(self, layout):
        pad_layout = QGridLayout()
        pad_layout.setContentsMargins(10, 10, 10, 10)
        label = QLabel("🎛️ MIDI Control Pads")
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        for i in range(8):
            button = QPushButton(f"Pad {i+1}")
            button.setStyleSheet(self.get_pad_style(i))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            button.clicked.connect(lambda checked, index=i: self.select_pad(index))
            self.pad_buttons.append(button)
            pad_layout.addWidget(button, i // 4, i % 4)

        layout.addLayout(pad_layout)
        layout.setAlignment(pad_layout, Qt.AlignTop | Qt.AlignLeft)

    def get_pad_style(self, index):
        if index in self.pad_midi_mapping:
            return self.get_assigned_style()
        return self.get_default_style()

    def get_default_style(self):
        return """
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
        """
    
    def get_selected_style(self):
        return """
            QPushButton {
                background: #ff8800;
                color: black;
                border: 4px solid #ff5500;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """
    
    def get_assigned_style(self):
        return """
            QPushButton {
                background: #ff8800;
                color: black;
                border: 4px solid #ff5500;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """
    
    def select_pad(self, index):
        if self.selected_pad is not None:
            self.pad_buttons[self.selected_pad].setStyleSheet(self.get_pad_style(self.selected_pad))
        self.selected_pad = index
        self.pad_buttons[index].setStyleSheet(self.get_selected_style())
        self.show_pad_details()
    
    def show_pad_details(self):
        if self.selected_pad is None:
            return
        
        dialog = QDialog()
        dialog.setWindowTitle(f"Pad {self.selected_pad + 1}")
        layout = QVBoxLayout()
        
        midi_label = QLabel(f"Assign Pad: {self.pad_midi_mapping.get(self.selected_pad, 'None')}")
        layout.addWidget(midi_label)
        
        assign_button = QPushButton("Assign Key")
        assign_button.clicked.connect(lambda: self.wait_for_keypress(dialog, midi_label))
        layout.addWidget(assign_button)
        
        load_sample_btn = QPushButton("Import...")
        load_sample_btn.clicked.connect(self.assign_sound)
        layout.addWidget(QLabel("Load Samples:"))
        layout.addWidget(load_sample_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def wait_for_keypress(self, parent, label):
        key_dialog = QDialog(parent)
        key_dialog.setWindowTitle("Press a Key to Assign")
        key_dialog.setModal(True)
        key_dialog.resize(200, 100)
        key_dialog.keyPressEvent = lambda event: self.set_assigned_key(event, key_dialog, label)
        key_dialog.exec_()
    
    def set_assigned_key(self, event, dialog, label):
        key = event.text().upper()
        if self.selected_pad is not None and key:
            self.pad_midi_mapping[self.selected_pad] = key
            label.setText(f"Assign Pad: {key}")
            self.pad_buttons[self.selected_pad].setStyleSheet(self.get_assigned_style())
            dialog.accept()
    
    def assign_sound(self):
        if self.selected_pad is not None:
            file_path, _ = QFileDialog.getOpenFileName(None, "Select Sound File", "", "Audio Files (*.wav *.mp3)")
            if file_path:
                self.pad_sound_mapping[self.selected_pad] = file_path
                print(f"Assigned Sound {file_path} to Pad {self.selected_pad + 1}")

def add_midi_pads(layout):
    midi_pads = MidiPads(layout)
    return midi_pads
