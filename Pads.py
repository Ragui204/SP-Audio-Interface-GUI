from PyQt5.QtWidgets import (
    QPushButton, QGridLayout, QLabel, QSizePolicy, QDialog, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QPushButton
)
from PyQt5.QtCore import Qt
import os
import sounddevice as sd
import soundfile as sf

DRUM_SAMPLES_FOLDER = "drum_samples"

class MidiPads:
    def __init__(self, layout):
        self.pad_buttons = []
        self.selected_pad = None
        self.pad_midi_mapping = {}
        self.pad_sound_mapping = {}
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
        if index in self.pad_sound_mapping:
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
        """

    def get_assigned_style(self):
        return """
            QPushButton {
                background: #44cc44;
                color: black;
                border: 4px solid #228822;
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
        self.pad_buttons[index].setStyleSheet(self.get_assigned_style())
        self.show_pad_details()

    def show_pad_details(self):
        if self.selected_pad is None:
            return

        dialog = QDialog()
        dialog.setWindowTitle(f"Pad {self.selected_pad + 1}")
        layout = QVBoxLayout()

        midi_label = QLabel(f"Assigned Key: {self.pad_midi_mapping.get(self.selected_pad, 'None')}")
        layout.addWidget(midi_label)

        assign_button = QPushButton("Assign Key")
        assign_button.clicked.connect(lambda: self.wait_for_keypress(dialog, midi_label))
        layout.addWidget(assign_button)

        load_sample_btn = QPushButton("Import Sample...")
        load_sample_btn.clicked.connect(self.assign_sound)
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
            label.setText(f"Assigned Key: {key}")
            self.pad_buttons[self.selected_pad].setStyleSheet(self.get_assigned_style())
            dialog.accept()

    def assign_sound(self):
        if self.selected_pad is None:
            return

        dialog = QDialog()
        dialog.setWindowTitle("Select Drum Sample")
        layout = QVBoxLayout()

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.populate_tree_widget()

        layout.addWidget(self.tree_widget)

        assign_button = QPushButton("Assign Selected Sound")
        assign_button.clicked.connect(lambda: self.confirm_tree_sound_assignment(dialog))
        layout.addWidget(assign_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def populate_tree_widget(self):
        self.tree_widget.clear()

        if not os.path.exists(DRUM_SAMPLES_FOLDER):
            os.makedirs(DRUM_SAMPLES_FOLDER)

        for genre in sorted(os.listdir(DRUM_SAMPLES_FOLDER)):
            genre_path = os.path.join(DRUM_SAMPLES_FOLDER, genre)
            if not os.path.isdir(genre_path):
                continue

            genre_item = QTreeWidgetItem([genre])

            for item in sorted(os.listdir(genre_path)):
                item_path = os.path.join(genre_path, item)

                if os.path.isdir(item_path):
                    type_item = QTreeWidgetItem([item])
                    genre_item.addChild(type_item)

                    for sample_file in sorted(os.listdir(item_path)):
                        if sample_file.endswith(('.wav', '.mp3')):
                            sample_item = QTreeWidgetItem([sample_file])
                            type_item.addChild(sample_item)
                elif item.endswith(('.wav', '.mp3')):
                    sample_item = QTreeWidgetItem([item])
                    genre_item.addChild(sample_item)

            self.tree_widget.addTopLevelItem(genre_item)

    def confirm_tree_sound_assignment(self, dialog):
        selected_item = self.tree_widget.currentItem()

        if not selected_item:
            print("Please select a valid sound file.")
            return

        path_parts = []
        item = selected_item
        while item is not None:
            path_parts.insert(0, item.text(0))
            item = item.parent()

        if len(path_parts) < 2:
            print("Please select a valid sound file.")
            return

        full_path = os.path.join(DRUM_SAMPLES_FOLDER, *path_parts)
        self.pad_sound_mapping[self.selected_pad] = full_path
        print(f"Assigned Sound {path_parts[-1]} to Pad {self.selected_pad + 1}")
        dialog.accept()

    def handle_key_event(self, event):
        key = event.text().upper()
        for pad, assigned_key in self.pad_midi_mapping.items():
            if key == assigned_key:
                self.play_pad_sound(pad)

    def play_pad_sound(self, pad_index):
        if pad_index in self.pad_sound_mapping:
            sound_path = self.pad_sound_mapping[pad_index]
            print(f"Playing sound: {sound_path}")
            self.play_sound(sound_path)

    def play_sound(self, file_path):
        try:
            data, samplerate = sf.read(file_path, dtype='float32')
            sd.play(data, samplerate)
        except Exception as e:
            print(f"Failed to play sound: {e}")


def add_midi_pads(layout):
    midi_pads = MidiPads(layout)
    return midi_pads
