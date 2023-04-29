from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import json
from pages import MainPage


class FinishWindow(QMainWindow):
    def __init__(self) -> None:
        super(FinishWindow, self).__init__()

        title = QLabel()
        title.setText("Questionario finalizado, estas listo para aprender?" )
        title.adjustSize()
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(18)
        font_title.setFamily("Lato")
        title.setFont(font_title)
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMargin(10)

        finish_button = QPushButton()
        finish_button.setText("Iniciar aprendizaje")
        finish_button.clicked.connect(self.close_window)
        finish_button.setFixedSize(250, 30)

        v_layout = QVBoxLayout()
        v_layout.addWidget(title)
        v_layout.addWidget(finish_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        widget = QWidget()
        widget.setLayout(v_layout)
        self.showMaximized()
        self.setCentralWidget(widget)

    def close_window(self):
        with open("data.json", "r") as file:
            data = json.load(file) 
            
        self.main_page = MainPage(data)
        self.main_page.show()
        self.hide()
