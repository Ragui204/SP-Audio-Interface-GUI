from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from NavegationBar import NavigationBar
from Pads import MidiPads
from equalizer import add_equalizer_controls
from DelayReverb import Delay_Reverb_Controls
from Volume import add_volume_controls

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.midi_pads_by_tab = {}  # Dictionary to store pads per tab
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Interface")
        self.showFullScreen()  # Ensures full touchscreen display
        self.setStyleSheet("background-color: #1E1E1E; color: white; font-size: 22px;")  

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.navbar = NavigationBar(self.switch_tab)
        self.stacked_widget = QStackedWidget()

        # Adding all tabs (MIDI1, MIDI2, Guitar1, Guitar2)
        self.tabs = [
            self.create_midi_tab(1),  # MIDI1 -> Teensy 1
            self.create_midi_tab(2),  # MIDI2 -> Teensy 2
            self.create_guitar1_tab(),  # Guitar1
            self.create_guitar2_tab()   # Guitar2
        ]

        for tab in self.tabs:
            self.stacked_widget.addWidget(tab)

        main_layout.addLayout(self.navbar.navbar)
        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)
        self.switch_tab(0)  # Default to first tab (MIDI1)

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

        # MIDI Pads (Interactive Buttons)
        midi_pads = self.add_midi_pads(left_panel)
        self.midi_pads_by_tab[teensy_id] = midi_pads  

        # Equalizer
        add_equalizer_controls(left_panel)

        # Delay & Reverb (CAN Integrated)
        Delay_Reverb_Controls(right_panel, teensy_id)

        # Volume Control (CAN Integrated)
        add_volume_controls(right_panel, teensy_id)

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page

    def add_midi_pads(self, layout):
        """Creates MIDI pad buttons dynamically."""
        midi_pads = MidiPads()
        layout.addWidget(midi_pads)
        return midi_pads

    def create_guitar1_tab(self):
        """Creates Guitar1 tab (No CAN)."""
        return self.create_midi_tab(2)

    def create_guitar2_tab(self):
        """Creates Guitar2 tab (No CAN)."""
        return self.create_midi_tab(3)

    def keyPressEvent(self, event):
        """Handles key presses for MIDI pads."""
        current_index = self.stacked_widget.currentIndex()
        if current_index in self.midi_pads_by_tab:
            midi_pads = self.midi_pads_by_tab[current_index]
            midi_pads.handle_key_event(event)
        super().keyPressEvent(event)
