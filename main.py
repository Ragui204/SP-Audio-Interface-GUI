from PyQt5.QtWidgets import QApplication
from ui_setup import MainWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()  # Force full-screen mode
    sys.exit(app.exec_())
