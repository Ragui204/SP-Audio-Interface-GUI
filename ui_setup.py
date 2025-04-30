from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from NavegationBar import NavigationBar
from Pads import MidiPads
from DelayReverb import Delay_Reverb_Controls
from Volume import add_volume_controls
from waveform import add_waveform_selector
from GuitarControls import create_guitar_tab
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.midi_pads_by_tab = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Interface")
        self.showFullScreen()
        self.setStyleSheet("background-color: #1E1E1E; color: white; font-size: 22px;")

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.navbar = NavigationBar(self.switch_tab)
        self.stacked_widget = QStackedWidget()

        self.tabs = [
            self.create_midi_tab(0x100),  # MIDI1 -> Teensy 1
            self.create_midi_tab(0x200),  # MIDI2 -> Teensy 2
            self.create_guitar1_tab(),    # Guitar1
            self.create_guitar2_tab()     # Guitar2
        ]

        for tab in self.tabs:
            self.stacked_widget.addWidget(tab)

        main_layout.addLayout(self.navbar.navbar)
        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)
        self.switch_tab(0)

    def switch_tab(self, index):
        """Switches between MIDI and Guitar tabs."""
        self.navbar.switch_tab(index)
        self.stacked_widget.setCurrentIndex(index)

    def create_midi_tab(self, teensy_id):
        """Creates a MIDI tab for a specific Teensy ID."""
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        midi_pads = self.add_midi_pads(left_panel, teensy_id)
        self.midi_pads_by_tab[teensy_id] = midi_pads  

        Delay_Reverb_Controls(right_panel, teensy_id)
        add_volume_controls(right_panel, teensy_id)
        add_waveform_selector(left_panel, teensy_id)

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page

    def add_midi_pads(self, layout, teensy_id):
        midi_pads = MidiPads(teensy_id=teensy_id)
        layout.addWidget(midi_pads)
        return midi_pads

    def create_guitar1_tab(self):
        """Creates Guitar1 tab with CAN ID 0x300."""
        return create_guitar_tab(0x300)

    def create_guitar2_tab(self):
        return create_guitar_tab(0x400)

    def keyPressEvent(self, event):
        """Handles key presses for MIDI pads."""
        current_index = self.stacked_widget.currentIndex()
        if current_index in self.midi_pads_by_tab:
            midi_pads = self.midi_pads_by_tab[current_index]
            midi_pads.handle_key_event(event)
        super().keyPressEvent(event)

    def closeEvent(self, event):
        """Shutdown CAN bus when GUI is closed."""
        try:
            subprocess.run("sudo ip link set can0 down", shell=True)
            print("🛑 CAN bus shut down.")
        except Exception as e:
            print(f"⚠️ Failed to shut down CAN bus: {e}")
        super().closeEvent(event)
