from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget
from concent import ConcentWindow


class WelcomeWindow(QMainWindow):
    def __init__(self) -> None:
        super(WelcomeWindow, self).__init__()
        
        #title
        title = QLabel(self)
        title.setText("Aprendizaje automático y gamificación para una aplicación educativa personalizada y adaptativa")
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
        
        content.setText(
            "Este proyecto cuenta con el apoyo de la beca FONDOCyT (2022-3A1-112), y cuenta con la colaboración de " +
            "la Universidad Nacional Pedro Henríquez Ureña (UNPHU) y la Asociación para la Creatividad," + 
            "Innovación, Emprendimiento y Networking (A100%) de República Dominicana.\n\n"
            
            "El proyecto tiene como objetivo explorar la implementación de algoritmos de Machine Learning en una aplicación educativa" +
            "gamificada para personalizar sus elementos de juego y adaptar su contenido pedagógico. La aplicación se" +
            "centrará en ayudar a sus usuarios a aprender a programar usando Python, ya que los desarrolladores " +
            "de software de Python se encuentran entre las profesiones emergentes más demandadas."
        )

        font_content = QFont()
        font_content.setPointSize(12)
        font_content.setFamily("Lato")
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignJustify)
        content.setMargin(10)

        next_button = QPushButton(self)
        next_button.setText("Siguiente")
        next_button.setFixedSize(250, 30)
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
