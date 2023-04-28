import json
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
sys.path.append("C:/Users/Admin/VSCode/AI_Gamification_Python")
from Elmer.Elmer_Pages_That_Mimic_SoloLearn import question_pedagogical_page


class FinishWindow(QMainWindow):
    def __init__(self) -> None:
        super(FinishWindow, self).__init__()

        title = QLabel()
        title.setText("Questionario finalizado" )
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
        finish_button.setText("Pasar a contenido")
        finish_button.clicked.connect(self.pass_to_content)
        finish_button.setFixedSize(250, 30)

        v_layout = QVBoxLayout()
        v_layout.addWidget(title)
        v_layout.addWidget(finish_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        widget = QWidget()
        widget.setLayout(v_layout)
        self.showMaximized()
        self.setCentralWidget(widget)

    def pass_to_content(self):
        with open(r"../Elmer/Elmer_Pages_That_Mimic_SoloLearn/data.json", "r") as file:
            self.data = json.load(file)
        self.pedagogical_page = question_pedagogical_page.MainPage(data=self.data)
        self.pedagogical_page.show()
        self.hide()
