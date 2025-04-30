import json
import os
import can
from PyQt5.QtWidgets import (
    QPushButton, QGridLayout, QLabel, QSizePolicy, QVBoxLayout,
    QWidget, QDialog, QHBoxLayout, QMessageBox, QSpacerItem, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

from can_handler import bus  # Shared CAN bus

SAMPLE_NAMES = {
    0: "Kick",
    1: "Snare",
    2: "Hat",
    3: "Clap",
    4: "Perc"
}

PAD_MAPPING_FILE = "pad_mappings.json"
MIDI_NOTE_ID = 0x100
DRUM_ASSIGNMENT_ID = 0x101

class CANReceiver(QThread):
    note_received = pyqtSignal(int)

    def __init__(self, note_ids):
        super().__init__()
        self.running = True
        self.note_ids = note_ids if isinstance(note_ids, list) else [note_ids]
        try:
            self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
        except Exception as e:
            print(f"CAN Bus init failed in CANReceiver: {e}")
            self.bus = None

    def run(self):
        if not self.bus:
            return
        while self.running:
            try:
                msg = self.bus.recv(timeout=0.05)
                if msg and msg.arbitration_id in self.note_ids and msg.dlc >= 1:
                    note = msg.data[0]
                    self.note_received.emit(note)
            except Exception as e:
                print(f"CANReceiver error: {e}")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()



class MidiAssignmentDialog(QDialog):
    def __init__(self, parent, pad_index, midi_note_id, drum_assignment_id):
        super().__init__(parent)
        self.setWindowTitle("Assign MIDI Pad")
        self.setMinimumSize(400, 400)
        self.pad_index = pad_index
        self.parent = parent
        self.current_note = None
        self.selected_drum = None
        self.drum_assignment_id = drum_assignment_id


        layout = QVBoxLayout()
        self.note_display = QLabel("Last Note: None")
        self.note_display.setAlignment(Qt.AlignCenter)
        self.note_display.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.note_display)

        for sample_id, name in SAMPLE_NAMES.items():
            btn = QPushButton(f"Assign to {name}")
            btn.setMinimumHeight(70)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 25px;
                    font-weight: bold;
                    color: white;
                    background-color: grey;
                    border: 2px solid #666;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: green;
                    color: black;
                }
            """)

            btn.clicked.connect(lambda _, s=sample_id: self.assign_sample(s))
            layout.addWidget(btn)

        layout.addSpacerItem(QSpacerItem(0, 10))

        save_btn = QPushButton("✅ Save Mapping")
        save_btn.setMinimumHeight(60)
        save_btn.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #222; color: #000;")
        save_btn.clicked.connect(self.save_mapping)
        layout.addWidget(save_btn)

        self.setLayout(layout)

        self.receiver = CANReceiver([midi_note_id])
        self.receiver.note_received.connect(self.update_note)
        self.receiver.start()

    def update_note(self, note):
        self.current_note = note
        self.note_display.setText(f"Last Note: {note}")

    def assign_sample(self, sample_type):
        if self.current_note is None:
            QMessageBox.warning(self, "No MIDI Note", "You must play a note first.")
            return
        selector = DrumSampleSelector(self, sample_type, self.current_note, self.drum_assignment_id)
        if selector.exec_() == QDialog.Accepted:
            self.selected_drum = sample_type
            self.selected_sample_index = selector.selected_sample_index  # ✅ Store the selected index
            drum_name = SAMPLE_NAMES[sample_type]
            self.note_display.setText(
                f"Assigned {drum_name} #{self.selected_sample_index} to Note {self.current_note}"
            )


    # replaced original assign_sample

        self.selected_drum = sample_type
        QMessageBox.information(self, "Assigned", f"Selected: {SAMPLE_NAMES[sample_type]}")

    def save_mapping(self):
        if self.current_note is not None and self.selected_drum is not None and hasattr(self, "selected_sample_index"):
            self.parent.save_pad_assignment(
                self.pad_index,
                self.current_note,
                SAMPLE_NAMES[self.selected_drum],
                self.selected_sample_index  # ✅ Pass the selected sample index
            )
            self.parent.send_full_drum_mapping()
            self.receiver.stop()
            self.accept()
        else:
            QMessageBox.warning(self, "Incomplete", "You must select a MIDI note and drum sample before saving.")


    def closeEvent(self, event):
        self.receiver.stop()
        event.accept()


class MidiPads(QWidget):
    def __init__(self, parent=None, teensy_id=0x100):
        super().__init__(parent)
        self.setFixedSize(360, 200)
        self.pad_buttons = []
        self.midi_mapping = {}
        self.teensy_id = teensy_id
        self.midi_note_id = teensy_id
        self.drum_assignment_id = teensy_id + 1
        self.load_mappings()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("\ud83c\udfa7 MIDI Pads")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-weight: bold; font-size: 20px; color: white;")
        layout.addWidget(label)

        grid = QGridLayout()
        for i in range(8):
            btn = QPushButton(f"Pad {i+1}")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setMinimumSize(40, 40)
            btn.setStyleSheet(self.get_default_style())
            btn.clicked.connect(lambda _, idx=i: self.open_mapper(idx))
            self.pad_buttons.append(btn)
            grid.addWidget(btn, i // 4, i % 4)
        layout.addLayout(grid)
        self.setLayout(layout)
        self.update_buttons()

    def open_mapper(self, pad_index):
        dialog = MidiAssignmentDialog(self, pad_index, self.midi_note_id, self.drum_assignment_id)

        dialog.exec_()


    def save_pad_assignment(self, pad_index, midi_note, drum, sample_index):
        self.midi_mapping[pad_index] = {
            "note": midi_note,
            "sample": drum,
            "sample_index": sample_index  # ✅ Now stores the actual sample index
        }
        self.update_buttons()
        self.save_mappings()


    def send_full_drum_mapping(self):
        sample_to_note = {name: 0 for name in SAMPLE_NAMES.values()}
        for entry in self.midi_mapping.values():
            sample_to_note[entry["sample"]] = entry["note"]

        data = [
            sample_to_note.get("Kick", 0),
            sample_to_note.get("Snare", 0),
            sample_to_note.get("Hat", 0),
            sample_to_note.get("Clap", 0),
            sample_to_note.get("Perc", 0) 
        ]

        msg = can.Message(arbitration_id=self.drum_assignment_id, data=bytearray(data), is_extended_id=False)
        try:
            bus.send(msg)
            print(f"[CAN] Sent drum mapping: {data}")
        except can.CanError as e:
            print(f"CAN Send Failed: {e}")

    def update_buttons(self):
        for i, btn in enumerate(self.pad_buttons):
            if i in self.midi_mapping:
                data = self.midi_mapping[i]
                btn.setText(f"Pad {i+1}\n{data['sample']}\n{data['note']}")
                btn.setStyleSheet("background: #44cc44; color: black; font-size: 15px; border: 3px solid #228822;")
            else:
                btn.setText(f"Pad {i+1}")
                btn.setStyleSheet(self.get_default_style())

    def get_default_style(self):
        return ("QPushButton { background-color: #444; color: white; border: 2px solid #111; border-radius: 6px; font-size: 20px; }")

    def load_mappings(self):
        if os.path.exists(PAD_MAPPING_FILE):
            with open(PAD_MAPPING_FILE, 'r') as f:
                self.midi_mapping = json.load(f)

    def save_mappings(self):
        with open(PAD_MAPPING_FILE, 'w') as f:
            json.dump(self.midi_mapping, f, indent=2)

KICK_SAMPLE_NAMES = [
    "Kick 1985", "Kick asacschrader", "Kick boiler", "Kick borefest2021",
    "Kick chipsynth", "Kick coffeeshop", "Kick darkroom", "Kick devastate",
    "Kick duster", "Kick edgy", "Kick fistpump", "Kick glitcher",
    "Kick grandmaster", "Kick hard", "Kick it", "Kick juicy",
    "Kick juno", "Kick lorida", "Kick lowrez", "Kick mecha",
    "Kick nailgun", "Kick neato", "Kick oceanbreeze", "Kick pots",
    "Kick quake", "Kick retro", "Kick roundabout", "Kick rummmmble",
    "Kick shower", "Kick showstopper", "Kick slowlow", "Kick sonya",
    "Kick swooshy", "Kick tekk", "Kick thumpster", "Kick tight",
    "Kick tron"
]

SNARE_SAMPLE_NAMES = [
    "Snare 1982drive", "Snare analog", "Snare blackout", "Snare breathe",
    "Snare cassette", "Snare clappersdelight", "Snare crushed", "Snare datasette",
    "Snare doublebarrel", "Snare duotone", "Snare 808", "Snare frogger",
    "Snare gnr", "Snare hypemachine", "Snare jet", "Snare lastbar",
    "Snare lofi", "Snare 909", "Snare nudisco", "Snare offgrid",
    "Snare og", "Snare papercut", "Snare piccolo", "Snare retro",
    "Snare slammer", "Snare smoochie", "Snare snapper", "Snare suction",
    "Snare tapestop", "Snare tight", "Snare trapped", "Snare urban",
    "Snare ussr", "Snare verbotron", "Snare vhs", "Snare vinyl"
]

HAT_SAMPLE_NAMES = [
    "Hat massamolla", "Hat metal", "Hat micro", "Hat noise",
    "Hat pedal", "Hat salty", "Hat sizzle", "Hat springwater",
    "Hat stutter", "Hat sweet", "Hat vinyl", "Hat wonky",
    "Hat zippo"
]

CLAP_SAMPLE_NAMES = [
    "Clap crackle1", "Clap crackle2", "Clap crackle3", "Clap crackle4",
    "Clap flange", "Clap giannis", "Clap liquid", "Clap neat",
    "Clap tape", "Clap vinyl1", "Clap vinyl2"
]

PERC_SAMPLE_NAMES = [
    "Perc Analog 1", "Perc Analog 2", "Perc Box", "Perc Digital Noise",
    "Perc Kungfu", "Perc Old Computer", "Perc Retro Stick", "Perc Skipper",
    "Perc Springboard", "Perc Tambo", "Perc Tomtom", "Perc Transit", "Perc Wobble"
]



class DrumSampleSelector(QDialog):
    def __init__(self, parent, drum_type, note, drum_assignment_id):
        super().__init__(parent)
        self.setWindowTitle("Choose Drum Sample")
        self.setMinimumSize(300, 400)
        self.drum_type = drum_type
        self.note = note
        self.drum_assignment_id = drum_assignment_id
        self.selected_sample_index = None
        

        self.layout = QVBoxLayout()
        self.scroll_area = QVBoxLayout()

        sample_names = {
            0: KICK_SAMPLE_NAMES,
            1: SNARE_SAMPLE_NAMES,
            2: HAT_SAMPLE_NAMES,
            3: CLAP_SAMPLE_NAMES,
            4: PERC_SAMPLE_NAMES 
        }.get(drum_type, [])


        for i, name in enumerate(sample_names):
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 25px;
                    font-weight: bold;
                    color: white;           /* <-- TEXT COLOR */
                    background-color: grey; /* <-- BUTTON BG COLOR */
                    border: 2px solid #666;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: green;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda _, idx=i: self.select_sample(idx))
            self.scroll_area.addWidget(btn)



        scroll_widget = QWidget()
        scroll_widget.setLayout(self.scroll_area)

        scroll_area_wrapper = QScrollArea()
        scroll_area_wrapper.setWidgetResizable(True)
        scroll_area_wrapper.setWidget(scroll_widget)

        self.layout.addWidget(scroll_area_wrapper)
        self.setLayout(self.layout)

    def select_sample(self, sample_index):
        msg = can.Message(
            arbitration_id=(self.drum_assignment_id & 0xFF00) | 0x10,  # This makes 0x110 for 0x100, or 0x210 for 0x200
            data=bytearray([self.note, self.drum_type, sample_index]),
            is_extended_id=False
        )

        try:
            bus.send(msg)
            print(f"[CAN] Sent sample mapping: note={self.note}, type={self.drum_type}, sample={sample_index}")
        except can.CanError as e:
            print(f"CAN send failed: {e}")
        self.accept()
