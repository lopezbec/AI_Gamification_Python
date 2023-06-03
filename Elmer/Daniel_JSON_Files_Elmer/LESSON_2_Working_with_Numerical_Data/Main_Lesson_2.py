import datetime
import json
import sys
import csv
import drag_drop
import re

from functools import partial
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QFont, QDrag
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QRadioButton, QButtonGroup, QSizePolicy
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager
from custom_console import CustomPythonConsole


class JsonLoader:
    @staticmethod
    def load_json_data(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def load_json_styles():
        with open("styles.json") as styles_file:
            styles = json.load(styles_file)
        return styles


class JsonWindow(QWidget):
    def __init__(self, filename, page_type,  json_number):
        super().__init__()
        self.data = None
        self.layout = None
        self.hint_label = None
        self.button_group = None
        self.radio_buttons = None
        self.blank_space_index = None
        self.original_hint_text = None
        self.filename = filename
        self.feedback_label = QLabel(self)
        self.page_type = page_type
        self.styles = JsonLoader.load_json_styles()
        self.json_number = json_number
        self.init_ui()

    def title(self):
        title = QLabel(self.data[self.page_type.lower()][0]["title"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"background-color: {self.styles['title_background_color']}; color: {self.styles['title_text_color']}; border: 2px solid {self.styles['title_border_color']}")
        title_font = QFont()
        title_font.setPointSize(self.styles["font_size_titles"])
        title.setFont(title_font)
        self.layout.addWidget(title)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.data = JsonLoader.load_json_data(self.filename)
        self.title()

        if self.page_type.lower() == "multiplechoice":
            self.create_multiple_choice_layout_radioButtons()
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
        self.setLayout(self.layout)

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

    def createResetBottom(self):
        # Add a reset button to the layout
        reset_button = QPushButton('Reiniciar')
        reset_button.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white; border: 1px solid black; padding: 5px; border-radius: 5px")
        self.layout.addWidget(reset_button)
        reset_button.clicked.connect(self.reset_drag_and_drop)

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

    def create_multiple_choice_layout_radioButtons(self):
        self.radio_buttons = []
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
            radio_button = QRadioButton(answer["text"])
            radio_button.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white")
            self.radio_buttons.append(radio_button)
            self.button_group.addButton(radio_button, idx)
            answers_layout.addWidget(radio_button)  # Agregar al layout horizontal en lugar del vertical

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

    def reset_drag_and_drop(self):
        # Remove all current widgets from the layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Call the function that creates the initial layout again
        self.title()
        print(self.page_type.lower())
        if self.page_type.lower() == "draganddrop":
            self.create_drag_and_drop_layout()
        elif self.page_type.lower() == "multiplechoice":
            self.create_multiple_choice_plus_layout_radioButtons()
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
    def __init__(self, lesson_number=1):
        super().__init__()
        self.layout = None
        self.current_part = None
        self.button_layout = None
        self.submit_button = None
        self.stacked_widget = None
        self.python_console = None
        self.practice_button = None
        self.continue_button = None
        self.last_json_number = None
        self.python_console_widget = None
        self.styles = JsonLoader.load_json_styles()
        self.lesson_number = lesson_number
        self.log_data = []
        self.click_data = []
        self.time_log_data = []
        self.mouse_log_data = []
        self.init_ui()
        self.current_page = 0
        self.total_pages = 0

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setStyleSheet(f"background-color: {self.styles['main_background_color']}")
        self.stacked_widget = QStackedWidget()

        for page in self.load_page_order():
            if page["type"] == "JsonWindow":
                json_window = JsonWindow(page["filename"], page["page_type"], page["json_number"])
                self.stacked_widget.addWidget(json_window)

        self.log_event(f"{self.stacked_widget.currentWidget().page_type.capitalize()} Page Open Time", True)

        self.continue_button = QPushButton("Continuar")
        self.continue_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        continue_button_font = QFont()
        continue_button_font.setPointSize(self.styles["font_size_buttons"])
        self.continue_button.setFont(continue_button_font)
        self.continue_button.clicked.connect(self.switch_page)

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
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.practice_button)
        self.button_layout.addWidget(self.continue_button)

        self.layout.addWidget(self.stacked_widget)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.showMaximized()

    def SubmitAnswers(self, NoSeleciona, Correcto, Incorrecto):
        current_widget = self.stacked_widget.currentWidget()

        if NoSeleciona:
            current_widget.feedback_label.setText("No se ha seleccionado ninguna respuesta")
            current_widget.feedback_label.setStyleSheet(f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")
        elif Correcto:
            current_widget.feedback_label.setText("Respuesta correcta")
            current_widget.feedback_label.setStyleSheet(f"color: {self.styles['correct_color']}; font-size: {self.styles['font_size_answers']}px")
            self.SubmitHideContinueShow(True, False)
        elif Incorrecto:
            current_widget.feedback_label.setText("Respuesta incorrecta. Por favor, inténtalo de nuevo.")
            current_widget.feedback_label.setStyleSheet(f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")
        else:
            current_widget.feedback_label.setText("Respuesta incompleta, vuelve a intentarlo.")
            current_widget.feedback_label.setStyleSheet(f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")

    def open_python_console(self):
        self.SubmitHideContinueShow(True, False)

    def SubmitHideContinueShow(self, pedagogical, practica):
        if pedagogical: self.submit_button.hide(), self.practice_button.hide(), self.continue_button.show()
        elif practica: self.submit_button.hide(), self.practice_button.show(), self.continue_button.hide()
        else: self.submit_button.show(), self.practice_button.hide(), self.continue_button.hide()

    def log_event(self, event, event_type="time"):
        event_time = datetime.datetime.now().strftime("%H:%M:%S")
        json_number = self.stacked_widget.currentWidget().json_number

        # Si la parte cambia, agrega la entrada de "Parte X"
        if not hasattr(self, 'current_part') or self.current_part != json_number:
            self.current_part = json_number
            if event_type == "mouse": self.mouse_log_data.append({"event": f"Parte {self.current_part}", "time": event_time})
            else: self.time_log_data.append({"event": f"Parte {self.current_part}", "time": event_time})
            return  # Evita que se registre el mismo evento dos veces

        # Añadir el evento y su hora al registro de datos (log_data)
        if event_type == "mouse": self.mouse_log_data.append({"event": event, "time": event_time})
        else: self.time_log_data.append({"event": event, "time": event_time})

    def save_log(self, log_type="time"):
        fieldnames = ['event', 'time']
        filename = "Time_Lesson_2.csv" if log_type == "time" else "Entradas_Salidas_Clics_Lesson_2.csv"
        log_data = self.time_log_data if log_type == "time" else self.mouse_log_data

        with open(filename, mode="a", newline="") as csv_file:
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
        json_number = current_widget.json_number

        if hasattr(self, 'last_json_number') and self.last_json_number != json_number: self.log_event(f"Parte {json_number}", "mouse")
        self.last_json_number = json_number

        if current_page_type == "multiplechoice":
            selected_answer_id = current_widget.button_group.checkedId()
            if selected_answer_id != -1:
                correct_answer_id = None
                for idx, answer in enumerate(current_widget.data[current_page_type][0]["answers"]):
                    if answer["correct"]:
                        correct_answer_id = idx
                        break

                selected_answer_text = current_widget.data[current_page_type][0]["answers"][selected_answer_id]["text"]
                if selected_answer_id == correct_answer_id:
                    current_widget.feedback_label.setText("Respuesta correcta")
                    current_widget.feedback_label.setStyleSheet(f"color: {self.styles['correct_color']}; font-size: {self.styles['font_size_answers']}px")
                    self.log_event(f"{selected_answer_text} (Correcto)", event_type="mouse")  # Registrar la respuesta correcta como "Correcto"
                    self.SubmitHideContinueShow(True, False)

                else:
                    current_widget.feedback_label.setText("Respuesta incorrecta. Por favor, inténtalo de nuevo.")
                    current_widget.feedback_label.setStyleSheet(f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size_answers']}px")
                    self.log_event(f"{selected_answer_text} (Incorrecto)", event_type="mouse")  # Registrar la respuesta incorrecta como "Incorrecto"
            else:
                self.SubmitAnswers(True, False, False)

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

                    # Check if the question requires multiple responses
                    if data_block.get("multipleResponses"):
                        correct_order = None

                        # Verify if the "correctOrder" field exists
                        if "correctOrder" in data_block:
                            correct_order = data_block["correctOrder"]

                        if correct_order:
                            # Check the correct order against the texts dropped into the drop label
                            if correct_order == dropped_texts:
                                correct_count += 1

                    else:
                        # For questions requiring only one response, the original check is performed
                        correct_answer = None

                        for option in data_block["answers"]:
                            if option["correct"] and (label_type is None or option.get("correctType") == label_type):
                                correct_answer = option
                                break

                        if correct_answer:
                            if correct_answer["text"] in dropped_texts[0]:
                                correct_count += 1

            else:

                for label in drop_labels:
                    dropped_text = label.drop_area.text()
                    label_type = label.question_type

                    if "____" in dropped_text or "_" in dropped_text:
                        unanswered += 1
                        continue

                    correct_answer = None
                    for option in data_block["answers"]:
                        if option["correct"] and (label_type is None or option.get("correctType") == label_type):
                            correct_answer = option
                            break

                    if correct_answer:
                        if correct_answer["text"] in dropped_text:
                            correct_count += 1
                            self.log_event(f"{dropped_text} (Correcto)", event_type="mouse")  # Registrar la respuesta correcta como "Correcto"

                        else:
                            self.log_event(f"{dropped_text} (Incorrecto)", event_type="mouse")  # Registrar la respuesta incorrecta como "Incorrecto"

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

            current_hint_text = current_widget.hint_label.text()
            selected_symbol = current_hint_text[current_widget.blank_space_index]
            if selected_symbol == "_":
                self.SubmitAnswers(True, False, False)

            elif selected_symbol == correct_answer_text:
                self.SubmitAnswers(False, True, False)

            else:
                self.SubmitAnswers(False, False, True)

    def switch_page(self):
        current_page_type = self.stacked_widget.currentWidget().page_type.lower()  # Obtener el tipo de página actual
        self.log_event(f"{current_page_type.capitalize()} Page Close Time")  # Registrar el evento de cierre de la página actual
        next_index = self.stacked_widget.currentIndex() + 1  # Calcular el índice de la siguiente página

        # Si el siguiente índice es menor que el número total de páginas, continuar navegando
        if next_index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(next_index)  # Cambiar a la siguiente página
            current_page_type = self.stacked_widget.currentWidget().page_type.lower()  # Obtener el tipo de página actualizado
            self.log_event(f"{current_page_type.capitalize()} Page Open Time")  # Registrar el evento de apertura de la nueva página

            if current_page_type == "pedagogical" or current_page_type == "pedagogical2": self.SubmitHideContinueShow(True, False) # Si la nueva página es una pregunta, mostrar el botón de envío y ocultar el botón de continuar
            elif current_page_type == "practica": self.SubmitHideContinueShow(False, True)  # Si la nueva página no es una pregunta, y es práctica, ocultar el botón de envío y el de continuar, y mostrar el de practica
            else: self.SubmitHideContinueShow(False, False) # Si la nueva página no es una pregunta, ocultar el botón de envío y mostrar el botón de continuar
        # Sí se alcanza el final del recorrido de páginas, guardar el registro y cerrar la aplicación
        else:
            self.save_log(log_type="time")
            self.save_log(log_type="mouse")
            self.close()
        self.current_page += 1 # Incrementar el número de la página actual


def main():
    app = QApplication(sys.argv) # Crear una instancia de QApplication
    main_window = MainWindow(lesson_number=2)  # Aquí puedes cambiar el número de lecciones que deseas cargar
    sys.exit(app.exec()) # Ejecutar el bucle de eventos de la aplicación


if __name__ == '__main__':
    main() # Llamar a la función principal si el script se ejecuta como el programa principal
