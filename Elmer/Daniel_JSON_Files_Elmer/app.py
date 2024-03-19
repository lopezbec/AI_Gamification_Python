import sys
from PyQt6.QtWidgets import QApplication
from welcome_window import WelcomeWindow

class Intro_Pages():
        """Método que ejecuta la ventana de PyQt."""
        app = QApplication(sys.argv)
        window = WelcomeWindow()
        window.showMaximized()

