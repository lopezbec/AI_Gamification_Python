import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from concent import ConcentWindow
import os
import sys


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()

        # Obtiene la ruta del directorio donde se encuentra el script actual
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al archivo JSON usando os.path.join
        json_path = os.path.join(current_script_path, 'json', 'welcome_info.json')

        with open(json_path, 'r', encoding='UTF-8') as welcome_data:
            data = json.load(welcome_data)

        #window title
        self.setWindowTitle(data["window_title"])
        
        #title
        title = QLabel(self)
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setPointSize(data["title_font_size"])
        title.setFont(font_title)
        title.setWordWrap(data["content_word_wrap"])
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        title.setMargin(data["title_margin"])

        content = QLabel(self)
        
        content.setText(data["content_text"])

        font_content = QFont()
        font_content.setPointSize(data["content_font_size"])

        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(data["content_word_wrap"])
        content.setAlignment(Qt.AlignmentFlag.AlignTop |  Qt.AlignmentFlag.AlignJustify)
        content.setMargin(data["title_margin"])

        next_button = QPushButton(self)
        next_button.setText(data["button_text"])
        next_button.setStyleSheet(f"background-color: {data['continue_button_color']};color: white;font-size:{data['font_size_buttons']}px")
        next_button.clicked.connect(self.show_concent)


        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        v_layout.addWidget(title)

        h_layout.addWidget(content)
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(-1,-1,-1,-1)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(next_button)
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(-1,-1,-1,-1)
        
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

    def show_concent(self):
        self.concent_window = ConcentWindow()
        self.concent_window.show()
        self.hide()

    def closeEvent(self, event):
        # Llamado cuando se intenta cerrar la ventana
        sys.exit()  # Termina el programa completamente

    def show_concent(self):
        self.concent_window = ConcentWindow()
        self.concent_window.show()
        self.hide()

