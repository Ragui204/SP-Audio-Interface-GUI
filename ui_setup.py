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
from CanInit import Can_INIT  # ✅ Import CAN initialization
from can_listener import start_can_listener

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bus = Can_INIT()  # ✅ Initialize CAN Bus
        if self.bus:
            start_can_listener(self.bus)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Interface")
        self.showFullScreen()
        self.setStyleSheet("background-color: #1E1E1E; color: white;")

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.navbar = NavigationBar(self.switch_tab)
        self.stacked_widget = QStackedWidget()

        # ✅ Define CAN addresses without changing original features
        self.can_addresses = {
            "MIDI1": 0x100,
            "MIDI2": 0x120,
        }

        # ✅ Keep existing tab layouts
        self.tabs = [
            self.create_midi_tab("MIDI1"),
            self.create_midi_tab("MIDI2"),
            self.create_guitar1_tab(),
            self.create_guitar2_tab()
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

    def create_midi_tab(self, tab_name):
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        add_midi_pads(left_panel)
        add_equalizer_controls(left_panel)  # ✅ Pass CAN bus and address
        Delay_Reverb_Controls(right_panel, self.bus, self.can_addresses[tab_name])
        add_volume_controls(right_panel, self.bus, self.can_addresses[tab_name])

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
        Delay_Reverb_Controls(right_panel, self.bus, self.can_addresses[tab_name])
        add_volume_controls(right_panel, self.bus, None)  # 🎸 No CAN needed

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page

    def create_guitar2_tab(self):
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        add_equalizer_controls(left_panel)
        Delay_Reverb_Controls(right_panel, self.bus, self.can_addresses[tab_name])
        add_volume_controls(right_panel, self.bus, None)  # 🎸 No CAN needed

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page
