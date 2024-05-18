import json
import os
from badge_system.badge_verification import BadgeVerification

class BadgeCriteriaStreak:
    def __init__(self):
        self.streak = 0

    def correct_answer(self):
        self.streak += 1

    def incorrect_answer(self):
        self.streak = 0

    def get_current_streak(self):
        return self.streak

def display_badge(badge_details):
    badge_window = BadgeVerification(badge_details)
    badge_window.exec()

def load_badges():
    with open("badge_info.json", "r") as file:
        return json.load(file)
    
def load_badges_criteria():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_criteria.json")) as content:
        return json.load(content)

def check_badges(streak):
    badges_criteria = load_badges_criteria()
    for criteria in badges_criteria:
        if streak >= criteria.get("value", 0):
            display_badge(criteria.get("badge_id"))

def save_badge_progress_per_user(username):
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
            "intermedio": False,
            "avanzado": False,
            "experto": False
        }

        # Escribir el diccionario en el archivo json
        with open(filepath, 'w') as file:
            json.dump(badge_data, file, indent=4)
    else:
        pass

def update_streak(username, new_streak):
    # Nombre del directorio
    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'badge_progress')
    # Nombre del archivo json
    filename = f'{username}_badge_progress.json'
    # Path completo al archivo
    filepath = os.path.join(directory, filename)

    # Verificar si el archivo json existe
    if os.path.exists(filepath):
        # Leer el contenido del archivo json
        with open(filepath, 'r') as file:
            # Cargar los datos del archivo JSON
            badge_data = json.load(file)
        
        # Actualizar el valor de streak en el diccionario
        badge_data['streak'] += new_streak
        
        # Escribir los datos actualizados en el archivo json
        with open(filepath, 'w') as file:
            json.dump(badge_data, file, indent=4)
    else:
        print(f"El archivo {filename} no existe.")

def reset_streak(username):
    # Nombre del directorio
    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'badge_progress')
    # Nombre del archivo json
    filename = f'{username}_badge_progress.json'
    # Path completo al archivo
    filepath = os.path.join(directory, filename)

    # Verificar si el archivo json existe
    if os.path.exists(filepath):
        # Leer el contenido del archivo json
        with open(filepath, 'r') as file:
            # Cargar los datos del archivo JSON
            badge_data = json.load(file)
        
        # Actualizar el valor de streak en el diccionario
        badge_data['streak'] = 0
        
        # Escribir los datos actualizados en el archivo json
        with open(filepath, 'w') as file:
            json.dump(badge_data, file, indent=4)
    else:
        print(f"El archivo {filename} no existe.")

def read_stored_streak(username):
    # Nombre del directorio
    directory = 'badge_progress'
    # Nombre del archivo json
    filename = f'{username}_badge_progress.json'
    # Path completo al archivo
    filepath = os.path.join(directory, filename)

    # Verificar si el archivo json existe
    if os.path.exists(filepath):
        # Leer el contenido del archivo json
        with open(filepath, 'r') as file:
            # Cargar los datos del archivo JSON
            badge_data = json.load(file)
            return badge_data['streak']
    else:
        print(f"El archivo {filename} no existe.")
        return None