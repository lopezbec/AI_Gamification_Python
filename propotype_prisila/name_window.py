from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from question_window import QuestionWindow

class NameWindow(QMainWindow):
    def __init__(self) -> None:
        super(NameWindow, self).__init__()

        #Window properties
        self.setWindowTitle = "Bienvenido"
        #Layouts
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        layout_V_Form = QVBoxLayout()
        layoutForm = QFormLayout()
        #Label properties
        ask_name = QLabel(self)
        ask_name.setText("¿Cual es tu nombre? ")
        font = QFont()
        font.setFamily("Lato")
        ask_name.setFont(font)
        font.setPointSize(14)
        ask_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ask_name.setMargin(40)
        #input properties
        self.input = QLineEdit(self)
        self.input.setContentsMargins(0,20,0, 20)
        self.input.setMinimumWidth(300)
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #button properties
        button = QPushButton("Siguiente", self)
        button.clicked.connect(self.show_survey)
        button.setMinimumWidth(300)
        #Add widgets to Layouts
            #Horizontal Layout
        layoutH.addWidget(ask_name)
        #Form Layout
        layoutForm.addRow(layoutH)
        layout_V_Form.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_V_Form.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutForm.addRow(layout_V_Form)
        layoutForm.setContentsMargins(10, 10, 10, 10)
        
        #Vertical layout
        layoutV.setSpacing(10)
        layoutV.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layoutV.addLayout(layoutForm)
        #Widget/Container initialization
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
