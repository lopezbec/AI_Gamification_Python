import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QButtonGroup, \
    QCheckBox, QRadioButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from drag_drop import DraggableLabel, DropLabel


class JsonLoader:
    @staticmethod
    def load_json_data(filename):
        try:
            if not os.path.isfile(filename):
                raise FileNotFoundError(f"Archivo no encontrado: {filename}")
            with open(filename, encoding='UTF-8') as json_file:
                data = json.load(json_file)
            return data
        except Exception as e:
            print(f"Error al cargar el archivo JSON: {e}")
            return None

    @staticmethod
    def load_json_styles():
        try:
            styles_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.json")
            with open(styles_path, encoding='UTF-8') as styles_file:
                styles = json.load(styles_file)
            return styles
        except Exception as e:
            print(f"Error al cargar el archivo styles.json: {e}")
            return {}


class Main_Modulos_Quizzes_Window(QWidget):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.data = JsonLoader.load_json_data(filename)
        self.styles = JsonLoader.load_json_styles()
        self.page_type = self.detect_page_type()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        if not self.data:
            error_label = QLabel("Error al cargar el archivo JSON. Por favor, verifica que el archivo exista y sea válido.")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: red; font-size: 16px")
            self.layout.addWidget(error_label)
            self.setLayout(self.layout)
            return

        title = QLabel(self.data[self.page_type][0]["title"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            f"background-color: {self.styles['title_background_color']}; color: {self.styles['title_text_color']}; border: 2px solid {self.styles['title_border_color']}")
        title_font = QFont()
        title_font.setPointSize(self.styles["font_size_titles"])
        title.setFont(title_font)
        self.layout.addWidget(title)

        if self.page_type == 'multiplechoice':
            self.create_multiple_choice_layout()
        elif self.page_type == 'completeblankspace':
            self.create_complete_blank_space_layout()
        elif self.page_type == 'draganddrop':
            self.create_drag_and_drop_layout()

        self.create_feedback_label()

        self.submit_button = QPushButton('Enviar')
        self.submit_button.setStyleSheet(
            f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
        self.submit_button.clicked.connect(self.check_answers)
        self.layout.addWidget(self.submit_button)

        self.reset_button = QPushButton('Reiniciar')
        self.reset_button.setStyleSheet(
            f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
        self.reset_button.clicked.connect(self.reset_layout)
        self.layout.addWidget(self.reset_button)

        self.continue_button = QPushButton('Continuar')
        self.continue_button.setStyleSheet(
            f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
        self.continue_button.clicked.connect(self.close_quiz)
        self.continue_button.setVisible(False)  # Oculto por defecto
        self.layout.addWidget(self.continue_button)

        self.setLayout(self.layout)

    def detect_page_type(self):
        if 'multiplechoice' in self.data:
            return 'multiplechoice'
        elif 'completeblankspace' in self.data:
            return 'completeblankspace'
        elif 'draganddrop' in self.data:
            return 'draganddrop'
        else:
            raise ValueError("Tipo de página no soportado en el archivo JSON")

    def create_feedback_label(self):
        self.feedback_label = QLabel('')
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.feedback_label)

    def create_multiple_choice_layout(self):
        self.button_widgets = []
        self.button_group = QButtonGroup()

        answers_layout = QHBoxLayout()

        for block in self.data['multiplechoice'][0]['blocks']:
            block_type = block['type']
            block_label = QLabel(block['text'])
            block_label.setWordWrap(True)
            block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
            if block["type"] == "Consola":
                block_label.setStyleSheet(
                    f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
            self.layout.addWidget(block_label)

        for answer in self.data['multiplechoice'][0]['answers']:
            button_widget = QRadioButton(answer["text"])
            button_widget.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white")
            self.button_widgets.append(button_widget)
            self.button_group.addButton(button_widget)
            answers_layout.addWidget(button_widget)

        self.layout.addLayout(answers_layout)

    def create_complete_blank_space_layout(self):
        self.blank_space_index = -1
        self.original_hint_text = ""

        for block in self.data['completeblankspace'][0]['blocks']:
            block_type = block['type']
            if block_type == "info":
                block_label = QLabel(block["text"])
                block_label.setWordWrap(True)
                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)
            elif block_type == "Consola":
                self.hint_label = QLabel(block["text"])
                self.hint_label.setWordWrap(True)
                self.hint_label.setStyleSheet(
                    f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(self.hint_label)
                self.original_hint_text = block['text']

        answers_layout = QHBoxLayout()

        for answer in self.data['completeblankspace'][0]['answers']:
            answer_button = QPushButton(answer["text"])
            answer_button.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white")
            answer_button.clicked.connect(lambda checked, text=answer["text"]: self.handle_answer_click(text))
            answers_layout.addWidget(answer_button)

        self.layout.addLayout(answers_layout)

    def create_drag_and_drop_layout(self):
        drop_labels = {}
        data_block = self.data['draganddrop'][0]

        if "draganddropSecuence" in data_block and data_block["draganddropSecuence"]:
            for block in data_block["blocks"]:
                block_type = block["type"]

                if "correctOrder" in data_block:
                    multiple_drops = len(data_block["correctOrder"]) > 1
                else:
                    multiple_drops = False

                if block_type == "Consola":
                    drop_labels[block_type] = DropLabel(block["text"], self.styles, question_type=block_type, multiple=multiple_drops)
                    block_label = drop_labels[block_type]
                else:
                    block_label = QLabel(block["text"])
                    block_label.setWordWrap(True)

                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)

        else:
            for block in data_block["blocks"]:
                block_type = block["type"]

                if "correctValue" in block or "correctOrder" in data_block:
                    multiple_drops = "correctOrder" in data_block and len(data_block["correctOrder"]) > 1
                    drop_labels[block_type] = DropLabel(block["text"], self.styles, question_type=block_type, multiple=multiple_drops)
                    block_label = drop_labels[block_type]
                elif block_type == "Consola":
                    block_label = DropLabel(block["text"], self.styles)
                else:
                    block_label = QLabel(block["text"])
                    block_label.setWordWrap(True)

                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)

        draggable_labels_layout = QHBoxLayout()
        draggable_labels_layout.setSpacing(50)

        for answer in data_block["answers"]:
            draggable_label = DraggableLabel(answer["text"])
            draggable_label.setStyleSheet(
                f"font-size: {self.styles['font_size_normal']}px; background-color: white; border: 1px solid black; padding: 5px; border-radius: 5px")
            draggable_labels_layout.addWidget(draggable_label)

        self.layout.addLayout(draggable_labels_layout)

    def handle_answer_click(self, answer_text):
        current_text = self.hint_label.text()
        new_text = current_text.replace("___", answer_text, 1)
        self.hint_label.setText(new_text)

    def check_answers(self):
        if self.page_type == 'draganddrop':
            self.check_drag_and_drop_answers()
        elif self.page_type == 'multiplechoice':
            self.check_multiple_choice_answers()
        elif self.page_type == 'completeblankspace':
            self.check_complete_blank_space_answers()

    def check_drag_and_drop_answers(self):
        drop_labels = self.findChildren(DropLabel)
        correct_order = self.data['draganddrop'][0]['correctOrder']
        user_order = []

        for label in drop_labels:
            user_order.extend(label.dropped_texts)

        if user_order == correct_order:
            self.feedback_label.setText('¡Correcto!')
            self.feedback_label.setStyleSheet(f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            self.submit_button.setVisible(False)
            self.continue_button.setVisible(True)  # Mostrar botón "Continuar" si la respuesta es correcta
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")

    def check_multiple_choice_answers(self):
        selected_answers = [btn.text() for btn in self.button_widgets if btn.isChecked()]
        correct_answers = [answer["text"] for answer in self.data['multiplechoice'][0]["answers"] if answer.get("correct", False)]

        if selected_answers == correct_answers:
            self.feedback_label.setText('¡Correcto!')
            self.feedback_label.setStyleSheet(f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            self.submit_button.setVisible(False)
            self.continue_button.setVisible(True)  # Mostrar botón "Continuar" si la respuesta es correcta
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")

    def check_complete_blank_space_answers(self):
        user_text = self.hint_label.text()
        correct_text = self.original_hint_text.replace("___", self.data['completeblankspace'][0]["correctValue"])

        if user_text == correct_text:
            self.feedback_label.setText('¡Correcto!')
            self.feedback_label.setStyleSheet(f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            self.submit_button.setVisible(False)
            self.continue_button.setVisible(True)  # Mostrar botón "Continuar" si la respuesta es correcta
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")

    def reset_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        title = QLabel(self.data[self.page_type][0]["title"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            f"background-color: {self.styles['title_background_color']}; color: {self.styles['title_text_color']}; border: 2px solid {self.styles['title_border_color']}")
        title_font = QFont()
        title_font.setPointSize(self.styles["font_size_titles"])
        title.setFont(title_font)
        self.layout.addWidget(title)

        if self.page_type == 'multiplechoice':
            self.create_multiple_choice_layout()
        elif self.page_type == 'completeblankspace':
            self.create_complete_blank_space_layout()
        elif self.page_type == 'draganddrop':
            self.create_drag_and_drop_layout()

        self.create_feedback_label()

        self.submit_button = QPushButton('Enviar')
        self.submit_button.setStyleSheet(
            f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
        self.submit_button.clicked.connect(self.check_answers)
        self.layout.addWidget(self.submit_button)

        self.reset_button = QPushButton('Reiniciar')
        self.reset_button.setStyleSheet(
            f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
        self.reset_button.clicked.connect(self.reset_layout)
        self.layout.addWidget(self.reset_button)

        self.continue_button = QPushButton('Continuar')
        self.continue_button.setStyleSheet(
            f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
        self.continue_button.clicked.connect(self.close_quiz)
        self.continue_button.setVisible(False)  # Oculto por defecto
        self.layout.addWidget(self.continue_button)

        self.setLayout(self.layout)

    def close_quiz(self):
        self.close()


