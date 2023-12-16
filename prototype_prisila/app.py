import sys
from PyQt6.QtWidgets import QApplication
from welcome_window import WelcomeWindow


class Intro_Pages(): #Clase para llamarla y ejecutar esto desde otro codigo.
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.showMaximized()
    window.show()

    try:
        app.exec()
    except KeyboardInterrupt:
        print("shuting down...")
