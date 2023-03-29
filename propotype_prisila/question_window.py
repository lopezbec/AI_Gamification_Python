from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget

class QuestionWindow(QMainWindow):
    def __init__(self) -> None:
        super(QuestionWindow, self).__init__()
        
        #title
        title = QLabel(self)
        title.setText("Pregunta #1")
        title.adjustSize()
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(18)
        font_title.setFamily("Lato")
        title.setFont(font_title)
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        title.setMargin(10)

        content = QLabel(self)
        
        content.setText("Aqui va tu pregunta")

        font_content = QFont()
        font_content.setPointSize(12)
        font_content.setFamily("Lato")
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content.setMargin(10)

        next_button = QPushButton(self)
        next_button.setText("Siguiente")
        next_button.setFixedSize(250, 30)
        next_button.clicked.connect(self.save_content)


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
        self.showMaximized()
        self.setCentralWidget(widget)

    def save_content(self):
        print("clicked")