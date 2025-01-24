from PyQt5.QtWidgets import QApplication
from ui_setup import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
