import sys
from PyQt6.QtWidgets import QApplication
import name_window
import welcome_window


app = QApplication(sys.argv)
window = welcome_window.WelcomeWindow()
window.showMaximized()
window.show()

try:
    app.exec()
except KeyboardInterrupt:
    print("shuting down...")
