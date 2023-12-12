import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from question_window import QuestionWindow


class NameWindow(QMainWindow):
    def __init__(self) -> None:
        super(NameWindow, self).__init__()

        with open(r'./json/name_info.json', "r", encoding='UTF-8') as name_info:
            data = json.load(name_info)
        # Window properties
        self.setWindowTitle = data["window_title"]
        # Layouts
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        layout_V_Form = QVBoxLayout()
        layoutForm = QFormLayout()
        # Label properties
        ask_name = QLabel(self)
        ask_name.setText(data["ask_name_title"])
        font = QFont()
        ask_name.setFont(font)
        font.setPointSize(data["ask_name_font_size"])
        ask_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ask_name.setStyleSheet(f"font-size:{data['ask_name_font_size']}px")
        ask_name.setMargin(data["ask_name_margin"])
        # input properties
        self.input = QLineEdit(self)
        self.input.setContentsMargins(data["input_margin"]["left"], data["input_margin"]["top"],
                                      data["input_margin"]["right"], data["input_margin"]["bottom"])
        self.input.setMinimumWidth(data["input_minimum_width"])
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # button properties
        button = QPushButton(data["button_text"], self)
        button.clicked.connect(self.show_survey)
        button.setStyleSheet(f"background-color: {data['continue_button_color']};color: white;font-size:{data['font_size_buttons']}px")
        button.setMinimumWidth(data["button_minimun_width"])
        # Add widgets to Layouts
        # Horizontal Layout
        layoutH.addWidget(ask_name)
        # Form Layout
        layoutForm.addRow(layoutH)
        layout_V_Form.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_V_Form.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutForm.addRow(layout_V_Form)
        layoutForm.setContentsMargins(10, 10, 10, 10)

        # Vertical layout
        layoutV.setSpacing(10)
        layoutV.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layoutV.addLayout(layoutForm)
        # Widget/Container initialization
        widget = QWidget()
        widget.setLayout(layoutV)
        self.showMaximized()
        self.setCentralWidget(widget)

    def show_survey(self):
        self.question_window = QuestionWindow()
        self.question_window.username = self.input.text()
        self.question_window.read_csv()
        self.question_window.show()
        self.hide()
