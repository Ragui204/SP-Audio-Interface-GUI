from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from NavegationBar import NavigationBar
from Pads import add_midi_pads
from equalizer import add_equalizer_controls
from volume import add_volume_controls
from chorus import add_chorus_controls

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Interface")
        self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(3240, 2160)
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        
        # Main Layout
        main_layout = QVBoxLayout()
        
        # Navigation Bar
        self.navbar = NavigationBar(self.switch_tab)
        self.navbar.setStyleSheet("background-color: #2D2D2D;")
        
        # Content Area Layout
        self.stacked_widget = QStackedWidget()
        
        # Define unique layouts for each tab
        tabs = {
            "MIDI1": self.create_midi1_tab(),
            "MIDI2": self.create_midi2_tab(),
            "Guitar1": self.create_guitar1_tab(),
            "Guitar2": self.create_guitar2_tab()
        }
        
        for tab in tabs.values():
            self.stacked_widget.addWidget(tab)
        
        # Add widgets to layout
        main_layout.addLayout(self.navbar.navbar)
        main_layout.addWidget(self.stacked_widget)
        
        self.setLayout(main_layout)
        
        self.switch_tab(0)
    
    def switch_tab(self, index):
        self.navbar.switch_tab(index)
        self.stacked_widget.setCurrentIndex(index)
    
    def create_midi1_tab(self):
        page = QWidget()
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()
        
        add_midi_pads(left_panel)
        add_equalizer_controls(left_panel)
        add_volume_controls(right_panel)
        add_chorus_controls(right_panel)
        
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
        add_volume_controls(right_panel)
        add_chorus_controls(right_panel)
        
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
        add_volume_controls(right_panel)
        add_chorus_controls(right_panel)
        
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
        add_volume_controls(right_panel)
        add_chorus_controls(right_panel)
        
        layout.addLayout(left_panel)
        layout.addLayout(right_panel)
        page.setLayout(layout)
        return page
