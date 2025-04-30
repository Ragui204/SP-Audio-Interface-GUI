import sys
import can
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal


class CANReceiver(QThread):
    note_received = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
        self.running = True

    def run(self):
        while self.running:
            msg = self.bus.recv(timeout=0.05)
            if msg and msg.arbitration_id == 0x100 and msg.dlc >= 1:
                note = msg.data[0]
                self.note_received.emit(note)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class DrumMapper(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drum Pad Mapper")
        self.setFixedSize(320, 350)

        self.current_note = None
        self.mapping = {
            "Kick": None,
            "Snare": None,
            "Hi-Hat": None,
            "Clap": None
        }

        self.note_label = QLabel("Last Note: None")
        self.note_label.setStyleSheet("font-size: 18px;")
        self.mapping_labels = {
            drum: QLabel(f"{drum}: None") for drum in self.mapping
        }

        self.kick_btn = QPushButton("Assign to Kick")
        self.snare_btn = QPushButton("Assign to Snare")
        self.hat_btn = QPushButton("Assign to Hi-Hat")
        self.clap_btn = QPushButton("Assign to Clap")
        self.send_btn = QPushButton("Send Mapping to Teensy")

        self.kick_btn.clicked.connect(lambda: self.assign("Kick"))
        self.snare_btn.clicked.connect(lambda: self.assign("Snare"))
        self.hat_btn.clicked.connect(lambda: self.assign("Hi-Hat"))
        self.clap_btn.clicked.connect(lambda: self.assign("Clap"))
        self.send_btn.clicked.connect(self.send_mapping)

        layout = QVBoxLayout()
        layout.addWidget(self.note_label)
        for lbl in self.mapping_labels.values():
            layout.addWidget(lbl)

        for btn in [self.kick_btn, self.snare_btn, self.hat_btn, self.clap_btn, self.send_btn]:
            layout.addWidget(btn)

        self.setLayout(layout)

        self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
        self.receiver = CANReceiver()
        self.receiver.note_received.connect(self.update_note)
        self.receiver.start()

    def update_note(self, note):
        self.current_note = note
        self.note_label.setText(f"Last Note: {note}")

    def assign(self, drum):
        if self.current_note is not None:
            self.mapping[drum] = self.current_note
            self.mapping_labels[drum].setText(f"{drum}: {self.current_note}")

    def send_mapping(self):
        try:
            msg = can.Message(
                arbitration_id=0x101,
                data=[
                    self.mapping["Kick"] or 0,
                    self.mapping["Snare"] or 0,
                    self.mapping["Hi-Hat"] or 0,
                    self.mapping["Clap"] or 0
                ],
                is_extended_id=False
            )
            self.bus.send(msg)
            QMessageBox.information(self, "Sent!", "Mapping sent to Teensy ✅")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send mapping:\n{e}")

    def closeEvent(self, event):
        self.receiver.stop()
        event.accept()

  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrumMapper()
    window.show()
    sys.exit(app.exec_())
