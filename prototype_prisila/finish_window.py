import json
import sys
# sys.path.append(r"C:/Users/Admin/VSCode/AI_Gamification_Python")
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
# from Elmer.Elmer_Pages_That_Mimic_SoloLearn import question_pedagogical_page
from pages import MainPage


class FinishWindow(QMainWindow):
    def __init__(self) -> None:
        super(FinishWindow, self).__init__()

        with open(r'./json/finish_info.json', "r") as finish_info:
            data = json.load(finish_info)

        title = QLabel()
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setBold(data["title_bold"])
        font_title.setPointSize(data["title_font_size"])
        font_title.setFamily(data["title_font_family"])
        title.setFont(font_title)
        title.setWordWrap(data["title_word_wrap"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMargin(data["title_margin"])

        finish_button = QPushButton()
        finish_button.setText(data["finish_button_text"])
        finish_button.clicked.connect(self.close_window)
        finish_button.setFixedSize(data["finish_button_width"], data["finish_button_height"])

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
