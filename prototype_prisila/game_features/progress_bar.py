import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton
from PyQt6.QtCore import Qt, QBasicTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Barra de Progreso")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 50, 250, 15)

        self.start_button = QPushButton("Iniciar", self)
        self.start_button.setGeometry(50, 100, 75, 30)
        self.start_button.clicked.connect(self.startProgress)

        self.reset_button = QPushButton("Reiniciar", self)
        self.reset_button.setGeometry(175, 100, 75, 30)
        self.reset_button.clicked.connect(self.resetProgress)

        self.timer = QBasicTimer()
        self.progress = 0
        self.step = 0

        self.setGeometry(300, 300, 300, 200)

    def timerEvent(self, event):
        if self.step >= 11:
            self.progress_bar.setValue(100)
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.start_button.setText("Reiniciar")
            return

        self.progress += 9
        self.progress_bar.setValue(self.progress)
        self.step += 1

    def startProgress(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("Continuar")
        else:
            self.progress = 0
            self.step = 0
            self.timer.start(100, self)
            self.start_button.setEnabled(False)

    def resetProgress(self):
        self.progress = 0
        self.step = 0
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(True)
        self.start_button.setText("Iniciar")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
