import json
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from question_window import QuestionWindow
from datetime import datetime


class NameWindow(QMainWindow):
    nameEntered = pyqtSignal(str)
    progressNeedsReload = pyqtSignal()

    def __init__(self) -> None:
        super(NameWindow, self).__init__()
        self.question_window = None
        self._load_ui_data()
        self._setup_ui()
        self.leaderboard_file = './Codigos_LeaderBoard/leaderboard.json'  # Ruta al archivo leaderboard.json

    def _load_ui_data(self):
        with open(r'./json/name_info.json', "r", encoding='UTF-8') as name_info:
            self.data = json.load(name_info)

    def _setup_ui(self):
        self.setWindowTitle = self.data["window_title"]
        layoutV = QVBoxLayout()
        layoutV.setSpacing(10)
        layoutV.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        layoutV.addLayout(self._create_form_layout())
        widget = QWidget()
        widget.setLayout(layoutV)
        self.showMaximized()
        self.setCentralWidget(widget)

    def _create_form_layout(self):
        layoutForm = QFormLayout()
        layoutForm.addRow(self._create_label())
        layoutForm.addRow(self._create_input_and_button())
        layoutForm.setContentsMargins(10, 10, 10, 10)
        return layoutForm

    def _create_label(self):
        ask_name = QLabel(self)
        ask_name.setText(self.data["ask_name_title"])
        font = QFont()
        ask_name.setFont(font)
        font.setPointSize(self.data["ask_name_font_size"])
        ask_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ask_name.setStyleSheet(f"font-size:{self.data['ask_name_font_size']}px")
        ask_name.setMargin(self.data["ask_name_margin"])
        return ask_name

    def _create_input_and_button(self):
        layout_V_Form = QVBoxLayout()
        self.input = QLineEdit(self)
        self.input.setContentsMargins(self.data["input_margin"]["left"], self.data["input_margin"]["top"],
                                      self.data["input_margin"]["right"], self.data["input_margin"]["bottom"])
        self.input.setMinimumWidth(self.data["input_minimum_width"])
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton(self.data["button_text"], self)
        button.clicked.connect(self.show_survey)
        button.setStyleSheet(f"background-color: {self.data['continue_button_color']};color: white;font-size:{self.data['font_size_buttons']}px")
        button.setMinimumWidth(self.data["button_minimun_width"])

        layout_V_Form.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_V_Form.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
        return layout_V_Form

    @staticmethod
    def user_exists(username):
        try:
            with open('usernames.json', 'r', encoding='UTF-8') as file:
                usernames = json.load(file)
            return username in usernames
        except FileNotFoundError:
            return False

    def add_username(self, username):
        self._update_current_user_json(username)
        self._update_usernames_json(username)
        self._update_progress_json(username)
        self.progressNeedsReload.emit()

    @staticmethod
    def _update_current_user_json(username):
        try:
            current_user = {"current_user": username}
            with open('current_user.json', 'w', encoding='UTF-8') as file:
                json.dump(current_user, file)
        except Exception as e:
            print(f"Error al actualizar current_user.json: {e}")

    def _update_usernames_json(self, username):
        try:
            with open('usernames.json', 'r', encoding='UTF-8') as file:
                usernames = json.load(file)
        except FileNotFoundError:
            usernames = []

        if username not in usernames:
            usernames.append(username)
            with open('usernames.json', 'w', encoding='UTF-8') as file:
                json.dump(usernames, file)

    @staticmethod
    def _update_progress_json(username):
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

    def show_survey(self):
        username = self.input.text().strip()
        if username:
            self.update_current_user(username)
            self.update_user_last_active(username)

            if not self.user_exists(username):  # Verificar si existe en leaderboard.json
                self.add_user_to_leaderboard(username)  # Agregar usuario a leaderboard.json
                self.agregar_usuario_leccion_completada(username)
                self.add_username(username)  # Agregar usuario a los archivos existentes
                self._open_question_window(username)
            else:
                self.close()

    def user_exists_in_leaderboard(self, username):
        try:
            with open(self.leaderboard_file, 'r', encoding='UTF-8') as file:
                users = json.load(file)
            for user in users:
                if user['name'] == username:
                    return True
            return False
        except FileNotFoundError:
            return False

    def update_user_last_active(self, username):
        current_datetime = datetime.now().strftime("%Y-%m-%d ; %Hh:%Mm")
        try:
            with open(self.leaderboard_file, 'r', encoding='UTF-8') as file:
                users = json.load(file)

            for user in users:
                if user['name'] == username:
                    user['last_active'] = current_datetime
                    break
            else:
                # Si el usuario no existe, agrégalo.
                users.append({
                    "name": username,
                    "points": 0,
                    "last_active": current_datetime
                })

            with open(self.leaderboard_file, 'w', encoding='UTF-8') as file:
                json.dump(users, file, indent=4)

        except FileNotFoundError:
            # Si el archivo no existe, crea uno nuevo con el usuario actual.
            with open(self.leaderboard_file, 'w', encoding='UTF-8') as file:
                json.dump([{
                    "name": username,
                    "points": 0,
                    "last_active": current_datetime
                }], file, indent=4)

    def add_user_to_leaderboard(self, username):
        current_datetime = datetime.now().strftime("%Y-%m-%d ; %Hh:%Mm")  # Formato específico para fecha y hora
        new_user = {
            "name": username,
            "points": 0,
            "last_active": current_datetime  # Fecha y hora actual en el formato específico
        }

        try:
            with open(self.leaderboard_file, 'r', encoding='UTF-8') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

        users.append(new_user)
        with open(self.leaderboard_file, 'w', encoding='UTF-8') as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def agregar_usuario_leccion_completada(username):
        # Añadir usuario a leccion_completada.json
        try:
            with open('leccion_completada.json', 'r', encoding='UTF-8') as file:
                progreso = json.load(file)
        except Exception as e:
            print(f"Error archivo: {e}")

        try:

            if username not in progreso:
                progreso[username] = {
                    "Modulo1": {f"Leccion_completada{i}": False for i in range(1, 6)},
                    "Modulo2": {f"Leccion_completada{i}": False for i in range(1, 4)},
                    "Modulo3": {f"Leccion_completada{i}": False for i in range(1, 6)},
                    "Modulo4": {f"Leccion_completada{i}": False for i in range(1, 6)},
                    "Modulo5": {f"Leccion_completada{i}": False for i in range(1, 8)}
                }

                with open('leccion_completada.json', 'w', encoding='UTF-8') as file:
                    json.dump(progreso, file, indent=4)

        except Exception as e:
            print(f"Error: {e}")

    def _open_question_window(self, username):
        self.question_window = QuestionWindow()
        self.question_window.username = username
        self.question_window.read_csv()
        self.question_window.show()

    @staticmethod
    def update_current_user(username):
        try:
            current_user = {"current_user": username}
            with open('current_user.json', 'w', encoding='UTF-8') as file:
                json.dump(current_user, file)
        except Exception as e:
            print(f"Error al actualizar current_user.json: {e}")
