import json
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from config import Config
from question_window import QuestionWindow
from Codigos_LeaderBoard import Main_Leaderboard_FV


class NameWindow(QMainWindow):
    nameEntered = pyqtSignal(str)
    progressNeedsReload = pyqtSignal()
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
        # Verificar y actualizar usernames.json
        try:
            try:
                current_user = {"current_user": username}
                print(current_user)
                with open('current_user.json', 'w', encoding='UTF-8') as file:
                    json.dump(current_user, file)
            except Exception as e:
                print(f"Error al actualizar current_user.json: {e}")

            with open('usernames.json', 'r', encoding='UTF-8') as file:
                usernames = json.load(file)
        except FileNotFoundError:
            usernames = []

        if username not in usernames:
            usernames.append(username)
            with open('usernames.json', 'w', encoding='UTF-8') as file:
                json.dump(usernames, file)

        # Verificar y actualizar progreso.json
        progreso_inicial = {
            "Modulo1": {"Leccion1": True, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False},
            "Modulo2": {"Leccion1": False, "Leccion2": False, "Leccion3": False},
            "Modulo3": {"Leccion1": False, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False},
            "Modulo4": {"Leccion1": False, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False},
            "Modulo5": {"Leccion1": False, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False,
                        "Leccion6": False, "Leccion7": False}
        }

        try:
            with open('progreso.json', 'r', encoding='UTF-8') as file:
                progreso = json.load(file)
        except FileNotFoundError:
            progreso = {}

        if username not in progreso:
            progreso[username] = progreso_inicial
            with open('progreso.json', 'w', encoding='UTF-8') as file:
                json.dump(progreso, file, indent=4)

        self.progressNeedsReload.emit()

        # Llamada para actualizar la interfaz o cualquier otra lógica necesaria después de agregar el usuario

    def show_survey(self):
        username = self.input.text()
        self.update_current_user(username)  # Actualizar current_user.json con el usuario actual

        if not self.user_exists(username):
            # Usuario nuevo: añadir el nombre y proceder a la siguiente ventana
            self.add_username(username)
            self.question_window = QuestionWindow()
            self.question_window.username = username
            self.question_window.read_csv()
            self.question_window.show()
        else:
            # Usuario existente: solo cierra la ventana ya que el usuario ya fue agregado
            self.close()

    def recargar_progreso_usuario(self):
        try:
            # Cargar el progreso del usuario actualizado desde el archivo
            with open('progreso.json', 'r', encoding='UTF-8') as file:
                progreso = json.load(file)
            self.progreso_usuario = progreso.get(self.usuario_actual, {})

            # Actualizar el estado de las lecciones en la interfaz de usuario
            self.actualizar_lecciones(self.progreso_usuario)
        except Exception as e:
            print(f"Error al recargar el progreso del usuario: {e}")

    def update_current_user(self, username):
        try:
            current_user = {"current_user": username}
            with open('current_user.json', 'w', encoding='UTF-8') as file:
                json.dump(current_user, file)
        except Exception as e:
            print(f"Error al actualizar current_user.json: {e}")

