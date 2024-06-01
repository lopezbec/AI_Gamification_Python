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

def check_badges(streak, username):
    """
    check and display a certain badge based on the current streak of the users.
    """
    badges_criteria = load_badges_criteria()
    for criteria in badges_criteria:
        if streak >= criteria.get("value", 0):
            if not is_badge_earned(username, criteria.get("badge_id")):
                display_badge(criteria.get("badge_id"))
                update_badge_progress(username, criteria.get("badge_id"))

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
                "experto": False
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
        print(f'Error: {e}')
    except KeyError as e:
        print(f'Error: {e}')
    except OSError as e:
        print(f'Error al leer o escribir el archivo: {e}')

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
        print(f'Error: {e}')
        return False
    except KeyError as e:
        print(f'Error: {e}')
        return False
    except OSError as e:
        print(f'Error al leer el archivo: {e}')
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
                if score <= max_score:
                    display_badge(level["badge_id"])
                    update_badge_progress(self.usuario_actual, level["badge_id"])
                    return
            elif "-" in range_str:
                min_score, max_score = map(int, range_str.split('-'))
                if min_score <= score <= max_score:
                    display_badge(level["badge_id"])
                    update_badge_progress(self.usuario_actual, level["badge_id"])
                    return
        return
    except (ValueError, IndexError) as e:
        print(f"Error al procesar el rango del nivel: {e}")
        return None