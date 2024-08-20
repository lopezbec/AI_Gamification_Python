import json
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCheckBox, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget
from name_window import NameWindow
import sys


class ConcentWindow(QMainWindow):
    def __init__(self) -> None:
        super(ConcentWindow, self).__init__()

        # Obtiene la ruta del directorio donde se encuentra el script actual
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al archivo JSON usando os.path.join
        json_path = os.path.join(current_script_path, 'json', 'concent_info.json')
        with open(json_path, "r", encoding='UTF-8') as f:
            data = json.load(f)
        
        #window title
        self.setWindowTitle(data["window_title"])
        #title
        title = QLabel(self)
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setPointSize(data["title_font_size"])
        title.setFont(font_title)
        title.setWordWrap(data["title_word_wrap"])
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop )
        title.setMargin(data["title_margin"])

        content = QLabel(self)
        
        content.setText(data["content_text"])

        font_content = QFont()
        font_content.setPointSize(data["content_font_size"])
        #font_content.setFamily(data["content_font_family"])
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(data["content_word_wrap"])
        content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content.setMargin(data["content_margin"])

        self.accept_terms = QCheckBox(data["accept_checkbox_text"])
        self.accept_terms.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.accept_terms.stateChanged.connect(self.user_concent)

        #self.button = QPushButton(data["button_text"])
        #self.button.setEnabled(data["button_enabled"])
        #self.button.setStyleSheet(f"background-color: {data['continue_button_color']};color: white;font-size:{data['font_size_buttons']}px")
        #self.button.clicked.connect(self.agree_btn_is_clicked)
     
        v_layout = QVBoxLayout()

        v_layout.addWidget(title)
        v_layout.addWidget(content)
        v_layout.addWidget(self.accept_terms)
        #v_layout.addWidget(self.button)
        v_layout.setContentsMargins(5,10,5,10)
        
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.showMaximized()

    def user_concent(self):
        # Tu lógica existente para manejar el estado del checkbox y el botón
        if self.accept_terms.isChecked():
            self.name_window = NameWindow()
            self.name_window.show()
            self.hide()
            #self.button.setEnabled(True)
        #else:
            #self.button.setEnabled(False)

    #def agree_btn_is_clicked(self):
        # Tu lógica existente para manejar el click en el botón
        #if self.button.isEnabled():
            #self.name_window = NameWindow()
            #self.name_window.show()
            #self.hide()

    def closeEvent(self, event):
        # Método sobrescrito llamado al intentar cerrar la ventana
        sys.exit()  # Termina el programa
            
    #def agree_btn_is_clicked(self):
        #if self.button.isEnabled():
            #self.name_window = NameWindow()
            #self.name_window.show()
            #self.hide()
