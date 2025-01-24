from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QStackedWidget
from PyQt5.QtCore import Qt
from volume import add_volume_controls
from equalizer import add_equalizer_controls
from chorus import add_chorus_controls
from Pads import add_midi_pads
from NavegationBar import add_navigation_bar

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MIDI-Audio Controller")
        self.showFullScreen()

        # Main Layout
        self.layout = QVBoxLayout()

        # Add Navigation Bar
        add_navigation_bar(self.layout, self)

        # Create Stacked Widget for switching pages
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Initialize the 4 different GUI pages
        self.midi1_page = self.create_midi1_gui()
        self.midi2_page = self.create_midi2_gui()
        self.guitar1_page = self.create_guitar1_gui()
        self.guitar2_page = self.create_guitar2_gui()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.midi1_page)
        self.stacked_widget.addWidget(self.midi2_page)
        self.stacked_widget.addWidget(self.guitar1_page)
        self.stacked_widget.addWidget(self.guitar2_page)

        # Set default page
        self.stacked_widget.setCurrentWidget(self.midi1_page)

        self.setLayout(self.layout)

    def create_midi1_gui(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("MIDI1 Interface"))
        add_midi_pads(layout)
        add_volume_controls(layout)
        page.setLayout(layout)
        return page

    def create_midi2_gui(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("MIDI2 Interface"))
        add_volume_controls(layout)
        add_equalizer_controls(layout)
        page.setLayout(layout)
        return page

    def create_guitar1_gui(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Guitar1 Interface"))
        add_equalizer_controls(layout)
        add_chorus_controls(layout)
        page.setLayout(layout)
        return page

    def create_guitar2_gui(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Guitar2 Interface"))
        add_chorus_controls(layout)
        add_volume_controls(layout)
        page.setLayout(layout)
        return page

    # Navigation Functions
    def show_midi1(self):
        self.stacked_widget.setCurrentWidget(self.midi1_page)

    def show_midi2(self):
        self.stacked_widget.setCurrentWidget(self.midi2_page)

    def show_guitar1(self):
        self.stacked_widget.setCurrentWidget(self.guitar1_page)

    def show_guitar2(self):
        self.stacked_widget.setCurrentWidget(self.guitar2_page)

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
