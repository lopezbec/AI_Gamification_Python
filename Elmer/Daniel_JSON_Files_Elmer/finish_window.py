import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget



class FinishWindow(QMainWindow):
    def __init__(self) -> None:
        super(FinishWindow, self).__init__()

        with open(r'./json/finish_info.json', "r", encoding='UTF-8') as finish_info:
            data = json.load(finish_info)

        self.setWindowTitle(data['window_title'])
        title = QLabel()
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setPointSize(data["title_font_size"])
        title.setFont(font_title)
        title.setWordWrap(data["title_word_wrap"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMargin(data["title_margin"])

        finish_button = QPushButton()
        finish_button.setText(data["finish_button_text"])
        finish_button.setStyleSheet(f"background-color: {data['continue_button_color']};color: white;font-size:{data['font_size_buttons']}px")
        finish_button.clicked.connect(self.close_window)

        v_layout = QVBoxLayout()
        v_layout.addWidget(title)
        v_layout.addWidget(finish_button)

        widget = QWidget()
        widget.setLayout(v_layout)
        self.showMaximized()
        self.setCentralWidget(widget)

    def close_window(self):
        with open("data.json", "r", encoding='UTF-8') as file:
            data = json.load(file)

        self.close()


