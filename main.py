from PyQt5.QtWidgets import QApplication
from ui_setup import MainWindow
import subprocess
import time

def is_can_up():
    """Check if CAN interface is already up."""
    try:
        result = subprocess.run("ip link show can0", shell=True, check=True, capture_output=True, text=True)
        return "state UP" in result.stdout
    except subprocess.CalledProcessError:
        return False

# === Enable CAN Bus at startup only if not already up ===
if not is_can_up():
    try:
        subprocess.run("sudo ip link set can0 type can bitrate 500000", shell=True, check=True)
        subprocess.run("sudo ip link set can0 up", shell=True, check=True)
        print("✅ CAN bus enabled.")
        time.sleep(0.5)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to enable CAN bus: {e}")
else:
    print("ℹ️ CAN bus already active. Skipping setup.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
