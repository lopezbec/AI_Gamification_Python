import datetime
import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QMainWindow, QVBoxLayout, QWidget


class BadgeVerification(QDialog):
    def __init__(self, badge_id: str) -> None:
        super().__init__()
        self.badge_id = badge_id  # Asignar badge_id como propiedad de la clase

        try:
            # Cargar los criterios de las insignias desde el archivo JSON
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_criteria.json"), "r", encoding='UTF-8') as file:
                self.badge_criteria = json.load(file)

            # Cargar la información de la insignia específica usando el badge_id
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_info.json"), "r", encoding='UTF-8') as finish_info:
                data = json.load(finish_info)

            # Seleccionar la información de la insignia específica basada en badge_id
            badge_info = next((badge for badge in data if badge["badge_id"] == self.badge_id), None)

            if badge_info:
                # Window properties
                self.setWindowTitle(badge_info["badge_text"])
                # Layouts
                layoutV = QVBoxLayout()
                # Label properties
                badge = QLabel(self)
                badge_title = badge_info["badge_title"]
                badge_description = badge_info["badge_description"]
                badge.setText(badge_title + '\n' + badge_description)
                font = QFont()
                font.setFamily(badge_info["badge_font_family"])
                badge.setFont(font)
                font.setPointSize(badge_info["badge_font_size"])
                badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
                badge.setMargin(badge_info["badge_margin"])

                label = QLabel()
                image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medal_icon.png')
                pixmap = QPixmap(image_path)

                if not pixmap.isNull():
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    pixmap = pixmap.scaledToWidth(200)
                    label.setPixmap(pixmap)
                    label.setFixedSize(pixmap.width(), pixmap.height())

                    # Vertical layout
                    layoutV.setSpacing(10)
                    layoutV.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
                    layoutV.addWidget(badge)
                    layoutV.addWidget(label)
                    self.setLayout(layoutV)
                else:
                    raise FileNotFoundError("Ruta de la imagen no encontrada")
            else:
                raise Exception(f"No se encontró información para la insignia con ID '{self.badge_id}'")        
        except Exception as e:
            print(f"Fallo en la creación de la clase: {e}")
            print(f"Error en linea {sys.exc_info()[2].tb_lineno}")

def display_badge(badge_id):
        badge_window = BadgeVerification(badge_id)
        badge_window.exec()
    
def load_badges():
    with open("badge_info.json", "r") as file:
        return json.load(file)
    
def load_badges_criteria():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_criteria.json")) as content:
        return json.load(content)

def save_badge_progress_per_user(username):
    try:
        # Nombre del directorio
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'badge_progress')
        # Nombre del archivo json
        filename = f'{username}_badge_progress.json'
        # Path completo al archivo
        filepath = os.path.join(directory, filename)

        # Crear el directorio si no existe
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Verificar si el archivo json ya existe
        if not os.path.exists(filepath):
            # Crear un diccionario con los valores iniciales de cada badge
            badge_data = {
                "streak": 0,
                "gran_paso": False,
                "hello_world": False,
                "5_correctas": False,
                "10_correctas": False,
                "20_correctas": False,
                "intermedio": False,
                "avanzado": False,
                "experto": False,
                "doble_aprendizaje": False,
                "modulo_rapido": False
            }

            # Escribir el diccionario en el archivo json
            with open(filepath, 'w') as file:
                json.dump(badge_data, file, indent=4)
    except OSError as e:
        print(f"Error al crear el directorio o archivo: {e}")

def update_badge_progress(username, badge_name):
    try:
        # Nombre del directorio
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'badge_progress')
        # Nombre del archivo json
        filename = f'{username}_badge_progress.json'
        # Path completo al archivo
        filepath = os.path.join(directory, filename)

        # Verificar si el archivo json ya existe
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'El archivo {filepath} no existe.')

        # Leer el contenido del archivo JSON
        with open(filepath, 'r') as file:
            badge_data = json.load(file)

        # Verificar si el badge_name existe en el diccionario
        if badge_name not in badge_data:
            raise KeyError(f'El badge {badge_name} no existe.')

        # Actualizar el valor del badge a True
        badge_data[badge_name] = True

        # Escribir el diccionario actualizado en el archivo JSON
        with open(filepath, 'w') as file:
            json.dump(badge_data, file, indent=4)

    except FileNotFoundError as e:
        print(f'Error in update_badge_progress: {e}')
    except KeyError as e:
        print(f'Error in update_badge_progress: {e}')
    except OSError as e:
        print(f'Error al leer o escribir el archivo in update_badge_progress: {e}')

def is_badge_earned(username, badge_name) -> bool:
    try:
        # Nombre del directorio
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'badge_progress')
        # Nombre del archivo json
        filename = f'{username}_badge_progress.json'
        # Path completo al archivo
        filepath = os.path.join(directory, filename)

        # Verificar si el archivo json ya existe
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'El archivo {filepath} no existe.')

        # Leer el contenido del archivo JSON
        with open(filepath, 'r') as file:
            badge_data = json.load(file)

        # Verificar si el badge_name existe en el diccionario
        if badge_name not in badge_data:
            raise KeyError(f'El badge {badge_name} no existe.')

        # Retornar el valor del badge
        return badge_data[badge_name]

    except FileNotFoundError as e:
        print(f'Error in is_badge_earned: {e}')
        return False
    except KeyError as e:
        print(f'Error in is_badge_earned: {e}')
        return False
    except OSError as e:
        print(f'Error al leer el archivo in is_badge_earned: {e}')
        return False

def get_badge_level(self, score):
    try:
        # Cargar los niveles desde el archivo JSON
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_info.json"), "r", encoding='UTF-8') as file:
            levels = json.load(file)

        for level in levels:
            # Verificar si el nivel tiene el atributo 'range'
            if 'range' not in level:
                continue

            range_str = level["range"]
            if "<=" in range_str:
                max_score = int(range_str.split('<=')[1].strip())
                if score <= max_score and is_badge_earned(self.usuario_actual, level["badge_id"]):
                    display_badge(level["badge_id"])
                    update_badge_progress(self.usuario_actual, level["badge_id"])
                    return
            elif "-" in range_str:
                min_score, max_score = map(int, range_str.split('-'))
                if min_score <= score <= max_score and is_badge_earned(self.usuario_actual, level["badge_id"]):
                    display_badge(level["badge_id"])
                    update_badge_progress(self.usuario_actual, level["badge_id"])
                    return
        return
    except (ValueError, IndexError) as e:
        print(f"Error al procesar el rango del nivel: {e}")
        return None

def are_lessons_completed_same_day(username, module_name) -> bool:
    try:
        # Nombre del directorio
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'badge_progress')
        # Nombre del archivo JSON
        filename = 'lessons_date_completion.json'
        # Path completo al archivo
        filepath = os.path.join(directory, filename)

        # Verificar si el archivo json existe
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'El archivo {filepath} no existe.')

        # Leer el contenido del archivo JSON
        with open(filepath, 'r') as file:
            lesson_data = json.load(file)

        # Verificar si el usuario existe en el diccionario
        if username not in lesson_data:
            raise KeyError(f'El usuario {username} no existe.')

        # Verificar si el módulo_name existe en el diccionario del usuario
        if module_name not in lesson_data[username]:
            raise KeyError(f'El módulo {module_name} no existe para el usuario {username}.')

       # Obtener las lecciones completadas del módulo
        completed_lessons = lesson_data[username][module_name]

        # Verificar si todas las lecciones completadas del módulo fueron en la misma fecha
        completion_dates = set(completed_lessons.values())

        # Si hay algún valor vacío, devuelve False
        if "" in completion_dates:
            return False

        return len(completion_dates) == 1

    except FileNotFoundError as e:
        print(f'Error in are_lessons_completed_same_day File not Found: {e}')
        return False
    except KeyError as e:
        print(f'Error in are_lessons_completed_same_day Key not found: {e}')
        return False
    except Exception as e:
        print(f'Error in are_lessons_completed_same_day Other Exception: {e}')
        return False
    
def create_lessons_date_completion(username):
    try:
        # Nombre del directorio
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'badge_progress')
        # Nombre del archivo JSON
        filename = 'lessons_date_completion.json'
        # Path completo al archivo
        filepath = os.path.join(directory, filename)

        # Verificar si el archivo ya existe
        if not os.path.exists(filepath):
            # Crear la estructura inicial
            data = {username: {
                "Modulo1": {
                    "Leccion_completada1": "",
                    "Leccion_completada2": "",
                    "Leccion_completada3": "",
                    "Leccion_completada4": "",
                    "Leccion_completada5": ""
                },
                "Modulo2": {
                    "Leccion_completada1": "",
                    "Leccion_completada2": "",
                    "Leccion_completada3": ""
                },
                "Modulo3": {
                    "Leccion_completada1": "",
                    "Leccion_completada2": "",
                    "Leccion_completada3": "",
                    "Leccion_completada4": "",
                    "Leccion_completada5": ""
                },
                "Modulo4": {
                    "Leccion_completada1": "",
                    "Leccion_completada2": "",
                    "Leccion_completada3": "",
                    "Leccion_completada4": "",
                    "Leccion_completada5": ""
                },
                "Modulo5": {
                    "Leccion_completada1": "",
                    "Leccion_completada2": "",
                    "Leccion_completada3": "",
                    "Leccion_completada4": "",
                    "Leccion_completada5": "",
                    "Leccion_completada6": "",
                    "Leccion_completada7": ""
                }
            }}
            
            # Guardar la estructura inicial en el archivo JSON
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)

            print(f'Se creó el archivo {filename} con la estructura inicial para el usuario {username}.')
        else:
            # Leer el contenido del archivo JSON
            with open(filepath, 'r') as file:
                lesson_dates = json.load(file)
            
            # Verificar si el usuario ya existe en el archivo
            if username not in lesson_dates:
                # Agregar el nuevo usuario al final del diccionario
                lesson_dates[username] = {
                    "Modulo1": {
                        "Leccion_completada1": "",
                        "Leccion_completada2": "",
                        "Leccion_completada3": "",
                        "Leccion_completada4": "",
                        "Leccion_completada5": ""
                    },
                    "Modulo2": {
                        "Leccion_completada1": "",
                        "Leccion_completada2": "",
                        "Leccion_completada3": ""
                    },
                    "Modulo3": {
                        "Leccion_completada1": "",
                        "Leccion_completada2": "",
                        "Leccion_completada3": "",
                        "Leccion_completada4": "",
                        "Leccion_completada5": ""
                    },
                    "Modulo4": {
                        "Leccion_completada1": "",
                        "Leccion_completada2": "",
                        "Leccion_completada3": "",
                        "Leccion_completada4": "",
                        "Leccion_completada5": ""
                    },
                    "Modulo5": {
                        "Leccion_completada1": "",
                        "Leccion_completada2": "",
                        "Leccion_completada3": "",
                        "Leccion_completada4": "",
                        "Leccion_completada5": "",
                        "Leccion_completada6": "",
                        "Leccion_completada7": ""
                    }
                }
                
                # Guardar el diccionario actualizado en el archivo JSON
                with open(filepath, 'w') as file:
                    json.dump(lesson_dates, file, indent=4)
    except Exception as e:
        print(f'Error in create_lessons_date_completion: {e}')

def update_lesson_dates(username, module, lesson):
    try:
        # Nombre del directorio
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'badge_progress')
        # Nombre del archivo JSON
        filename = 'lessons_date_completion.json'
        # Path completo al archivo
        filepath = os.path.join(directory, filename)

        # Leer el contenido del archivo JSON
        with open(filepath, 'r') as file:
            lesson_dates = json.load(file)

        # Obtener la fecha actual en formato YYYY-MM-DD
        current_date = datetime.date.today().isoformat()

        # Verificar si el usuario tiene un módulo registrado en el archivo
        if username not in lesson_dates:
            lesson_dates[username] = {}

        # Verificar si el módulo tiene lecciones registradas en el archivo
        if module not in lesson_dates[username]:
            lesson_dates[username][module] = {}

        # Actualizar la fecha de la lección completada
        lesson_dates[username][module][lesson] = current_date

        # Guardar el diccionario actualizado en el archivo JSON
        with open(filepath, 'w') as file:
            json.dump(lesson_dates, file, indent=4)

        print(f'Se actualizó el archivo {filename} con la lección {lesson} del módulo {module} para el usuario {username}.')
    except Exception as e:
        print(f'Error in update_lesson_dates: {e}')