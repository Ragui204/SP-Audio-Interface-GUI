from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QStackedWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import subprocess

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
            btn.setStyleSheet("QPushButton { border: none; padding: 10px 20px; font-weight: bold; }")
            btn.clicked.connect(lambda checked, index=i: self.switch_callback(index))
            self.tabs.append(btn)
            self.navbar.addWidget(btn)

        # === ADD SMALL SHUTDOWN BUTTON HERE ===
        shutdown_btn = QPushButton("⏻")
        shutdown_btn.setFixedSize(30, 30)
        shutdown_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        shutdown_btn.clicked.connect(lambda: self.window().close())
        self.navbar.addWidget(shutdown_btn)

        
    def switch_tab(self, index):
        for i, btn in enumerate(self.tabs):
            if i == index:
                btn.setStyleSheet("QPushButton { border: none; padding: 10px 20px; font-weight: bold; color: Green }")
            else:
                btn.setStyleSheet("QPushButton { border: none; padding: 10px 20px; font-weight: bold; }")

    def shutdown_system(self):
        try:
            print("🛑 Shutting down CAN and Raspberry Pi...")
            subprocess.run("sudo ip link set can0 down", shell=True)
            subprocess.run("sudo shutdown now", shell=True)
        except Exception as e:
            print(f"⚠️ Shutdown failed: {e}")
