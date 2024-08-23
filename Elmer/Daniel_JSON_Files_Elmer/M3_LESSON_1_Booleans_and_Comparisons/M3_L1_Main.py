import re
import os
import sys
import csv
import json
import datetime
import drag_drop as drag_drop

from functools import partial
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from game_features.progress_bar import ProgressBar
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard, get_instance
from PyQt6.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QStackedWidget, QRadioButton, QButtonGroup, QCheckBox
from Main_Modulos_Intro_Pages import MainWindow as Dashboard
from badge_system.badge_criteria_streak import BadgeCriteriaStreak, reset_streak, \
read_stored_streak, update_streak, check_streak_badges
from badge_system.badge_verification import BadgeVerification, get_badge_level, is_badge_earned, \
        update_lesson_dates, are_lessons_completed_same_day, are_two_lessons_completed_same_day, display_badge, \
            update_badge_progress, are_three_modules_completed, update_lesson_status, check_module_streak_per_user
from badge_system.display_cabinet import BadgeDisplayCabinet
from command_line_UI import App
from congratulation_Feature import CongratulationWindow

class JsonLoader:
    @staticmethod
    def load_json_data(filename):
        try:
            with open(filename, encoding='UTF-8') as json_file:
                data = json.load(json_file)
            return data
        except Exception as e:
            print(f"Error load_json_data linea {sys.exc_info()[2].tb_lineno}")

    @staticmethod
    def load_json_styles():
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "styles.json")) as styles_file:
            styles = json.load(styles_file)
        return styles
    
    @staticmethod
    def load_active_widgets():
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "active_widgets", "game_elements_visibility.json")) as active_widgets:
            widgets = json.load(active_widgets)
        return widgets


class JsonWindow(QWidget):
    def __init__(self, filename, page_type, json_number, xp_ganados, user_score, lesson_completed, main_window=None, usuario_actual=None):
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
        self.display_cabinet = None
        self.main_window = main_window
        self.user_score = user_score
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
        self.usuario_actual = usuario_actual
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.data = JsonLoader.load_json_data(self.filename)

        # Crear un nuevo layout horizontal
        hlayout = QHBoxLayout()

        # Crear el widget de puntos
        self.puntos = QLabel(f"XP ganados: {self.user_score + self.XP_Ganados}")
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
        self.leaderboard_button.clicked.connect(self.abrir_leaderboard)

        #boton para Vitrina (display cabinet)
        self.display_cabinet = QPushButton("Mis insignias")
        self.display_cabinet.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        display_cabinet_font = QFont()
        display_cabinet_font.setPointSize(self.styles['font_size_buttons'])
        self.display_cabinet.setFont(display_cabinet_font)
        self.display_cabinet.clicked.connect(self.abrir_display_cabinet)

        # Añadir los widgets al layout horizontal
        if JsonLoader.load_active_widgets().get("points", True):
            hlayout.addWidget(self.puntos)
        if JsonLoader.load_active_widgets().get("Leaderboard", True):
            hlayout.addWidget(self.leaderboard_button)
        if JsonLoader.load_active_widgets().get("display_cabinet", True):
            hlayout.addWidget(self.display_cabinet)

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
            print(
                "Lo siento no se encontró el tipo de página especificada, O el tipo de página que se especificó no se ha configurado su lógica todavía. Configurar la lógica y ponerla aquí.")

        # Establecer el layout en el QWidget
        self.setWindowTitle('JsonWindow')
        self.setLayout(self.layout)

    def get_current_hint_text(self):
        return self.hint_label.text()

    @staticmethod
    def get_lesson_number(filename):
        base = os.path.basename(filename)  # Obtén el nombre del archivo con la extensión
        lesson_number = os.path.splitext(base)[0][-1]  # Elimina la extensión y toma el último carácter
        return int(lesson_number)  # Convierte el número de lecciones a un entero

    def update_points(self, new_points):
        if self.main_window is not None:
            self.main_window.update_xp(new_points)

    def update_points_display(self, new_points):
        self.puntos.setText(f"XP ganados: {self.user_score + new_points}")
    
    def abrir_display_cabinet(self):
        self.display_cabinet = BadgeDisplayCabinet(self.usuario_actual)
        self.display_cabinet.show()

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

    def handle_answer_click(self, answer_text, original_hint_text):
        # Restablece el texto a su estado original
        self.hint_label.setText(original_hint_text)

        current_text = self.hint_label.text()
        # Reemplaza los primeros cuatro guiones bajos encontrados por la respuesta seleccionada
        new_text = current_text.replace("____", answer_text, 1)
        self.hint_label.setText(new_text)

        # Actualizar el estado del texto actual
        self.current_text_state = new_text

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
            answer_button.clicked.connect(partial(self.handle_answer_click, answer["text"], self.original_hint_text))
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
                    drop_labels[block_type] = drag_drop.DropLabel(block["text"], self.styles, question_type=block_type,
                                                                  multiple=multiple_drops)
                    block_label = drop_labels[block_type]
                else:
                    block_label = QLabel(block["text"])

                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)

        else:

            for idx, block in enumerate(data_block["blocks"]):
                block_type = block["type"]

                if "correctValue" in block or "correctOrder" in data_block:
                    multiple_drops = "correctOrder" in data_block and len(data_block["correctOrder"]) > 1
                    drop_labels[block_type] = drag_drop.DropLabel(block["text"], self.styles, question_type=block_type, multiple=multiple_drops)
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

        # Reiniciar la visualización de los puntos XP
        self.update_points_display(self.main_window.XP_Ganados)

       # Recrear los widgets y layouts
        # Añadir el layout de puntos y leaderboard de nuevo
        hlayout = QHBoxLayout()
        if JsonLoader.load_active_widgets().get("points", True):
            hlayout.addWidget(self.puntos)
        if JsonLoader.load_active_widgets().get("Leaderboard", True):
            hlayout.addWidget(self.leaderboard_button)
        if JsonLoader.load_active_widgets().get("display_cabinet", True):
            hlayout.addWidget(self.display_cabinet)
        self.layout.addLayout(hlayout)

        # Restablecer el contenido del JsonWindow según el tipo de página
        self.title()
        if self.page_type.lower() == "draganddrop":
            self.create_drag_and_drop_layout()
        elif self.page_type.lower() == "multiplechoice":
            self.create_multiple_choice_layout(
                is_multiple_choice_plus=self.data[self.page_type.lower()][0].get("multiplechoiceplus", False))
        elif self.page_type.lower() == "completeblankspace":
            self.create_complete_blank_space_layout()
        elif self.page_type.lower() == "pedagogical" or self.page_type.lower() == "pedagogical2":
            self.create_pedagogical_layout()
        else:
            # Otros tipos de página según sea necesario
            print("No existe lógica para ese tipo de página.")

        # Restablecer y mostrar la etiqueta de feedback
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
        # Variable para acumular el texto de bloques "info".
        accumulated_info_text = ""

        for block in self.data[self.page_type.lower()][0]["blocks"]:
            # Si el bloque es de tipo "info", acumula su texto.
            if block["type"] == "info":
                accumulated_info_text += block["text"] + "\n\n"

            # Si el bloque es de tipo "Consola", procede como antes.
            elif block["type"] == "Consola":
                # Si hay texto acumulado de "info", créalo como QLabel antes del contenido de "Consola".
                if accumulated_info_text:
                    info_label = QLabel(accumulated_info_text.strip())
                    info_label.setWordWrap(True)
                    info_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px;")
                    self.layout.addWidget(info_label)
                    accumulated_info_text = ""  # Restablece el texto acumulado.

                # Crea los widgets de "Consola" como antes.
                console_frame = QFrame()
                console_frame.setStyleSheet(f"background-color: {self.styles['cmdExe_background_color']};")
                console_layout = QVBoxLayout(console_frame)
                console_layout.setContentsMargins(5, 5, 5, 5)
                console_label = QLabel(block["text"])
                console_label.setStyleSheet(
                    f"color: {self.styles['cmdExe_text_color']}; font-size: {self.styles['font_size_normal']}px;")
                console_label.setWordWrap(True)
                console_layout.addWidget(console_label)

                # Botón que desencadenará la adición del widget de la clase 'App'.
                self.execute_button = QPushButton("Haz clic para ejecutar")
                self.execute_button.setStyleSheet(
                    "background-color: orange; font-size: {self.styles['font_size_normal']}px; color: white;")
                self.execute_button.clicked.connect(lambda: self.openCommandLineUI(block["text"]))

                console_layout.addWidget(self.execute_button)
                self.layout.addWidget(console_frame)

            # Maneja los otros tipos de bloques como antes.
            else:
                block_label = QLabel(block["text"])
                block_label.setWordWrap(True)
                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px;")
                if block["type"] == "hint":
                    block_label.setStyleSheet(
                        f"border: {self.styles['hint_border_width']}px solid {self.styles['hint_border_color']}; background-color: {self.styles['hint_background_color']}; font-size: {self.styles['font_size_normal']}px;")
                self.layout.addWidget(block_label)

        # Si queda algún texto de "info" después de procesar todos los bloques, créalo como QLabel al final.
        if accumulated_info_text:
            info_label = QLabel(accumulated_info_text.strip())
            info_label.setWordWrap(True)
            info_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px;")
            self.layout.addWidget(info_label)

        # Crea un contenedor para el widget de la clase 'App' que será añadido al hacer clic en el botón.
        self.commandLineWidgetPlaceholder = QVBoxLayout()
        self.layout.addLayout(self.commandLineWidgetPlaceholder)

    def openCommandLineUI(self, text):
        self.main_window.log_event("Playground Page Open", event_type="time")
        # Verificar si el widget ya ha sido creado y, si no, crearlo y añadirlo al layout.
        if not hasattr(self, 'commandLineWidget'):
            # Suponiendo que 'App' es una subclase de QWidget
            self.commandLineWidget = App(current_user=self.usuario_actual)
            self.commandLineWidgetPlaceholder.addWidget(self.commandLineWidget)

            # Crear botón para ocultar el widget de la línea de comandos
            self.hideButton = QPushButton("Ocultar")
            self.hideButton.setStyleSheet(
                "background-color: orange; font-size: {self.styles['font_size_normal']}px; color: white;")
            self.hideButton.clicked.connect(self.hideCommandLineWidget)
            self.commandLineWidgetPlaceholder.addWidget(self.hideButton)
            self.execute_button.hide()

        # Si el widget ya existe, mostrarlo si está oculto
        else:
            self.commandLineWidget.show()
            self.hideButton.show()
            self.execute_button.hide()

    def hideCommandLineWidget(self):
        self.main_window.log_event("Playground Page Close", event_type="time")
        # Esta función oculta el widget de la línea de comandos y el botón de ocultar.
        self.commandLineWidget.hide()
        self.hideButton.hide()
        self.execute_button.show()


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
        self.highest_page_reached = 0
        self.is_rollback = False
        self.lesson_number = lesson_number
        self.lesson_finished_successfully = False
        self.styles = JsonLoader.load_json_styles()
        self.usuario_actual = self.load_current_user()
        self.leaderboard_window_instace = get_instance()
        self.streak = BadgeCriteriaStreak() #para manejar la racha de respuestas correctas
        self.all_correct = True
        self.setWindowTitle("Booleanos y comparaciones")
        self.progress_bar = ProgressBar(
            JsonLoader.load_json_data(
                 os.path.join(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))), "Page_order", "page_order_M3.json")
                )
                , 0)
        self.user_score = self.leaderboard_window_instace.get_current_user_score() #puntos ganados por el jugador en todo el juego (acumulativo)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setStyleSheet(f"background-color: {self.styles['main_background_color']}")
        self.stacked_widget = QStackedWidget()

        for page in self.load_page_order():
            if page["type"] == "JsonWindow":
                json_window = JsonWindow(os.path.join(os.path.dirname(os.path.abspath(__file__)), page["filename"]), page["page_type"], page["json_number"], self.XP_Ganados, self.user_score, 
                                             page.get("lesson_completed", False), main_window=self, usuario_actual=self.usuario_actual)
                self.json_windows.append(json_window)
                self.stacked_widget.addWidget(json_window)

        self.log_part_change()
        self.log_event(f"{self.stacked_widget.currentWidget().page_type.capitalize()} Page Open Time", True)

        self.python_console_widget = QTextEdit(self)
        self.python_console_widget.setReadOnly(True)
        self.layout.addWidget(self.python_console_widget)
        self.python_console_widget.hide()

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

        self.terminar_button = QPushButton("Leccion Completada")
        self.terminar_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        terminar_button_font = QFont()
        terminar_button_font.setPointSize(self.styles["font_size_buttons"])
        self.terminar_button.setFont(continue_button_font)
        self.terminar_button.clicked.connect(self.Leccion_Terminada)
        self.terminar_button.hide()

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
        self.button_layout.addWidget(self.terminar_button)

        if JsonLoader.load_active_widgets().get("progress", True):
            self.layout.addWidget(self.progress_bar)  # Agrega la barra de progreso al layout
        self.layout.addWidget(self.stacked_widget)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.showMaximized()

    def Leccion_Terminada(self):
        self.close()

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
            CongratulationWindow.incorrect_response()
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
            self.streak.correct_answer()
            CongratulationWindow.correct_response()
        elif Incorrecto:
            self.controlador = True
            current_widget.feedback_label.setText("Respuesta incorrecta. Por favor, inténtalo de nuevo.")
            current_widget.feedback_label.setStyleSheet(
                f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")
            self.streak.incorrect_answer()
            reset_streak(self.usuario_actual)
            self.all_correct = False
            CongratulationWindow.incorrect_response()
        else:
            self.controlador = True
            current_widget.feedback_label.setText("Respuesta incompleta, vuelve a intentarlo.")
            current_widget.feedback_label.setStyleSheet(
                f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")
            CongratulationWindow.incorrect_response()

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

    def save_log(self, modulo, leccion):
        user = self.load_current_user()
        if user is None:
            print("Usuario no encontrado.")
            return

        filename = f"{user}_Respuestas_Tiempos.csv"
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        user_logs_dir = os.path.join(parent_dir, 'Usuarios_respuestas_lecciones')
        if not os.path.exists(user_logs_dir):
            os.makedirs(user_logs_dir)

        filepath = os.path.join(user_logs_dir, filename)

        fieldnames = ['event', 'time']
        with open(filepath, mode="a", newline="", encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'event': f"Modulo {modulo}, Leccion {leccion}", 'time': ''})

            # Escribe la cabecera si es un archivo nuevo
            if csv_file.tell() == 0:
                writer.writeheader()
                # Escribe el módulo y la lección al inicio
                csv_file.write(f"Modulo {modulo}, Leccion {leccion}\n")

            combined_log_data = self.time_log_data + self.mouse_log_data
            combined_log_data.sort(key=lambda x: x['time'])

            parte_actual = ""
            for log in combined_log_data:
                # Verifica si el evento es un inicio de "Parte X"
                if log['event'].startswith('Parte'):
                    if log['event'] == parte_actual:
                        # Omite la escritura si ya se registró el inicio de esta parte
                        continue
                    else:
                        # Actualiza la parte actual y escribe el evento
                        parte_actual = log['event']

                writer.writerow(log)

            csv_file.write('\n')

    def load_page_order(self):
        # Construir la ruta al archivo dentro de la carpeta 'Page_order'
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Page_order', 'page_order_M3.json')

        with open(file_path, "r") as file:
            data = json.load(file)

        for lesson in data["lessons"]:
            if lesson["lesson_number"] == self.lesson_number:
                return lesson["pages"]

        raise ValueError(f"Lesson {self.lesson_number} not found in page_order_M3.json")

    def submit_answer(self):
        current_widget = self.stacked_widget.currentWidget()
        current_page_type = current_widget.page_type.lower()

        if current_page_type == "multiplechoice":
            selected_answers = []  # Respuestas seleccionadas
            correct_answers = []  # Respuestas correctas
            # Iterar sobre los botones
            for idx, button in enumerate(current_widget.button_widgets):
                if button.isChecked():
                    selected_answers.append({"text": button.text(), "correct": current_widget.data[current_page_type][0]["answers"][idx]["correct"]})
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
            try:
                correct_answer_text = None

                for answer in current_widget.data[current_page_type][0]["answers"]:
                    if answer["correct"]:
                        correct_answer_text = answer["text"]
                        break

                # Extraer la respuesta del usuario del hint_label
                current_hint_text = current_widget.get_current_hint_text()
                selected_answer_start = current_widget.original_hint_text.find("____")
                selected_answer_end = selected_answer_start + len("____")  # la longitud de "____"
                selected_answer = current_hint_text[selected_answer_start:selected_answer_end]

                if selected_answer == "____":
                    self.log_event(f"Blank Space Selected", event_type="mouse")  # Log mouse event
                    self.SubmitAnswers(True, False, False)

                elif selected_answer == correct_answer_text:
                    self.log_event(f"Correct Answer Selected: {correct_answer_text}", event_type="mouse")  # Log mouse event
                    self.SubmitAnswers(False, True, False)

                else:
                    self.log_event(f"Incorrect Answer Selected: {selected_answer}", event_type="mouse")  # Log mouse event
                    self.SubmitAnswers(False, False, True)
            except Exception as e:
                print(f"Error {e}")

    def actualizar_progreso_usuario(self, modulo, leccion_completada):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'progreso.json'), 'r', encoding='UTF-8') as file:
                progreso = json.load(file)

            progreso_usuario = progreso.get(self.usuario_actual, {})

            # Calcula el número de la siguiente lección para desbloquearla en progreso.json
            numero_leccion_actual = int(leccion_completada.replace("Leccion", ""))
            siguiente_leccion = f'Leccion{numero_leccion_actual + 1}'

            if modulo in progreso_usuario:
                progreso_usuario[modulo][siguiente_leccion] = True  # Desbloquea la siguiente lección

            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'progreso.json'), 'w', encoding='UTF-8') as file:
                json.dump(progreso, file, indent=4)

        except Exception as e:
            print(f"Error al actualizar el progreso: {e}")

    def actualizar_leccion_completada(self, modulo, leccion_completada):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'leccion_completada.json'), 'r', encoding='UTF-8') as file:
                leccion_completada_data = json.load(file)

            leccion_completada_usuario = leccion_completada_data.get(self.usuario_actual, {})

            # Marca la lección actual como completada en leccion_completada.json
            if modulo not in leccion_completada_usuario:
                leccion_completada_usuario[modulo] = {}
            leccion_completada_usuario[modulo][f"Leccion_completada{leccion_completada.replace('Leccion', '')}"] = True

            leccion_completada_data[self.usuario_actual] = leccion_completada_usuario

            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'leccion_completada.json'), 'w', encoding='UTF-8') as file:
                json.dump(leccion_completada_data, file, indent=4)

        except Exception as e:
            print(f"Error al actualizar lección completada: {e}")

    @staticmethod
    def load_current_user():
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'current_user.json'), 'r', encoding='UTF-8') as file:
                user_data = json.load(file)
            return user_data.get("current_user")
        except FileNotFoundError:
            print("Archivo current_user.json no encontrado.")
            return None

    @staticmethod
    def actualizar_puntos_en_leaderboard(usuario, puntos_ganados):
        # Ruta al archivo leaderboard.json
        leaderboard_path =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigos_LeaderBoard', 'leaderboard.json')  

        try:
            with open(leaderboard_path, 'r', encoding='UTF-8') as file:
                leaderboard = json.load(file)

            usuario_existente = False
            for user in leaderboard:
                if user["name"] == usuario:
                    user["points"] += puntos_ganados
                    usuario_existente = True
                    break

            if not usuario_existente:
                # Si el usuario no existe en el leaderboard, añadirlo con los puntos iniciales
                leaderboard.append({"name": usuario, "points": puntos_ganados, "last_active": ""})

            with open(leaderboard_path, 'w', encoding='UTF-8') as file:
                json.dump(leaderboard, file, indent=4)

        except FileNotFoundError:
            print("Archivo leaderboard.json no encontrado.")

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
                self.update_highest_page(next_index)
                next_index = current_index + 1
                self.XP_Ganados += 1
                self.progress_bar.increment_page()
            else:
                self.is_rollback = True
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

            if not forward:
                self.submit_button.hide()
                self.continue_button.show()
                self.back_button.hide()

        # Sí se alcanza el final del recorrido de páginas, guardar el registro y cerrar la aplicación
        elif not next_index < self.stacked_widget.count():
            self.continue_button.hide()
            self.terminar_button.show()
            self.save_log(modulo=3, leccion=1)
            self.XP_Ganados += 5  # 5 puntos por terminar la lección.
            self.actualizar_puntos_en_leaderboard(self.usuario_actual, self.XP_Ganados)
            self.actualizar_progreso_usuario('Modulo3', 'Leccion1')
            self.actualizar_leccion_completada('Modulo3', 'Leccion1')
            update_lesson_status(self.usuario_actual, 'Modulo3', 'Leccion1', self.all_correct)
                        
            if self.streak.get_current_streak() > 0:
                update_streak(self.usuario_actual, self.streak.get_current_streak())
            #Badge verification correct anwers streak
            check_streak_badges(int(read_stored_streak(self.usuario_actual)), self.usuario_actual)
            get_badge_level(self, score=self.leaderboard_window_instace.get_current_user_score() + self.XP_Ganados)           
            update_lesson_dates(self.usuario_actual, "Modulo3", "Leccion_completada1")           
            if are_lessons_completed_same_day(self.usuario_actual, "Modulo3") and not is_badge_earned(self.usuario_actual, 'modulo_rapido'):
                    display_badge('modulo_rapido')
                    update_badge_progress(self.usuario_actual, 'modulo_rapido')
            if are_two_lessons_completed_same_day(self.usuario_actual, "Modulo3") and not is_badge_earned(self.usuario_actual, 'doble_aprendizaje'):
                display_badge('doble_aprendizaje')
                update_badge_progress(self.usuario_actual, 'doble_aprendizaje')
            if are_three_modules_completed(self.usuario_actual) and not is_badge_earned(self.usuario_actual, 'Explorador_curioso'):
                display_badge('Explorador_curioso')
                update_badge_progress(self.usuario_actual, 'Explorador_curioso')
            if check_module_streak_per_user(self.usuario_actual) and not is_badge_earned(self.usuario_actual, 'dominador_modulo'):
                display_badge('dominador_modulo')
                update_badge_progress(self.usuario_actual, 'dominador_modulo')
            self.close()

        else:
            print("¡La leccion no se completó, se cerró!.")
            self.close()

        if next_index == self.highest_page_reached and self.is_rollback == True:
                self.is_rollback = False
                #Llamar al método de reinicio con el tipo de página correspondiente
                self.json_windows[next_index].reset_button()

        self.current_page += 1  # Incrementar el número de la página actual

    def update_highest_page(self, current_page):
        if current_page > self.highest_page_reached:
            self.highest_page_reached = current_page

    def closeEvent(self, event):
        self.dashboard = Dashboard()
        self.dashboard.showMaximized()
        # Luego, cierra la ventana normalmente
        super().closeEvent(event)

def M3_L1_Main():
    main_window = MainWindow(lesson_number=1)
    main_window.show()
    return main_window
