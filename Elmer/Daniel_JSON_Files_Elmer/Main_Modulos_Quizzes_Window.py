import sys
import os
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QButtonGroup, \
    QRadioButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from drag_drop import DraggableLabel, DropLabel
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard
from Main_Modulos_Intro_Pages import MainWindow as Dashboard


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


class QuizLoader:
    def __init__(self, layout, styles, quiz_file, page_order_file, current_quiz_index, current_module_index, main_window):
        self.layout = layout
        self.styles = styles
        self.quiz_file = quiz_file
        self.page_order_file = page_order_file
        self.current_section_index = 0
        self.load_page_order()
        self.feedback_label = QLabel('')
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.feedback_label)
        self.current_user = self.load_current_user()
        self.current_quiz_index = current_quiz_index #Numero actual del quiz
        self.current_module_index = current_module_index #Numero actual del modulo
        self.main_window = main_window #Instancia actual del Main Modulo Quizzes Window
        self.section = None #declaracion de section como atributo de la clase
        self.page_type = None # declaracion de page type  como atributo de la clase

    def load_page_order(self):
        if not os.path.isfile(self.page_order_file):
            raise FileNotFoundError(f"Archivo no encontrado: {self.page_order_file}")
        with open(self.page_order_file, "r", encoding='UTF-8') as file:
            self.page_order = json.load(file)["quizzes"]
        self.current_section_in_quiz_index = 0

    def load_quiz_section(self):
        self.clear_layout()
        try:
            quiz_file_path = self.quiz_file
            if not os.path.isfile(quiz_file_path):
                raise FileNotFoundError(f"Archivo no encontrado: {quiz_file_path}")
            with open(quiz_file_path, "r", encoding='UTF-8') as file:
                quiz_data = json.load(file)

            # Realizar la búsqueda del quiz paso a paso
            matching_quizzes = [] #lista de los quizzes que cumplen las condiciones
            # Se itera sobre los elementos del page_order.json 
            for quiz in self.page_order:
                # revisa cada elemento del page order y se compara el numero de quiz y el numero del modulo 
                if int(quiz["module"]) == int(self.current_module_index) and int(quiz["quiz_number"]) == int(self.current_quiz_index):
                    # si se cumplen las condiciones se guarda en la lista
                    matching_quizzes.append(quiz)

            #si se encuentra uno o mas quizzes entonces se toma el primero de la lista
            if matching_quizzes:
                current_quiz = matching_quizzes[0]
            else:
                #en caso contrario lanzamos unn erorr de FileNotFoundError
                current_quiz = None
                raise FileNotFoundError("No se encontró ningún quiz que coincida con los números especificados.")
            
            #current_quiz es true (digase hay un quiz en esta variable)
            if current_quiz:
                # Verifica que el índice de la sección actual del quiz esté dentro de los límites de las secciones disponibles en el quiz actual.
                if 0 <= self.current_section_in_quiz_index < len(current_quiz["sections"]):                   
                    
                    # Obtiene la sección actual del quiz basado en el índice de la sección actual.
                    current_section = current_quiz["sections"][self.current_section_in_quiz_index]                   
                    # Extrae el tipo de página (page_type) de la sección actual.
                    page_type = current_section["page_type"]                   
                    # Extrae el número de sección (section_number) de la sección actual.
                    section_number = current_section["section_number"]                   
                    # Asigna la sección correspondiente en los datos del quiz usando page_type y section_number (el número de sección es 1-based).
                    self.section = quiz_data[page_type][section_number - 1]              
                    # Asigna el tipo de página actual a self.page_type para que pueda ser utilizado más adelante.
                    self.page_type = page_type

            if self.page_type not in quiz_data:
                raise KeyError(f"La clave '{self.page_type}' no existe en el JSON")

            if not quiz_data[self.page_type]:
                raise ValueError(f"La lista para la clave '{self.page_type}' está vacía")

            self.leaderboard_button = QPushButton("Leaderboard")
            self.leaderboard_button.setStyleSheet(
                f"background-color: {self.styles['continue_button_color']}; color: white; font-size: {self.styles['font_size_buttons']}px"
            )
            self.leaderboard_button.clicked.connect(self.abrir_leaderboard)
            self.layout.addWidget(self.leaderboard_button)

            section_data = self.section
            title = QLabel(section_data["title"])
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet(
                f"background-color: {self.styles['title_background_color']}; color: {self.styles['title_text_color']}; border: 2px solid {self.styles['title_border_color']}")
            title_font = QFont()
            title_font.setPointSize(self.styles["font_size_titles"])
            title.setFont(title_font)
            self.layout.addWidget(title)

            if self.page_type == 'multiplechoice':
                self.create_multiple_choice_layout(section_data)
            elif self.page_type == 'completeblankspace':
                self.create_complete_blank_space_layout(section_data)
            elif self.page_type == 'draganddrop':
                self.create_drag_and_drop_layout(section_data)

            self.create_feedback_label()

            button_layout = QHBoxLayout()

            self.submit_button = QPushButton('Enviar')
            self.submit_button.setStyleSheet(
                f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
            self.submit_button.clicked.connect(self.check_answers)
            button_layout.addWidget(self.submit_button)

            self.reset_button = QPushButton('Reiniciar')
            self.reset_button.setStyleSheet(
                f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
            self.reset_button.clicked.connect(self.reset_layout)
            button_layout.addWidget(self.reset_button)

            self.continue_button = QPushButton('Continuar')
            self.continue_button.setStyleSheet(
                f"background-color: {self.styles.get('continue_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
            self.continue_button.clicked.connect(self.load_next_section)
            self.continue_button.setVisible(False)
            button_layout.addWidget(self.continue_button)

            self.complete_button = QPushButton('Completar')
            self.complete_button.setStyleSheet(
                f"background-color: {self.styles.get('complete_button_color', '#4CAF50')}; color: white; font-size: {self.styles.get('font_size_buttons', 12)}px")
            self.complete_button.clicked.connect(self.complete_quiz)
            self.complete_button.setVisible(False)
            button_layout.addWidget(self.complete_button)

            self.layout.addLayout(button_layout)
        except KeyError as e:
            print(f"Error al acceder a una clave en el JSON: {e}")
        except ValueError as e:
            print(f"Error de valor: {e}")
        except Exception as e:
            print(f"Error al cargar la sección: {e}")

    def load_next_section(self):
        self.current_section_in_quiz_index += 1
        current_quiz = self.page_order[self.current_quiz_index - 1]
        if self.current_section_in_quiz_index >= len(current_quiz["sections"]):
            self.current_quiz_index += 1
            self.current_section_in_quiz_index = 0
            if self.current_quiz_index >= len(self.page_order):
                self.submit_button.setVisible(False)
                self.reset_button.setVisible(False)
                self.continue_button.setVisible(False)
                self.complete_button.setVisible(True)
                return
        self.clear_layout()
        self.load_quiz_section()

    def complete_quiz(self):
        self.mark_quiz_complete()
        self.actualizar_puntos_en_leaderboard(5)  # Añade la cantidad de puntos que consideres.
        self.close_quiz() #Se usa close_quiz en vez de otro metodo para que el menu principal se muestre al cierre del quiz

    def mark_quiz_complete(self):
        try:
            user = self.current_user
            if user is None:
                print("Usuario no encontrado.")
                return

            progress_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progreso.json')
            completion_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leccion_completada.json')

            """
            module_key = nombre del modulo actual
            quiz_key = nombre del quiz actual
            quiz_completion_key = clave que ira al leccion_completada.json para marcar como completado el quiz
            """
            module_key = f"Modulo{self.current_module_index}"
            quiz_key = f"Quiz{self.current_quiz_index}"
            quiz_completion_key = f"Quiz_completado{self.current_quiz_index}"

            # Actualizar progreso.json
            with open(progress_file_path, 'r', encoding='UTF-8') as file:
                progress_data = json.load(file)

            #Si la clave del modulo no se encuentra en progreso.json se levanta un key Error 
            # En caso contrario Se marca el quiz como completado (True) para el usuario actual
            if module_key not in progress_data[user]:
                raise KeyError(f"Error: {module_key} no existe en progreso.json")
            progress_data[user][module_key][quiz_key] = True

            # Desbloquear la siguiente lección o quiz en progreso.json
            siguiente_quiz = f'Quiz{int(self.current_quiz_index) + 1}'
            siguiente_modulo = f"Modulo{int(self.current_module_index) + 1}"
            # Verificar si el módulo actual tiene el siguiente quiz
            if siguiente_quiz not in progress_data[user].get(module_key, {}):
                # Si no existe el siguiente quiz en el módulo actual, desbloquear el primer quiz del siguiente módulo
                if siguiente_modulo in progress_data[user]:
                    progress_data[user][siguiente_modulo]["Quiz1"] = True
                else:
                    raise KeyError(f"El siguiente módulo ({siguiente_modulo}) no existe en el progreso del usuario.")
            else:
                # Si existe, desbloquear el siguiente quiz en el módulo actual
                progress_data[user][module_key][siguiente_quiz] = True

            #Se escribe progreso.json con la nueva información
            with open(progress_file_path, 'w', encoding='UTF-8') as file:
                json.dump(progress_data, file, indent=4)

            #Leer leccion_completada.json
            with open(completion_file_path, 'r', encoding='UTF-8') as file:
                completion_data = json.load(file)
 
            #Verificar Si la clave del modulo existe en el JSON para el usuario actual
            if module_key not in completion_data[user]:
                # Si el módulo no está presente, inicializa un nuevo diccionario vacío para este módulo en los datos de finalización del usuario.
                completion_data[user][module_key] = {}

            # Marca el quiz como completado estableciendo su clave (quiz_completion_key) en True dentro del módulo correspondiente para el usuario.
            completion_data[user][module_key][quiz_completion_key] = True

            #Se reescribe leccion_completada.json con los nuevos cambios
            with open(completion_file_path, 'w', encoding='UTF-8') as file:
                json.dump(completion_data, file, indent=4)

        except Exception as e:
            print(f"Error al marcar el quiz como completado: {e}")
            print(f"Linea {sys.exc_info()[2].tb_lineno}")

    def abrir_leaderboard(self):
        LeaderBoard()

    def actualizar_puntos_en_leaderboard(self, puntos_ganados):
        leaderboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Codigos_LeaderBoard', 'leaderboard.json')

        try:
            with open(leaderboard_path, 'r', encoding='UTF-8') as file:
                leaderboard = json.load(file)

            usuario_existente = False
            for user in leaderboard:
                if user["name"] == self.current_user:
                    user["points"] += puntos_ganados
                    usuario_existente = True
                    break

            if not usuario_existente:
                leaderboard.append({"name": self.current_user, "points": puntos_ganados})

            with open(leaderboard_path, 'w', encoding='UTF-8') as file:
                json.dump(leaderboard, file, indent=4)

        except FileNotFoundError:
            print("Archivo leaderboard.json no encontrado.")


    @staticmethod
    def load_current_user():
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'current_user.json'), 'r', encoding='UTF-8') as file:
                user_data = json.load(file)
            return user_data.get("current_user")
        except FileNotFoundError:
            print("Archivo current_user.json no encontrado.")
            return None

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.layout.update()

    def create_feedback_label(self):
        self.feedback_label = QLabel('')
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.feedback_label)

    def create_multiple_choice_layout(self, section):
        self.button_widgets = []
        self.button_group = QButtonGroup()

        answers_layout = QHBoxLayout()

        for block in section['blocks']:
            block_type = block['type']
            block_label = QLabel(block['text'])
            block_label.setWordWrap(True)
            block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
            if block["type"] == "Consola":
                block_label.setStyleSheet(
                    f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
            self.layout.addWidget(block_label)

        for answer in section['answers']:
            button_widget = QRadioButton(answer["text"])
            button_widget.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white")
            self.button_widgets.append(button_widget)
            self.button_group.addButton(button_widget)
            answers_layout.addWidget(button_widget)

        self.layout.addLayout(answers_layout)

    def create_complete_blank_space_layout(self, section):
        self.blank_space_index = -1
        self.original_hint_text = ""

        for block in section['blocks']:
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

        for answer in section['answers']:
            answer_button = QPushButton(answer["text"])
            answer_button.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px; background-color: white")
            answer_button.clicked.connect(lambda checked, text=answer["text"]: self.handle_answer_click(text))
            answers_layout.addWidget(answer_button)

        self.layout.addLayout(answers_layout)

    def create_drag_and_drop_layout(self, section):
        drop_labels = []

        for block in section["blocks"]:
            block_type = block["type"]

            if block_type == "Consola":
                drop_label = DropLabel(block["text"], self.styles, question_type=block_type, multiple=True)
                drop_labels.append(drop_label)
                self.layout.addWidget(drop_label)
            else:
                block_label = QLabel(block["text"])
                block_label.setWordWrap(True)
                block_label.setStyleSheet(f"font-size: {self.styles['font_size_normal']}px")
                self.layout.addWidget(block_label)

        self.drop_labels = drop_labels

        draggable_labels_layout = QHBoxLayout()
        draggable_labels_layout.setSpacing(50)

        for answer in section["answers"]:
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
        user_order = []

        for label in self.drop_labels:
            user_order.extend(label.dropped_texts)

        correct_order = self.section['correctOrder']

        if user_order == correct_order:
            self.feedback_label.setText('¡Correcto!')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            self.submit_button.setVisible(False)
            if self.is_last_section():
                self.complete_button.setVisible(True)
            else:
                self.continue_button.setVisible(True)
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")

    def check_multiple_choice_answers(self):
        selected_answers = [btn.text() for btn in self.button_widgets if btn.isChecked()]
        correct_answers = [answer["text"] for answer in self.section["answers"] if answer.get("correct", False)]

        if selected_answers == correct_answers:
            self.feedback_label.setText('¡Correcto!')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            self.submit_button.setVisible(False)
            if self.is_last_section():
                self.complete_button.setVisible(True)
            else:
                self.continue_button.setVisible(True)
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")

    def check_complete_blank_space_answers(self):
        user_text = self.hint_label.text()
        correct_text = self.section["correctValue"]

        if user_text == correct_text:
            self.feedback_label.setText('¡Correcto!')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            self.submit_button.setVisible(False)
            if self.is_last_section():
                self.complete_button.setVisible(True)
            else:
                self.continue_button.setVisible(True)
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")

    def reset_layout(self):
        self.load_quiz_section()

    def load_next_section(self):
        self.current_section_in_quiz_index += 1
        current_quiz = self.page_order[self.current_quiz_index - 1]
        if self.current_section_in_quiz_index >= len(current_quiz["sections"]):
            self.current_quiz_index += 1
            self.current_section_in_quiz_index = 0
            if self.current_quiz_index >= len(self.page_order):
                return
        self.clear_layout()
        self.load_quiz_section()

    def is_last_section(self):
        current_quiz = self.page_order[self.current_quiz_index - 1]
        return self.current_section_in_quiz_index == len(current_quiz["sections"]) - 1

    def close_quiz(self):
        #Aqui cerramos el quiz pero, previo a esto, creamos y mostramos la ventana del menu principal.
        self.dashboard = Dashboard()
        self.dashboard.showMaximized()
        self.main_window.close()
  

class Main_Modulos_Quizzes_Window(QWidget):
    def __init__(self, quiz_file, current_quiz_index, current_module_index):
        super().__init__()
        self.styles = JsonLoader.load_json_styles()
        self.quiz_file = quiz_file
        self.current_quiz_index = current_quiz_index
        self.current_module_index = current_module_index
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Ubicación fija para page_order_file
        page_order_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Quizzes', 'page_order_Quizzes', 'page_order.json')
        self.quiz_loader = QuizLoader(self.layout, self.styles, self.quiz_file, page_order_file, self.current_quiz_index, self.current_module_index, self)
        self.quiz_loader.load_quiz_section()

    def closeEvent(self, event):
        #NOTA: el closeEvent es una funcion nativa de la ventana (boton cerrar ó X)
        #La modificamos para que antes de cerrar la ventana del quiz, abra el menu principal
        self.dashboard = Dashboard()
        self.dashboard.showMaximized()
        # Luego, cierra la ventana normalmente
        super().closeEvent(event)


