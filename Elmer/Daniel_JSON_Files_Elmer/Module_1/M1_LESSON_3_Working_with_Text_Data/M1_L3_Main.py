import re
import os
import sys
import csv
import json
import datetime
import drag_drop

from PyQt6 import QtWidgets
from functools import partial
from PyQt6.QtGui import QFont, QDrag
from PyQt6.QtCore import Qt, QMimeData
from qtconsole.manager import QtKernelManager
from custom_console import CustomPythonConsole
from game_features.progress_bar import ProgressBar
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QRadioButton, QButtonGroup, QSizePolicy, QCheckBox


class JsonLoader:
    @staticmethod
    def load_json_data(filename):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), encoding='UTF-8') as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def load_json_styles():
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.json")) as styles_file:
            styles = json.load(styles_file)
        return styles


class JsonWindow(QWidget):
    def __init__(self, filename, page_type, json_number, xp_ganados, lesson_completed, main_window=None):
        super().__init__()

        self.data = None
        self.layout = None
        self.hint_label = None
        self.progress_bar = None
        self.button_group = None
        self.radio_buttons = None
        self.button_widgets = None
        self.blank_space_index = None
        self.current_text_state = None
        self.leaderboard_button = None
        self.original_hint_text = None
        self.main_window = main_window
        self.puntos = QLabel()
        self.update_points_display(self.main_window.XP_Ganados)
        self.filename = filename
        self.page_type = page_type
        self.XP_Ganados = xp_ganados
        self.feedback_label = QLabel(self)
        self.lesson_completed = lesson_completed
        self.styles = JsonLoader.load_json_styles()
        self.lesson_number = self.get_lesson_number(filename)  # Obteniendo el número de lección de alguna manera
        self.json_number = json_number
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.data = JsonLoader.load_json_data(self.filename)

        # Crear un nuevo layout horizontal
        hlayout = QHBoxLayout()

        # Crear el widget de puntos
        self.puntos = QLabel(f"XP ganados: {self.XP_Ganados}")
        self.puntos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.puntos.setStyleSheet(f"background-color: grey; color: white; border: 2px solid black")
        puntos_font = QFont()
        puntos_font.setPointSize(self.styles["font_size_normal"])
        self.puntos.setFont(puntos_font)

        # Crear el botón de Leaderboard
        self.leaderboard_button = QPushButton("Leaderboard")
        self.leaderboard_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        leaderboard_button_font = QFont()
        leaderboard_button_font.setPointSize(self.styles['font_size_buttons'])
        self.leaderboard_button.setFont(leaderboard_button_font)
        self.leaderboard_button.clicked.connect(self.abrir_leaderboard)  # Esta función necesita ser definida

        # Añadir los widgets al layout horizontal
        hlayout.addWidget(self.puntos)
        hlayout.addWidget(self.progress_bar)  # Añade la barra de progreso aquí.
        hlayout.addWidget(self.leaderboard_button)

        # Añadir el layout horizontal al layout vertical
        self.layout.addLayout(hlayout)

        self.title()  # Ahora añadimos el título

        if self.page_type.lower() == "multiplechoice":
            multiplechoiceplus_value = self.data[self.page_type.lower()][0].get("multiplechoiceplus", False)
            if multiplechoiceplus_value:
                self.create_multiple_choice_layout(is_multiple_choice_plus=True)
            else:
                self.create_multiple_choice_layout(is_multiple_choice_plus=False)
            self.create_feedback_label()

        elif self.page_type.lower() == "completeblankspace":
            self.create_complete_blank_space_layout()
            self.create_feedback_label()

        elif self.page_type.lower() == "draganddrop":
            self.create_drag_and_drop_layout()
            self.create_feedback_label()

        elif self.page_type.lower() == "practica":
            self.create_practice_layout()
            self.create_feedback_label()

        # Si el tipo de página es "pedagogical", agregar bloques de contenido
        elif self.page_type.lower() == "pedagogical" or self.page_type.lower() == "pedagogical2":
            self.create_pedagogical_layout()

        else:
            print("Lo siento no se encontró el tipo de página especificada, O el tipo de página que se especificó no se ha configurado su lógica todavía. Configurar la lógica y ponerla aquí.")

        # Establecer el layout en el QWidget
        self.setWindowTitle('JsonWindow')
        self.setLayout(self.layout)

    @staticmethod
    def get_lesson_number(filename):
        base = os.path.basename(filename)  # Obtén el nombre del archivo con la extensión
        lesson_number = os.path.splitext(base)[0][-1]  # Elimina la extensión y toma el último carácter
        return int(lesson_number)  # Convierte el número de lecciones a un entero

    def update_points(self, new_points):
        if self.main_window is not None:
            self.main_window.update_xp(new_points)

    def update_points_display(self, new_points):
        self.puntos.setText(f"XP ganados: {new_points}")

    def showEvent(self, event):
        super().showEvent(event)
        self.update_points_display(self.main_window.XP_Ganados)

    @staticmethod
    def abrir_leaderboard():
        LeaderBoard()

    def title(self):
        title = QLabel(self.data[self.page_type.lower()][0]["title"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"background-color: {self.styles['title_background_color']}; color: {self.styles['title_text_color']}; border: 2px solid {self.styles['title_border_color']}")
        title_font = QFont()
        title_font.setPointSize(self.styles["font_size_titles"])
        title.setFont(title_font)
        self.layout.addWidget(title)

    def createResetBottom(self):
        # Add a reset button to the layout
        reset_button = QPushButton('Reiniciar')
        reset_button.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white; border: 1px solid black; padding: 5px; border-radius: 5px")
        self.layout.addWidget(reset_button)
        reset_button.clicked.connect(self.reset_button)

    def handle_answer_click(self, answer_text):
        # Restaurar el texto original de la pista
        self.hint_label.setText(self.original_hint_text)

        # Reemplazar el espacio en blanco con la respuesta seleccionada
        updated_hint = self.hint_label.text()[:self.blank_space_index] + answer_text + self.hint_label.text()[self.blank_space_index + 1:]
        self.hint_label.setText(updated_hint)

    def create_feedback_label(self):
        # Añadir la etiqueta de retroalimentación al layout
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setMinimumHeight(0)
        self.feedback_label.setMaximumHeight(50)  # Ajusta este valor según sea necesario
        self.layout.addWidget(self.feedback_label)

    def create_complete_blank_space_layout(self):
        self.blank_space_index = -1
        self.original_hint_text = ""

        # Añadir bloques de contenido al layout
        for idx, block in enumerate(self.data[self.page_type.lower()][0]["blocks"]):
            if block["type"] == "info":
                block_label = QLabel(block["text"])
                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)
            elif block["type"] == "Consola":
                self.hint_label = QLabel(block["text"])
                self.hint_label.setStyleSheet(f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(self.hint_label)
                self.blank_space_index = block["text"].find("_")
                self.original_hint_text = block["text"]

        # Crear un layout horizontal para los botones de respuesta
        answers_layout = QHBoxLayout()

        # Añadir botones de respuesta al layout horizontal
        for idx, answer in enumerate(self.data[self.page_type.lower()][0]["answers"]):
            answer_button = QPushButton(answer["text"])
            answer_button.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white")
            answer_button.clicked.connect(partial(self.handle_answer_click, answer["text"]))
            answers_layout.addWidget(answer_button)

        # Añadir el layout horizontal de botones de respuesta al layout principal (vertical)
        self.layout.addLayout(answers_layout)
        self.createResetBottom()

    def create_multiple_choice_layout(self, is_multiple_choice_plus=False):
        self.button_widgets = []  # Esta lista almacenará las QCheckBox o QRadioButton.
        self.button_group = QButtonGroup()

        answers_layout = QHBoxLayout()  # Nuevo layout horizontal para las respuestas

        for idx, block in enumerate(self.data[self.page_type.lower()][0]["blocks"]):
            block_type = block["type"]
            block_label = QLabel(block["text"])
            block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
            if block["type"] == "Consola":
                block_label.setStyleSheet(f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
            self.layout.addWidget(block_label)

        for idx, answer in enumerate(self.data[self.page_type.lower()][0]["answers"]):
            button_widget = QCheckBox(answer["text"]) if is_multiple_choice_plus else QRadioButton(answer["text"])
            button_widget.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white")
            self.button_widgets.append(button_widget)
            self.button_group.addButton(button_widget, idx)
            answers_layout.addWidget(button_widget)  # Agregar al layout horizontal en lugar del vertical

        if is_multiple_choice_plus:
            self.button_group.setExclusive(False)  # Permitir la selección de múltiples respuestas

        self.layout.addLayout(answers_layout)  # Agregar el layout horizontal al layout principal
        self.createResetBottom()

    def create_drag_and_drop_layout(self):
        drop_labels = {}
        data_block = self.data[self.page_type.lower()][0]

        if "draganddropSecuence" in data_block and data_block["draganddropSecuence"]:

            for idx, block in enumerate(data_block["blocks"]):
                block_type = block["type"]

                if "correctOrder" in data_block:
                    multiple_drops = len(data_block["correctOrder"]) > 1
                else:
                    multiple_drops = False

                if block_type == "Consola":
                    drop_labels[block_type] = drag_drop.DropLabel(block["text"], self.styles, question_type=block_type, multiple=multiple_drops)
                    block_label = drop_labels[block_type]
                else:
                    block_label = QLabel(block["text"])

                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)

        else:

            for idx, block in enumerate(data_block["blocks"]):
                block_type = block["type"]

                if "correctValue" in block or "correctOrder" in data_block:
                    multiple_drops = "correctOrder" in data_block and len(
                        data_block["correctOrder"]) > 1
                    drop_labels[block_type] = drag_drop.DropLabel(block["text"], self.styles, question_type=block_type,
                                                                  multiple=multiple_drops)
                    block_label = drop_labels[block_type]
                elif block_type == "Consola":
                    block_label = drag_drop.DropLabel(block["text"], self.styles)
                else:
                    block_label = QLabel(block["text"])

                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)

        draggable_labels_layout = QHBoxLayout()
        draggable_labels_layout.setSpacing(50)

        for idx, answer in enumerate(data_block["answers"]):
            draggable_label = drag_drop.DraggableLabel(answer["text"])
            draggable_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white; border: 1px solid black; padding: 5px; border-radius: 5px")
            draggable_labels_layout.addWidget(draggable_label)

        self.layout.addLayout(draggable_labels_layout)
        self.createResetBottom()

    def reset_button(self):
        # Remove all current widgets from the layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add the puntos and leaderboard_button widgets back to the layout
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.puntos)
        hlayout.addWidget(self.leaderboard_button)
        self.layout.insertLayout(0, hlayout)  # Insert at the beginning of the layout

        # Call the function that creates the initial layout again
        self.title()
        if self.page_type.lower() == "draganddrop":
            self.create_drag_and_drop_layout()

        if self.page_type.lower() == "multiplechoice":
            if self.data[self.page_type.lower()][0].get("multiplechoiceplus", False):
                self.create_multiple_choice_layout(is_multiple_choice_plus=True)
            else:
                self.create_multiple_choice_layout(is_multiple_choice_plus=False)

        elif self.page_type.lower() == "completeblankspace":
            self.create_complete_blank_space_layout()
        else:
            self.create_pedagogical_layout()

        self.create_feedback_label()

    def create_practice_layout(self):
        for block in self.data[self.page_type.lower()][0]["blocks"]:
            block_label = QLabel(block["text"])

            if block["type"] == "hint":
                block_label.setStyleSheet(f"border: {self.styles['hint_border_width']}px solid {self.styles['hint_border_color']}; background-color: {self.styles['hint_background_color']}; font-size: {self.styles['font_size_normal']}px")
            elif block["type"] == "Consola":
                block_label.setStyleSheet(f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
            else:
                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")

            self.layout.addWidget(block_label)  # Añadir el bloque al layout

    def create_pedagogical_layout(self):
        for block in self.data[self.page_type.lower()][0]["blocks"]:
            block_label = QLabel(block["text"])
            if block["type"] == "hint":
                block_label.setStyleSheet(f"border: {self.styles['hint_border_width']}px solid {self.styles['hint_border_color']}; background-color: {self.styles['hint_background_color']}; font-size: {self.styles['font_size_normal']}px")
            elif block["type"] == "Consola":
                block_label.setStyleSheet(f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
            else:
                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")

            self.layout.addWidget(block_label)  # Añadir el bloque al layout


class MainWindow(QWidget):
    def __init__(self, lesson_number=3, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_data = []
        self.layout = None
        self.current_xp = 0
        self.XP_Ganados = 0
        self.click_data = []
        self.total_pages = 0
        self.completed = None
        self.current_page = 0
        self.json_windows = []
        self.back_button = None
        self.time_log_data = []
        self.mouse_log_data = []
        self.current_part = None
        self.controlador = False
        self.button_layout = None
        self.submit_button = None
        self.stacked_widget = None
        self.python_console = None
        self.practice_button = None
        self.continue_button = None
        self.last_json_number = None
        self.last_page_number = None
        self.leaderboard_button = None
        self.python_console_widget = None
        self.lesson_number = lesson_number
        self.lesson_finished_successfully = False
        self.styles = JsonLoader.load_json_styles()
        self.setWindowTitle("Aprendiendo Python - Lección 3")

        self.progress_bar = ProgressBar(JsonLoader.load_json_data(os.path.join("..", "page_order.json")), 2)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setStyleSheet(f"background-color: {self.styles['main_background_color']}")
        self.stacked_widget = QStackedWidget()

        for page in self.load_page_order():
            if page["type"] == "JsonWindow":
                json_window = JsonWindow(page["filename"], page["page_type"], page["json_number"], self.XP_Ganados, page.get("lesson_completed", False), main_window=self)
                self.json_windows.append(json_window)
                self.stacked_widget.addWidget(json_window)

        self.log_part_change()
        self.log_event(f"{self.stacked_widget.currentWidget().page_type.capitalize()} Page Open Time", True)

        self.continue_button = QPushButton("Continuar")
        self.continue_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        continue_button_font = QFont()
        continue_button_font.setPointSize(self.styles["font_size_buttons"])
        self.continue_button.setFont(continue_button_font)
        self.continue_button.clicked.connect(lambda: self.switch_page(forward=True))

        self.back_button = QPushButton("Retroceder")
        self.back_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        back_button_font = QFont()
        back_button_font.setPointSize(self.styles["font_size_buttons"])
        self.back_button.setFont(continue_button_font)
        self.back_button.clicked.connect(lambda: self.switch_page(forward=False))
        self.back_button.hide()

        self.submit_button = QPushButton("Enviar")
        self.submit_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        submit_button_font = QFont()
        submit_button_font.setPointSize(self.styles['font_size_buttons'])
        self.submit_button.setFont(submit_button_font)
        self.submit_button.clicked.connect(self.submit_answer)
        self.submit_button.hide()

        self.practice_button = QPushButton("Practica")
        self.practice_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        practice_button_font = QFont()
        practice_button_font.setPointSize(self.styles["font_size_buttons"])
        self.practice_button.setFont(practice_button_font)
        self.practice_button.clicked.connect(self.open_python_console)
        self.practice_button.hide()

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.practice_button)
        self.button_layout.addWidget(self.continue_button)

        self.layout.addWidget(self.progress_bar)  # Agrega la barra de progreso al layout
        self.layout.addWidget(self.stacked_widget)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.showMaximized()

    def update_xp(self, new_points):
        self.XP_Ganados += new_points
        for window in self.json_windows:
            window.update_points_display(self.XP_Ganados)

    @staticmethod
    def lesson_completed():
        return True

    def SubmitAnswers(self, NoSeleciona, Correcto, Incorrecto):
        current_widget = self.stacked_widget.currentWidget()

        if NoSeleciona:
            current_widget.feedback_label.setText("No se ha seleccionado ninguna respuesta")
            current_widget.feedback_label.setStyleSheet(
                f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")
        elif Correcto:
            # Incrementa el XP en 2 puntos cuando la respuesta es acertada en el primer intento y tiene 0 xp (0 XP significa primera página con pregunta)
            if self.current_xp == 0 and not self.controlador:
                self.current_xp = 2
            # Incrementa el XP en 1 punto cuando la respuesta es correcta en el segundo o más intentos y tiene 0 xp (0 XP significa primera página con pregunta)
            elif self.current_xp == 0 and self.controlador:
                self.current_xp = 1
                self.controlador = False
            # Disminuye el XP de 2 puntos a 1 punto cuando la primera respuesta fue acertada en el primer intento y ahora en el segundo o más intentos.
            elif self.current_xp == 2 and self.controlador:
                self.current_xp = 1
                self.controlador = False
            # Aumenta el XP de 1 punto a 2 puntos cuando la primera respuesta fue acertada en el segundo o más intentos y ahora en el primero
            elif self.current_xp == 1 and not self.controlador:
                self.current_xp = 2

            if self.current_xp == 2:
                current_widget.feedback_label.setText(f"Respuesta correcta. Haz ganado 2 puntos.")
            else:
                current_widget.feedback_label.setText(f"Respuesta correcta. Haz ganado 1 punto.")

            current_widget.update_points(self.current_xp)  # actualiza los puntos en el widget actual
            current_widget.feedback_label.setStyleSheet(
                f"color: {self.styles['correct_color']}; font-size: {self.styles['font_size_answers']}px")
            self.SubmitHideContinueShow(True, False)
        elif Incorrecto:
            self.controlador = True
            current_widget.feedback_label.setText("Respuesta incorrecta. Por favor, inténtalo de nuevo.")
            current_widget.feedback_label.setStyleSheet(
                f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")
        else:
            self.controlador = True
            current_widget.feedback_label.setText("Respuesta incompleta, vuelve a intentarlo.")
            current_widget.feedback_label.setStyleSheet(
                f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")

    def open_python_console(self):
        self.SubmitHideContinueShow(True, False)
        print("La consola no está disponible por el momento.")

    def SubmitHideContinueShow(self, pedagogical, practica):
        if pedagogical:
            self.submit_button.hide(), self.practice_button.hide(), self.continue_button.show(), self.back_button.show()
        elif practica:
            self.submit_button.hide(), self.practice_button.show(), self.continue_button.hide(), self.back_button.show()
        else:
            self.submit_button.show(), self.practice_button.hide(), self.continue_button.hide(), self.back_button.show()

    def log_part_change(self):
        event_time = datetime.datetime.now().strftime("%H:%M:%S")
        json_number = self.stacked_widget.currentWidget().json_number

        # Si la parte cambia, agrega la entrada de "Parte X"
        if not hasattr(self, 'current_part') or self.current_part != json_number:
            self.current_part = json_number
            self.time_log_data.append({"event": f"Parte {self.current_part}", "time": event_time})
            self.mouse_log_data.append({"event": f"Parte {self.current_part}", "time": event_time})

    def log_event(self, event, event_type="time"):
        event_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Añadir el evento y su hora al registro de datos (log_data)
        if event_type == "mouse":
            self.mouse_log_data.append({"event": event, "time": event_time})
        else:
            self.time_log_data.append({"event": event, "time": event_time})

    def save_log(self, log_type="time"):
        fieldnames = ['event', 'time']
        filename = "M1_L3_Time.csv" if log_type == "time" else "M1_L3_Entradas_Salidas_Clics.csv"
        log_data = self.time_log_data if log_type == "time" else self.mouse_log_data

        # Asegurarte de que el directorio existe, si no, lo crea
        if not os.path.exists('M1_LESSON_3_Working_with_Text_Data'):
            os.makedirs('M1_LESSON_3_Working_with_Text_Data')

        # Guardar el archivo en la carpeta especificada
        filepath = os.path.join('M1_LESSON_3_Working_with_Text_Data', filename)

        with open(filepath, mode="a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0: writer.writeheader()
            for log in log_data: writer.writerow(log)
            csv_file.write('\n')

    def load_page_order(self):
        with open("page_order.json", "r") as file:
            data = json.load(file)

        for lesson in data["lessons"]:
            if lesson["lesson_number"] == self.lesson_number:
                return lesson["pages"]

        raise ValueError(f"Lesson {self.lesson_number} not found in page_order.json")

    def submit_answer(self):
        current_widget = self.stacked_widget.currentWidget()
        current_page_type = current_widget.page_type.lower()

        if current_page_type == "multiplechoice":
            selected_answers = []  # Respuestas seleccionadas
            correct_answers = []  # Respuestas correctas
            # Iterar sobre los botones
            for idx, button in enumerate(current_widget.button_widgets):
                if button.isChecked():
                    selected_answers.append({
                        "text": button.text(),
                        "correct": current_widget.data[current_page_type][0]["answers"][idx]["correct"]
                    })
                    self.log_event(f"Checkbox Selected: {button.text()}", event_type="mouse")  # Log mouse event

            # Iterar sobre las respuestas
            for answer in current_widget.data[current_page_type][0]["answers"]:
                if answer["correct"]:
                    correct_answers.append(answer["text"])

            # Verificar las respuestas seleccionadas
            if selected_answers:
                correct_selected = [answer for answer in selected_answers if answer["correct"]]
                incorrect_selected = [answer for answer in selected_answers if not answer["correct"]]

                # Verificar las respuestas correctas seleccionadas y si hay alguna incorrecta seleccionada
                if len(correct_selected) == len(correct_answers) and len(incorrect_selected) == 0:
                    self.SubmitAnswers(False, True, False)  # Correcto
                elif len(correct_selected) < len(correct_answers) and len(incorrect_selected) == 0:
                    self.SubmitAnswers(False, False, True)  # Incompleto
                else:
                    self.SubmitAnswers(False, False, True)  # Incorrecto
            else:
                self.SubmitAnswers(True, False, False)  # Respuesta no seleccionada

        elif current_page_type == "draganddrop":
            drop_labels = current_widget.findChildren(drag_drop.DropLabel)
            correct_count = 0
            unanswered = 0
            data_block = current_widget.data[current_page_type][0]

            if "draganddropSecuence" in data_block and data_block["draganddropSecuence"]:
                for label in drop_labels:
                    dropped_texts = label.dropped_texts
                    label_type = label.question_type

                    if len(dropped_texts) == 0:
                        unanswered += 1
                        continue

                    if data_block.get("multipleResponses"):
                        correct_order = None

                        if "correctOrder" in data_block:
                            correct_order = data_block["correctOrder"]

                        if correct_order:
                            if correct_order == dropped_texts:
                                for text in dropped_texts:
                                    self.log_event(f"Correct Drop Event: {text}", event_type="mouse")
                                correct_count += 1
                            else:
                                for text in dropped_texts:
                                    self.log_event(f"Incorrect Drop Event: {text}", event_type="mouse")

                    else:
                        correct_answer = None
                        for option in data_block["answers"]:
                            if option["correct"] and (label_type is None or option.get("correctType") == label_type):
                                correct_answer = option
                                break

                        if correct_answer:
                            if correct_answer["text"] in dropped_texts[0]:
                                self.log_event(f"Correct Drop Event: {dropped_texts[0]}", event_type="mouse")
                                correct_count += 1
                            else:
                                self.log_event(f"Incorrect Drop Event: {dropped_texts[0]}", event_type="mouse")

            else:
                for label in drop_labels:
                    full_dropped_text = label.drop_area.text()
                    label_type = label.question_type

                    if "____" in full_dropped_text or "_" in full_dropped_text:
                        unanswered += 1
                        continue

                    if "multipleResponseVariant" in data_block and data_block["multipleResponseVariant"]:
                        if ":" in full_dropped_text:
                            dropped_text = full_dropped_text.split(':')[1].strip()
                        else:
                            dropped_text = full_dropped_text.strip().split('\n')[-1]

                        correct_value = None
                        for block in data_block["blocks"]:
                            if block["type"] == label_type:
                                correct_value = block.get("correctValue")
                                break

                        if "print" in dropped_text:
                            sep_argument = re.findall(r"(sep)=(['\"]([^'\"]*)['\"])", dropped_text)
                            if sep_argument:
                                dropped_answer = sep_argument[0][0] if correct_value == 'sep' else sep_argument[0][1]
                                if correct_value:
                                    if correct_value == dropped_answer:
                                        correct_count += 1
                                        self.log_event(f"Correct Answer Selected: {dropped_answer}", event_type="mouse")
                                    else:
                                        self.log_event(f"Incorrect Answer Selected: {dropped_answer}", event_type="mouse")
                        else:
                            if correct_value:
                                if correct_value == dropped_text:
                                    correct_count += 1
                                    self.log_event(f"Correct Answer Selected: {dropped_text}", event_type="mouse")

                                else:
                                    self.log_event(f"Incorrect Answer Selected: {dropped_text}", event_type="mouse")

                    else:
                        correct_answer = None
                        for option in data_block["answers"]:
                            if option["correct"] and (label_type is None or option.get("correctType") == label_type):
                                correct_answer = option
                                break

                        if correct_answer:
                            if correct_answer["text"] in full_dropped_text:
                                correct_count += 1
                                self.log_event(f"Correct Answer Selected: {full_dropped_text}", event_type="mouse")  # Registrar la respuesta correcta como "Correcto"
                            else:
                                self.log_event(f"Incorrect Answer Selected: {full_dropped_text}", event_type="mouse")  # Registrar la respuesta incorrecta como "Incorrecto"

            if unanswered == len(drop_labels):
                self.SubmitAnswers(True, False, False)
            elif unanswered > 0:
                self.SubmitAnswers(False, False, False)
            elif correct_count == len(drop_labels):
                self.SubmitAnswers(False, True, False)
            else:
                self.SubmitAnswers(False, False, True)

        elif current_page_type == "completeblankspace":
            correct_answer_text = None

            for answer in current_widget.data[current_page_type][0]["answers"]:
                if answer["correct"]:
                    correct_answer_text = answer["text"]
                    break

            if selected_symbol == "_":
                self.log_event(f"Blank Space Selected", event_type="mouse")  # Log mouse event
                self.SubmitAnswers(True, False, False)

            elif selected_symbol == correct_answer_text:
                self.log_event(f"Correct Answer Selected: {correct_answer_text}", event_type="mouse")  # Log mouse event
                self.SubmitAnswers(False, True, False)

            else:
                self.log_event(f"Incorrect Answer Selected: {selected_symbol}", event_type="mouse")  # Log mouse event
                self.SubmitAnswers(False, False, True)

    def switch_page(self, forward=True):
        current_index = self.stacked_widget.currentIndex()

        if forward:
            next_index = current_index + 1
        else:
            next_index = current_index - 1

        current_page_type = self.stacked_widget.currentWidget().page_type.lower()  # Obtener el tipo de página actual
        self.log_event(
            f"{current_page_type.capitalize()} Page Close Time")  # Registrar el evento de cierre de la página actual

        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, "lesson_completed"):
            self.lesson_finished_successfully = True

        # Si el siguiente índice es menor que el número total de páginas, continuar navegando
        if next_index < self.stacked_widget.count():
            if forward:
                next_index = current_index + 1
                self.XP_Ganados += 1
                self.progress_bar.increment_page()
            else:
                next_index = current_index - 1
                self.XP_Ganados -= 1
                self.progress_bar.decrement_page()
            # Antes de cambiar de página, añadimos un punto y log para debug.
            self.stacked_widget.setCurrentIndex(next_index)  # Cambiar a la siguiente página
            self.log_part_change()  # Registrar el cambio a la "Parte 1"

            current_page_type = self.stacked_widget.currentWidget().page_type.lower()  # Obtener el tipo de página actualizado
            self.log_event(
                f"{current_page_type.capitalize()} Page Open Time")  # Registrar el evento de apertura de la nueva página

            if current_page_type == "pedagogical" or current_page_type == "pedagogical2":
                self.SubmitHideContinueShow(True,
                                            False)  # Si la nueva página es una pregunta, mostrar el botón de envío y ocultar el botón de continuar
            elif current_page_type == "practica":
                self.SubmitHideContinueShow(False,
                                            True)  # Si la nueva página no es una pregunta, y es práctica, ocultar el botón de envío y el de continuar, y mostrar el de practica
            else:
                self.SubmitHideContinueShow(False,
                                            False)  # Si la nueva página no es una pregunta, ocultar el botón de envío y mostrar el botón de continuar

        # Sí se alcanza el final del recorrido de páginas, guardar el registro y cerrar la aplicación
        elif not next_index < self.stacked_widget.count():
            self.save_log(log_type="time")
            self.save_log(log_type="mouse")
            self.XP_Ganados += 5  # 5 puntos por terminar la lección.
            print(f"Page switched. Total XP: {self.XP_Ganados}")
            self.close()

        else:
            print("¡La leccion no se completó, se cerró!.")
            self.close()

        self.current_page += 1  # Incrementar el número de la página actual


def M1_L3_Main():
    main_window = MainWindow(lesson_number=3)
    main_window.show()
    return main_window
