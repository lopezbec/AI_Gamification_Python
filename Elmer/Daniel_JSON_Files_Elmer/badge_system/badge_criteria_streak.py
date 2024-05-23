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
    print("checking loaded badges")
    for criteria in badges_criteria:
        if streak >= criteria.get("value", 0):
            print("first check passed")
            if not is_badge_earned(username, criteria.get("badge_id")):
                print("second check passed")
                display_badge(criteria.get("badge_id"))
                update_badge_progress(username, criteria.get("badge_id"))

def display_badge(badge_id):
    badge_window = BadgeVerification(badge_id)
    badge_window.exec()

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
        print("updating badge")
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
