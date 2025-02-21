from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QGridLayout, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from NavegationBar import NavigationBar
from Pads import add_midi_pads
from equalizer import add_equalizer_controls
from DelayReverb import Delay_Reverb_Controls
from Volume import add_volume_controls

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Interface")
        #self.setGeometry(100, 100, 800, 480)  # Initial size, will resize
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
            "Guitar2": self.create_guitar2_tab(),
        }

        for tab in tabs.values():
            self.stacked_widget.addWidget(tab)

        # Add widgets to layout
        main_layout.addLayout(self.navbar.navbar)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

        self.switch_tab(0)  # Start on the first tab

    def switch_tab(self, index):
        self.navbar.switch_tab(index)
        self.stacked_widget.setCurrentIndex(index)

    def create_midi1_tab(self):
        page = QWidget()
        main_layout = QGridLayout()  # Use grid layout for better control

        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        add_midi_pads(left_panel)
        Delay_Reverb_Controls(right_panel)  # Add volume and plugins
        add_volume_controls(right_panel)
        add_equalizer_controls(left_panel)  # Equalizer at the bottom left

        # Add spacer to push EQ to bottom
        left_panel.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Add layouts to main grid layout
        main_layout.addLayout(left_panel, 0, 0, 2, 1)  # Span 2 rows
        main_layout.addLayout(right_panel, 0, 1, 2, 1)  # Span 2 rows

        page.setLayout(main_layout)
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

    def resizeEvent(self, event):
        # Get the new size of the widget
        new_width = event.size().width()
        new_height = event.size().height()

        # Adjust font sizes and element sizes based on new_width and new_height
        #... (implementation depends on your specific requirements)

        # Example: Adjust font size of navigation bar
        font = self.navbar.font()
        font.setPointSize(int(new_width * 0.015))  # Example: font size is 2% of the width
        self.navbar.setFont(font)