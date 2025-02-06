from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QStackedWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

class NavigationBar(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.initUI()

    def initUI(self):
        # Navigation Bar Layout
        self.navbar = QHBoxLayout()
        self.navbar.setSpacing(0)
        self.navbar.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = []
        tab_names = ["MIDI1", "MIDI2", "Guitar1", "Guitar2"]
        
        for i, name in enumerate(tab_names):
            btn = QPushButton(name)
            btn.setFont(QFont("Arial", 15))
            btn.setStyleSheet("QPushButton { border: 8px; padding: 10px 20px; }")
            btn.clicked.connect(lambda checked, index=i: self.switch_callback(index))
            self.tabs.append(btn)
            self.navbar.addWidget(btn)
        
    
    def switch_tab(self, index):
        for i, btn in enumerate(self.tabs):
            if i == index:
                btn.setStyleSheet("QPushButton { border: none; padding: 10px 20px; font-weight: bold; color: Green }")
            else:
                btn.setStyleSheet("QPushButton { border: none; padding: 10px 20px; font-weight: bold; }")
