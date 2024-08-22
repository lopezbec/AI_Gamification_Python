import json
import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from question_window import QuestionWindow
from datetime import datetime
import sys


class NameWindow(QMainWindow):
    nameEntered = pyqtSignal(str)
    progressNeedsReload = pyqtSignal()

    def __init__(self) -> None:
        super(NameWindow, self).__init__()
        self.question_window = None
        self.should_exit_on_close = True
        self._load_ui_data()
        self._setup_ui()
        self.leaderboard_file =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Codigos_LeaderBoard', 'leaderboard.json')  # Ruta al archivo leaderboard.json

    def _load_ui_data(self):
        # Obtiene la ruta del directorio donde se encuentra el script actual
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al archivo JSON usando os.path.join
        json_path = os.path.join(current_script_path, 'json', 'name_info.json')
        with open(json_path, "r", encoding='UTF-8') as name_info:
            self.data = json.load(name_info)

    def _setup_ui(self):
        self.setWindowTitle(self.data["window_title"])
        layoutV = QVBoxLayout()
        layoutV.setSpacing(10)
        layoutV.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Agregar el formulario al layout
        layoutV.addLayout(self._create_form_layout())

        #Enable Keyboard Navigation: Allow Advance to Next Slide with Enter by Daniel.
        self.input.returnPressed.connect(self.show_survey)

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
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usernames.json'), 'r', encoding='UTF-8') as file:
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
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'current_user.json'), 'w', encoding='UTF-8') as file:
                json.dump(current_user, file)
        except Exception as e:
            print(f"Error al actualizar current_user.json: {e}")

    def _update_usernames_json(self, username):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usernames.json'), 'r', encoding='UTF-8') as file:
                usernames = json.load(file)
        except FileNotFoundError:
            usernames = []

        if username not in usernames:
            usernames.append(username)
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usernames.json'), 'w', encoding='UTF-8') as file:
                json.dump(usernames, file)

    @staticmethod
    def _update_progress_json(username):
        progreso_inicial = {
            "Modulo1": {"Leccion1": True, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False, "Quiz1": False, "Quiz2": False},
            "Modulo2": {"Leccion1": False, "Leccion2": False, "Leccion3": False, "Quiz1": False, "Quiz2": False},
            "Modulo3": {"Leccion1": False, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False, "Quiz1": False, "Quiz2": False},
            "Modulo4": {"Leccion1": False, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False, "Quiz1": False, "Quiz2": False},
            "Modulo5": {"Leccion1": False, "Leccion2": False, "Leccion3": False, "Leccion4": False, "Leccion5": False,
                        "Leccion6": False, "Leccion7": False, "Quiz1": False, "Quiz2": False}
        }

        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progreso.json'), 'r', encoding='UTF-8') as file:
                progreso = json.load(file)
        except FileNotFoundError:
            progreso = {}

        if username not in progreso:
            progreso[username] = progreso_inicial
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progreso.json'), 'w', encoding='UTF-8') as file:
                json.dump(progreso, file, indent=4)

    def show_survey(self):
        username = self.input.text().strip()
        if not username:
            QMessageBox.warning(self, "Campo vacío", "El campo no puede estar vacío.")
            self.input.setStyleSheet("border: 1px solid red;")
            return  # Stop the method if the input is empty

        if not self.is_valid_username(username):
            QMessageBox.warning(self, "Error de entrada", "El nombre solo puede tener letras.")
            self.input.setStyleSheet("border: 1px solid red;")
            return  # Stop the method if the input is invalid

        # Reset the style if the input is valid
        self.input.setStyleSheet("")
        self.should_exit_on_close = False
        self.update_current_user(username)
        self.update_user_last_active(username)

        if not self.user_exists(username):  # Check if exists in leaderboard.json
            self.add_user_to_leaderboard(username)  # Add user to leaderboard.json
            self.agregar_usuario_leccion_completada(username)
            self.add_username(username)  # Add user to existing files
            self._open_question_window(username)
            self.close()
        else:
            self.close()

    def is_valid_username(self, username):
        return username.isalpha()  # Checks if the username contains only letters

    def closeEvent(self, event):
        if self.should_exit_on_close:
            sys.exit()  # Termina el programa si se cierra con la "X"
        else:
            event.accept()  # Solo cierra la ventana pero no termina el programa

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

            ''' AVISO: The else condition below was commented in order to resolve bug #48
                (https://github.com/lopezbec/AI_Gamification_Python/issues/48)
                If this else was added to resolve or control 
                some type of scenario identified in the past, 
                please mention it in the issue thread to be discussed and find a useful solution 
            '''

            for user in users:
                if user['name'] == username:
                    user['last_active'] = current_datetime
                    break
            # else:
            #     # Si el usuario no existe, agrégalo.
            #     users.append({
            #         "name": username,
            #         "points": 0,
            #         "last_active": current_datetime
            #     })
            #     print("Agregaste un usuario desde last active")

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
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leccion_completada.json'), 'r',
                      encoding='UTF-8') as file:
                progreso = json.load(file)
        except Exception as e:
            print(f"Error archivo: {e}")
            progreso = {}

        try:
            if username not in progreso:
                progreso[username] = {
                    "Modulo1": {f"Leccion_completada{i}": False for i in range(1, 6)} | {f"Quiz_completado{i}": False
                                                                                         for i in range(1, 3)},
                    "Modulo2": {f"Leccion_completada{i}": False for i in range(1, 4)} | {f"Quiz_completado{i}": False
                                                                                         for i in range(1, 3)},
                    "Modulo3": {f"Leccion_completada{i}": False for i in range(1, 6)} | {f"Quiz_completado{i}": False
                                                                                         for i in range(1, 3)},
                    "Modulo4": {f"Leccion_completada{i}": False for i in range(1, 6)} | {f"Quiz_completado{i}": False
                                                                                         for i in range(1, 3)},
                    "Modulo5": {f"Leccion_completada{i}": False for i in range(1, 8)} | {f"Quiz_completado{i}": False
                                                                                         for i in range(1, 3)}
                }

                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leccion_completada.json'), 'w',
                          encoding='UTF-8') as file:
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
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'current_user.json'), 'w', encoding='UTF-8') as file:
                json.dump(current_user, file)
        except Exception as e:
            print(f"Error al actualizar current_user.json: {e}")
