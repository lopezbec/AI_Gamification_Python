import json
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from concent import ConcentWindow

class WelcomeWindow(QMainWindow):
    def __init__(self) -> None:
        super(WelcomeWindow, self).__init__()
        
        with open(r"./json/welcome_info.json", "r", encoding='utf-8') as welcome_data:
            data = json.load(welcome_data)
        
        #title
        title = QLabel(self)
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setBold(data["title_bold"])
        font_title.setPointSize(data["title_font_size"])
        font_title.setFamily(data["title_font_family"])
        title.setFont(font_title)
        title.setWordWrap(data["content_word_wrap"])
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        title.setMargin(data["title_margin"])

        content = QLabel(self)
        
        content.setText(data["content_text"])

        font_content = QFont()
        font_content.setPointSize(data["content_font_size"])
        font_content.setFamily(data["content_font_family"])
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(data["content_word_wrap"])
        content.setAlignment(Qt.AlignmentFlag.AlignTop |  Qt.AlignmentFlag.AlignJustify)
        content.setMargin(data["title_margin"])

        next_button = QPushButton(self)
        next_button.setText(data["button_text"])
        next_button.setFixedSize(data["button_width"], data["button_height"])
        next_button.clicked.connect(self.show_concent)


        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        v_layout.addWidget(title)

        h_layout.addWidget(content)
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(-1,-1,-1,-1)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(next_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(-1,-1,-1,-1)
        
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

    def show_concent(self):
        self.concent_window = ConcentWindow()
        self.concent_window.show()
        self.hide()
