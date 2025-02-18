from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QGridLayout, QSizePolicy, QSpacerItem, QWidgetItem, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
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
        # self.setGeometry(100, 100, 600, 400)  # Remove fixed geometry
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
        add_volume_controls(right_panel)  # Add volume and plugins
        add_chorus_controls(right_panel)
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
        add_volume_controls(right_panel)  # Add volume and plugins
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

    def resizeEvent(self, event):
        new_width = event.size().width()
        new_height = event.size().height()

        # Adjust font sizes
        self.adjust_font_sizes(new_width)

        # Adjust control sizes (example for pads)
        self.adjust_pad_sizes(new_width, new_height)

    def adjust_font_sizes(self, width):
        font_size = int(width * 0.02)  # Example: font size is 2% of the width
        font = self.navbar.font()
        font.setPointSize(font_size)
        self.navbar.setFont(font)

        # Adjust font sizes for other elements as needed

    def adjust_pad_sizes(self, width, height):
        # Get the layout for the pads (assuming it's accessible)
        pad_layout = self.stacked_widget.currentWidget().layout().itemAt(0).layout()

        # Calculate new size based on window dimensions
        new_size = int(min(width, height) * 0.08)  # Example

        for i in range(pad_layout.count()):
            item = pad_layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                widget = item.widget()
                if isinstance(widget, QPushButton):
                    widget.setFixedSize(new_size, new_size)