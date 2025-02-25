from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QGridLayout, QSizePolicy, QSpacerItem, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from NavegationBar import NavigationBar
from Pads import add_midi_pads
from equalizer import add_equalizer_controls
from DelayReverb import Delay_Reverb_Controls
from Volume import add_volume_controls

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Interface")
        self.showFullScreen()  # Set full screen mode
        self.setStyleSheet("background-color: #1E1E1E; color: white;")

        # Main Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Navigation Bar
        self.navbar = NavigationBar(self.switch_tab)
        self.navbar.setStyleSheet("background-color: #2D2D2D;")

        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: red; color: white;")
        exit_button.clicked.connect(self.close_application)
        
        # Content Area Layout
        self.stacked_widget = QStackedWidget()

        # Define unique layouts for each tab
        tabs = {
            "MIDI1": self.create_midi1_tab(),
            "MIDI2": self.create_midi2_tab(),
            "Guitar1": self.create_guitar1_tab(),
            "Guitar2": self.create_guitar2_tab(),
        }

        for tab in tabs.values():
            self.stacked_widget.addWidget(tab)

        # Add widgets to layout
        main_layout.addLayout(self.navbar.navbar)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(exit_button)  # Add exit button at the bottom

        self.setCentralWidget(central_widget)
        self.switch_tab(0)  # Start on the first tab

    def switch_tab(self, index):
        self.navbar.switch_tab(index)
        self.stacked_widget.setCurrentIndex(index)
    
    def close_application(self):
        QApplication.quit()

    def create_midi1_tab(self):
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()
        
        add_midi_pads(left_panel)
        add_equalizer_controls(left_panel)
        Delay_Reverb_Controls(right_panel)  # Add volume and plugins
        add_volume_controls(right_panel)
        
        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page

    def create_midi2_tab(self):
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()
        
        add_midi_pads(left_panel)
        add_equalizer_controls(left_panel)
        Delay_Reverb_Controls(right_panel)  # Add volume and plugins
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
