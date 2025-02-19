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
from congratulation_Feature import CongratulationWindow
from badge_system.display_cabinet import BadgeDisplayCabinet
from game_features.progress_bar_quizzes import ProgressBar



class JsonLoader:
    @staticmethod
    def load_json_data(filename):
        try:
            if not os.path.isfile(filename):
                raise FileNotFoundError(f"Archivo no encontrado: {filename}")
            with open(filename, encoding='UTF-8') as json_file:
                data = json.load(json_file)
                if data is None:
                    raise ValueError("El contenido del archivo es vacío o no válido.")
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
        self.load_page_order()  # Cargar page_order
        self.feedback_label = QLabel('')
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.feedback_label)
        self.current_user = self.load_current_user()
        self.current_quiz_index = current_quiz_index
        self.current_module_index = current_module_index
        self.main_window = main_window
        self.section = None
        self.page_type = None
        self.usuario_actual = self.cargar_usuario_actual()

        # Verifica si ya tienes una instancia de la barra de progreso
        if not hasattr(self, 'progress_bar'):  # Solo crea la barra si no ha sido creada antes
            page_order_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "Daniel_JSON_Files_Elmer", "Quizzes", "page_order_Quizzes", "page_order.json"
            )
            if not os.path.isfile(page_order_file):
                print(f"El archivo no existe en la ruta: {page_order_file}")
            else:
                lesson_data = JsonLoader.load_json_data(page_order_file)
                self.progress_bar = ProgressBar(lesson_data, current_quiz_index=self.current_quiz_index, current_module_index=self.current_module_index)

            


    def load_current_quiz(self):
            # Lógica para cargar el quiz basado en los índices
            for quiz in self.page_order:
                if quiz["module"] == self.current_module_index and quiz["quiz_number"] == self.current_quiz_index:
                    self.current_quiz = quiz
                    
    def load_page_order(self):
        if not os.path.isfile(self.page_order_file):
            raise FileNotFoundError(f"Archivo no encontrado: {self.page_order_file}")
        with open(self.page_order_file, "r", encoding='UTF-8') as file:
            self.page_order = json.load(file)["quizzes"]
        self.current_section_in_quiz_index = 0

    def cargar_usuario_actual(self):
        # Cargar el usuario actual desde el archivo JSON
        with open("current_user.json", "r") as file:
            data = json.load(file)
        return data["current_user"]

    def load_quiz_section(self):
        self.clear_layout()
        try:
            quiz_file_path = self.quiz_file
            if not os.path.isfile(quiz_file_path):
                raise FileNotFoundError(f"Archivo no encontrado: {quiz_file_path}")
            with open(quiz_file_path, "r", encoding='UTF-8') as file:
                quiz_data = json.load(file)

            matching_quizzes = []  # Lista de quizzes coincidentes
            for quiz in self.page_order:
                if int(quiz["module"]) == int(self.current_module_index) and int(quiz["quiz_number"]) == int(self.current_quiz_index):
                    matching_quizzes.append(quiz)

            if matching_quizzes:
                current_quiz = matching_quizzes[0]
            else:
                current_quiz = None
                raise FileNotFoundError("No se encontró ningún quiz que coincida con los números especificados.")
            
            if current_quiz:
                if 0 <= self.current_section_in_quiz_index < len(current_quiz["sections"]):
                    current_section = current_quiz["sections"][self.current_section_in_quiz_index]             
                    page_type = current_section["page_type"]                         
                    self.section = quiz_data[page_type][0]
                    self.page_type = page_type

            if self.page_type not in quiz_data:
                raise KeyError(f"La clave '{self.page_type}' no existe en el JSON")

            if not quiz_data[self.page_type]:
                raise ValueError(f"La lista para la clave '{self.page_type}' está vacía")

            buttons_layout = QHBoxLayout()

            self.leaderboard_button = QPushButton("Leaderboard")
            self.leaderboard_button.setStyleSheet(
                f"background-color: {self.styles['continue_button_color']}; color: white; font-size: {self.styles['font_size_buttons']}px"
            )
            self.leaderboard_button.clicked.connect(self.abrir_leaderboard)
            buttons_layout.addWidget(self.leaderboard_button)

            self.display_cabinet = QPushButton("Mis Insignias")
            self.display_cabinet.setStyleSheet(
                f"background-color: {self.styles['continue_button_color']}; color: white; font-size: {self.styles['font_size_buttons']}px"
            )
            display_cabinet_font = QFont()
            display_cabinet_font.setPointSize(self.styles['font_size_buttons'])
            self.display_cabinet.setFont(display_cabinet_font)
            self.display_cabinet.clicked.connect(self.abrir_display_cabinet)
            buttons_layout.addWidget(self.display_cabinet)

            
            self.layout.addWidget(self.progress_bar)  # Asegúrate de agregar la barra de progreso al layout
            self.layout.addLayout(buttons_layout)

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

    def abrir_display_cabinet(self, username):
        self.display_cabinet = BadgeDisplayCabinet(self.usuario_actual)
        self.display_cabinet.show()

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
            f'Módulo{int(self.current_module_index) + 1}',
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
            module_key = nombre del módulo actual
            quiz_key = nombre del quiz actual
            quiz_completion_key = clave que ira al leccion_completada.json para marcar como completado el quiz
            """
            module_key = f"Módulo{self.current_module_index}"
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
                siguiente_modulo_key = f"Módulo{int(self.current_module_index) + 1}"
                
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
                if isinstance(widget, ProgressBar):
                    continue  # No eliminar la barra de progreso
                widget.deleteLater()  # Eliminar otros widgets
            elif child.layout():
                self.clear_layout(child.layout())  # Llamada recursiva para limpiar los sublayouts
            else:
                print("Elemento desconocido encontrado en el layout.")

    def update_progress(self, current_section_index, total_sections):
        progress_value = (current_section_index / total_sections) * 100
        self.progress_bar.set_value(progress_value)  # Esto actualizaría la barra de progreso


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
            CongratulationWindow.correct_response()
            self.submit_button.setVisible(False)
            if self.is_last_section():
                self.complete_button.setVisible(True)
            else:
                self.continue_button.setVisible(True)
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            CongratulationWindow.incorrect_response()

    def check_multiple_choice_answers(self):
        selected_answers = [btn.text() for btn in self.button_widgets if btn.isChecked()]
        correct_answers = [answer["text"] for answer in self.section["answers"] if answer.get("correct", False)]

        if selected_answers == correct_answers:
            self.feedback_label.setText('¡Correcto!')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            CongratulationWindow.correct_response()
            self.submit_button.setVisible(False)
            if self.is_last_section():
                self.complete_button.setVisible(True)
            else:
                self.continue_button.setVisible(True)
        else:
            self.feedback_label.setText('Incorrecto, inténtalo de nuevo.')
            self.feedback_label.setStyleSheet(
                f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")
            CongratulationWindow.incorrect_response()

    def check_complete_blank_space_answers(self):
        try:
            # Obtener la respuesta correcta
            correct_answer_text = None
            for answer in self.section["answers"]:
                if answer.get("correct", False):
                    correct_answer_text = answer["text"]
                    break

            # Extraer la respuesta del usuario desde el espacio en blanco
            user_text = self.hint_label.text()

            # Buscar la posición del espacio en blanco en el texto original
            selected_answer_start = self.original_hint_text.find("___")

            # Si no hay espacio en blanco en el texto original, error
            if selected_answer_start == -1:
                self.feedback_label.setText("No se encontró el espacio en blanco en el texto. Verifica el formato.")
                self.feedback_label.setStyleSheet(
                    f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")
                return

            # Extraer todo lo que el usuario ingresó después del espacio en blanco
            selected_answer = user_text[selected_answer_start:].strip()

            # Limpiar cualquier texto adicional que no sea parte de la respuesta del usuario
            if " " in selected_answer:
                selected_answer = selected_answer.split()[0]  # Tomar solo la primera "palabra"

            # Validar si el usuario no ingresó respuesta
            if selected_answer == "___":
                self.feedback_label.setText("No has ingresado una respuesta. Por favor, inténtalo de nuevo.")
                self.feedback_label.setStyleSheet(
                    f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")
                return

            # Verificar si la respuesta del usuario es correcta
            print(selected_answer, correct_answer_text)  # Debug
            if selected_answer == correct_answer_text:
                self.feedback_label.setText("¡Correcto!")
                self.feedback_label.setStyleSheet(
                    f"color: {self.styles.get('correct_color', '#00FF00')}; font-size: {self.styles.get('font_size_answers', 12)}px")
                CongratulationWindow.correct_response()
                self.submit_button.setVisible(False)
                if self.is_last_section():
                    self.complete_button.setVisible(True)
                else:
                    self.continue_button.setVisible(True)
            else:
                # Respuesta incorrecta
                self.feedback_label.setText("Respuesta incorrecta. Inténtalo de nuevo.")
                self.feedback_label.setStyleSheet(
                    f"color: {self.styles.get('incorrect_color', '#FF0000')}; font-size: {self.styles.get('font_size_answers', 12)}px")
                CongratulationWindow.incorrect_response()
        except Exception as e:
            print(f"Error al verificar respuestas de completeblankspace: {e}")


    def reset_layout(self):
        self.load_quiz_section()

    def load_next_section(self):
        self.current_section_in_quiz_index += 1
        current_quiz = self.page_order[self.current_quiz_index - 1]
        total_sections = len(current_quiz["sections"])
        
        if self.current_section_in_quiz_index >= total_sections:
            self.current_quiz_index += 1
            self.current_section_in_quiz_index = 0
            if self.current_quiz_index >= len(self.page_order):
                self.submit_button.setVisible(False)
                self.reset_button.setVisible(False)
                self.continue_button.setVisible(False)
                self.complete_button.setVisible(True)
                return
        
        self.update_progress(self.current_section_in_quiz_index, total_sections)  # Actualiza el progreso
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
            