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
    
    @staticmethod
    def load_lesson_completed():
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leccion_completada.json'), 'r', encoding='UTF-8') as file:
                all_users_progress = json.load(file)
            return all_users_progress
        except FileNotFoundError:
            print("Archivo leccion_completada.json no encontrado.")
            return {}
    
    @staticmethod
    def load_user_progress():
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progreso.json'), 'r',
                      encoding='UTF-8') as file:
                progreso = json.load(file)
            return progreso
        except FileNotFoundError:
            print("Archivo progreso.json no encontrado.")
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
                    # Asigna la sección correspondiente en los datos del quiz usando page_type (el 0 es necesario para sacarlo del array)
                    self.section = quiz_data[page_type][0]
                    # Asigna el tipo de página actual
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
            elif self.page_type == 'completeblankspace' or self.page_type == 'completeblankspace2':
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
        self.main_window.unlock_module_first_quiz(
            JsonLoader.load_user_progress(),
            JsonLoader.load_lesson_completed(),
            f'Modulo{int(self.current_module_index) + 1}',
            self.current_user
        )
        self.actualizar_puntos_en_leaderboard(5)  # Añade la cantidad de puntos que consideres.
        self.main_window.close()   #Se usa close_quiz en vez de otro metodo para que el menu principal se muestre al cierre del quiz

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

            # Verificar si el siguiente quiz existe en el módulo actual
            if siguiente_quiz in progress_data[user][module_key]:
                progress_data[user][module_key][siguiente_quiz] = True  # Desbloquear siguiente quiz
            else:
                # Si no existe el siguiente quiz, desbloquear la primera lección del siguiente módulo
                siguiente_modulo_key = f"Modulo{int(self.current_module_index) + 1}"
                
                # Verificar si el siguiente módulo existe en progreso.json para el usuario actual
                if siguiente_modulo_key in progress_data[user]:
                    progress_data[user][siguiente_modulo_key]['Leccion1'] = True  # Desbloquear Leccion1 del siguiente módulo
                else:
                    print(f"El módulo {siguiente_modulo_key} no existe en progreso.json para el usuario {user}.")

            #Se escribe progreso.json con la nueva información
            with open(progress_file_path, 'w', encoding='UTF-8') as file:
                json.dump(progress_data, file, indent=4)

            #Leer leccion_completada.json
            with open(completion_file_path, 'r', encoding='UTF-8') as file:
                completion_data = json.load(file)
 
            #Verificar Si la clave del modulo existe en el JSON para el usuario actual
            if module_key not in completion_data[user]:
                raise KeyError(f"la clave {module_key} no existe en leccion_completada.json")

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

    def clear_layout(self, layout=None):
        if layout is None:
            layout = self.layout  # Usa el layout principal si no se pasa ninguno
        while layout.count():
            child = layout.takeAt(0)

            if child.widget():
                widget = child.widget()
                widget.deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())  # Llamada recursiva para limpiar el sublayout
            else:
                print("Elemento desconocido encontrado en el layout.")

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
                self.blank_space_index = block["text"].find("_")
                self.indices = [i for i, c in enumerate(block["text"]) if c == "_"]
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
    
        # Encuentra el primer espacio en blanco (___) en el texto actual
        blank_start = current_text.find("___")
        
        if blank_start != -1:
            # Longitud de la respuesta ingresada
            answer_length = len(answer_text)
            
            # Reemplaza solo el espacio requerido con la respuesta y elimina guiones sobrantes
            before_blank = current_text[:blank_start]  # Texto antes del espacio
            after_blank = current_text[blank_start + len(self.indices):]  # Texto después del espacio
            
            # Reemplaza el espacio en blanco con la respuesta y ajusta los guiones
            if answer_length < len(self.indices):  # Si la respuesta es más corta que el espacio
                # Ajustar guiones sobrantes
                new_text = f"{before_blank}{answer_text}"
            else:
                # La respuesta encaja exactamente o supera el espacio
                new_text = f"{before_blank}{answer_text[:len(self.indices)]}{after_blank}"
            
            # Actualiza el texto en el label
            self.hint_label.setText(new_text)

    def check_answers(self):
        if self.page_type == 'draganddrop':
            self.check_drag_and_drop_answers()
        elif self.page_type == 'multiplechoice':
            self.check_multiple_choice_answers()
        elif self.page_type == 'completeblankspace' or self.page_type == 'completeblankspace2':
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
        user_answer = []

        # Recorrer los índices y extraer el texto entre los guiones bajos
        for i in range(len(self.indices) - 1):
            user_answer.append(user_text[self.indices[i]:self.indices[i + 1]])
        
        answers = self.section["answers"]
        correct_text = [answer["text"] for answer in answers if answer["correct"]][0]

        if ''.join(user_answer) == correct_text:
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

class Main_Modulos_Quizzes_Window(QWidget):
    def __init__(self, quiz_file, current_quiz_index, current_module_index, username):
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

    @classmethod
    def unlock_module_first_quiz(cls, progreso_usuario, leccion_completada, nombre_modulo, username):
        try:
            # Verificar si el usuario existe en progreso_usuario y leccion_completada
            if username not in progreso_usuario:
                raise KeyError(f"Usuario '{username}' no encontrado en progreso.json.")
            if username not in leccion_completada:
                raise KeyError(f"Usuario '{username}' no encontrado en leccion_completada.json.")
            
            # Verificar si el módulo existe para el usuario
            if nombre_modulo.replace(" ", "") not in progreso_usuario[username]:
                raise KeyError(f"Módulo '{nombre_modulo}' no encontrado para el usuario '{username}' en progreso.json.")
            if nombre_modulo.replace(" ", "") not in leccion_completada[username]:
                raise KeyError(f"Módulo '{nombre_modulo}' no encontrado para el usuario '{username}' en leccion_completada.json.")
            
            # Obtener el estado del módulo para el usuario actual
            estado_modulo = progreso_usuario[username].get(nombre_modulo.replace(" ", ""), {})
            
            # Cargar las lecciones completadas del módulo
            estado_completado = leccion_completada[username].get(nombre_modulo.replace(" ", ""), {})

            # Obtener todas las claves que siguen el patrón "Leccion_completadaX" en el estado completado del módulo
            lecciones_completadas_claves = [
                clave for clave in estado_completado
                if clave.startswith("Leccion_completada")
            ]
            
            if not lecciones_completadas_claves:
                raise KeyError(f"No se encontraron claves de lección completada en '{nombre_modulo}' para el usuario '{username}'.")

            # Verificar si todas las lecciones del módulo han sido completadas
            todas_las_lecciones_completadas = all(
                estado_completado.get(clave, False)
                for clave in lecciones_completadas_claves
            )

            # Desbloquear el primer quiz si todas las lecciones del módulo han sido completadas
            if todas_las_lecciones_completadas:
                if "Quiz1" not in estado_modulo:
                    raise KeyError(f"'Quiz1' no encontrado en el módulo '{nombre_modulo}' para el usuario '{username}' en progreso.json.")
                
                if not estado_modulo.get("Quiz1", True):
                    estado_modulo["Quiz1"] = True  # Desbloquea el primer quiz
                    progreso_usuario[username][nombre_modulo.replace(" ", "")] = estado_modulo

            # Guardar los cambios en progreso.json y leccion_completada.json
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progreso.json'), 'w', encoding='UTF-8') as file:
                json.dump(progreso_usuario, file, indent=4)

            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leccion_completada.json'), 'w', encoding='UTF-8') as file:
                json.dump(leccion_completada, file, indent=4)

        except KeyError as e:
            print(f"Error: {e}")
            