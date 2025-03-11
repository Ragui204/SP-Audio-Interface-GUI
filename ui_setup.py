from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton
)
from PyQt5.QtCore import Qt
from NavegationBar import NavigationBar
from Pads import add_midi_pads
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
        self.showFullScreen()
        self.setStyleSheet("background-color: #1E1E1E; color: white;")

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.navbar = NavigationBar(self.switch_tab)
        self.stacked_widget = QStackedWidget()

        self.tabs = [
            self.create_midi_tab(0),  # Tab 0 - MIDI1
            self.create_midi_tab(1),  # Tab 1 - MIDI2
            self.create_guitar1_tab(),  # Tab 2 - Guitar1
            self.create_guitar2_tab()   # Tab 3 - Guitar2
        ]

        for tab in self.tabs:
            self.stacked_widget.addWidget(tab)

        main_layout.addLayout(self.navbar.navbar)
        main_layout.addWidget(self.stacked_widget)

        self.setCentralWidget(central_widget)
        self.switch_tab(0)

    def switch_tab(self, index):
        self.navbar.switch_tab(index)
        self.stacked_widget.setCurrentIndex(index)

    def create_midi_tab(self, tab_index):
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        # Create pads and store reference in the dictionary per tab index
        midi_pads = add_midi_pads(left_panel)
        self.midi_pads_by_tab[tab_index] = midi_pads

        add_equalizer_controls(left_panel)
        Delay_Reverb_Controls(right_panel)
        add_volume_controls(right_panel)

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page

    def create_guitar1_tab(self):
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        add_equalizer_controls(left_panel)
        Delay_Reverb_Controls(right_panel)
        add_volume_controls(right_panel)

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page

    def create_guitar2_tab(self):
        return self.create_guitar1_tab()

    def keyPressEvent(self, event):
        current_index = self.stacked_widget.currentIndex()
        if current_index in self.midi_pads_by_tab:
            midi_pads = self.midi_pads_by_tab[current_index]
            midi_pads.handle_key_event(event)
        super().keyPressEvent(event)  # Pass the event to the base class



