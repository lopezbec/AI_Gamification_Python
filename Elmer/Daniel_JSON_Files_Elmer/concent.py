import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCheckBox, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget
from name_window import NameWindow


class ConcentWindow(QMainWindow):
    def __init__(self) -> None:
        super(ConcentWindow, self).__init__()

        # Obtiene la ruta del directorio donde se encuentra el script actual
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al archivo JSON usando os.path.join
        json_path = os.path.join(current_script_path, 'json', 'concent_info.json')
        with open(json_path, "r", encoding='UTF-8') as f:
            data = json.load(f)
        
        # Título de la ventana
        self.setWindowTitle(data["window_title"])

        # Título
        title = QLabel(self)
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setPointSize(data["title_font_size"])
        title.setFont(font_title)
        title.setWordWrap(data["title_word_wrap"])
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        title.setMargin(data["title_margin"])

        # Contenido
        content = QLabel(self)
        content.setText(data["content_text"])
        font_content = QFont()
        font_content.setPointSize(data["content_font_size"])
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(data["content_word_wrap"])
        content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content.setMargin(data["content_margin"])

        # Checkbox para aceptar términos
        self.accept_terms = QCheckBox(data["accept_checkbox_text"])
        self.accept_terms.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.accept_terms.stateChanged.connect(self.user_concent)

        # Botón de aceptar
        self.accept_button = QPushButton(data["button_text"])
        self.accept_button.setEnabled(False)
        self.accept_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {data['continue_button_color']};
                color: white;
                font-size:{data['font_size_buttons']}px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }}
            QPushButton:disabled {{
                background-color: #A5D6A7;
            }}
            QPushButton:hover {{
                background-color: #45A049;
            }}
        """)
        self.accept_button.clicked.connect(self.proceed_to_next_window)

        # Layout principal
        v_layout = QVBoxLayout()
        v_layout.addWidget(title)
        v_layout.addWidget(content)
        v_layout.addWidget(self.accept_terms)
        v_layout.addWidget(self.accept_button)
        v_layout.setContentsMargins(5, 10, 5, 10)

        # ScrollArea para manejar contenido extenso
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(v_layout)
        scroll_area.setWidget(container)

        self.setCentralWidget(scroll_area)
        self.showMaximized()

    def user_concent(self):
        # Habilitar o deshabilitar el botón de aceptar según el estado del checkbox
        self.accept_button.setEnabled(self.accept_terms.isChecked())

    def proceed_to_next_window(self):
        # Proceder a la siguiente ventana
        if self.accept_terms.isChecked():
            self.name_window = NameWindow()
            self.name_window.show()
            self.hide()

    def closeEvent(self, event):
        # Método sobrescrito llamado al intentar cerrar la ventana con la "X"
        sys.exit()  # Termina el programa
