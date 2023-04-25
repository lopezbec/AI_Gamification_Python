from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCheckBox, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget
from name_window import NameWindow


class ConcentWindow(QMainWindow):
    def __init__(self) -> None:
        super(ConcentWindow, self).__init__()
        
        #title
        title = QLabel(self)
        title.setText("Terminos y condiciones")
        title.adjustSize()
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(18)
        font_title.setFamily("Lato")
        title.setFont(font_title)
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop )
        title.setMargin(5)

        content = QLabel(self)
        
        content.setText("Aqui ira un texto para dar concentimiento a los terminos y condiciones")

        font_content = QFont()
        font_content.setPointSize(12)
        font_content.setFamily("Lato")
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content.setMargin(10)

        self.accept_terms = QCheckBox("Aceptar terminos y condiciones")
        self.accept_terms.stateChanged.connect(self.user_concent)

        self.button = QPushButton("Acepto")
        self.button.setMaximumSize(250, 30);
        self.button.setEnabled(False)
        self.button.clicked.connect(self.agree_btn_is_clicked)
     
        v_layout = QVBoxLayout()

        v_layout.addWidget(title)
        v_layout.addWidget(content)
        v_layout.addWidget(self.accept_terms)
        v_layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)
        v_layout.setContentsMargins(5,10,5,10)
        
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.showMaximized()

    def user_concent(self):
        if  self.accept_terms.isChecked():
            self.button.setEnabled(True)
            
    def agree_btn_is_clicked(self):
        if self.button.isEnabled():
            self.name_window = NameWindow()
            self.name_window.show()
            self.hide()
