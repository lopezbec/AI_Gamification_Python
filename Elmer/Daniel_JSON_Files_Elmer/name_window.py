import json
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from config import Config
from question_window import QuestionWindow
from Codigos_LeaderBoard import Main_Leaderboard_FV


class NameWindow(QMainWindow):
    nameEntered = pyqtSignal(str) 
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

    def user_exists(self, username):
        try:
            with open('usernames.json', 'r', encoding='UTF-8') as file:
                usernames = json.load(file)
            return username in usernames
        except FileNotFoundError:
            return False

    def add_username(self, username):
        try:
            with open('usernames.json', 'r', encoding='UTF-8') as file:
                usernames = json.load(file)
        except FileNotFoundError:
            usernames = []

        if username not in usernames:
            usernames.append(username)
            with open('usernames.json', 'w', encoding='UTF-8') as file:
                json.dump(usernames, file)

    def show_survey(self):
        username = self.input.text()
        if not self.user_exists(username):
            # Usuario nuevo: añadir el nombre y proceder a la siguiente ventana
            self.add_username(username)
            Config.set_user_name(username)
            self.question_window = QuestionWindow()
            self.question_window.username = username
            self.question_window.read_csv()
            self.question_window.show()
            self.hide()
        else:
            Config.set_user_name(username)
            # Usuario existente: cerrar la ventana
            self.close()
