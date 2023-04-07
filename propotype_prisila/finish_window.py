from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QMainWindow, QPushButton, QRadioButton, QVBoxLayout, QWidget

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

        next_button = QPushButton()
        next_button.setText("Finalizar")
        next_button.setFixedSize(250, 30)

        v_layout = QVBoxLayout()
        v_layout.addWidget(title)
        v_layout.addWidget(next_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        widget = QWidget()
        widget.setLayout(v_layout)
        self.showMaximized()
        self.setCentralWidget(widget)