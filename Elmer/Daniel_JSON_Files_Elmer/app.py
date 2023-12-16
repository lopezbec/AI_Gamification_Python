import sys
from PyQt6.QtWidgets import QApplication


class Intro_Pages():
        """Método que ejecuta la ventana de PyQt."""
        app = QApplication(sys.argv)
        window = WelcomeWindow()
        window.showMaximized()
        window.show()


