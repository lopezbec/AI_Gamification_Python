import tkinter as tk
import random
from datetime import datetime


class CongratulationWindow:
    def __init__(self, log_filename="popup_log.txt", duration=3000):
        self.log_filename = log_filename
        self.duration = duration

    def show_popup(self, message):
        # Crear una ventana emergente (popup)
        popup = tk.Tk()
        popup.title("Mensaje")

        # Crear una etiqueta con el mensaje
        label = tk.Label(popup, text=message)
        label.pack(pady=30, padx=40)

        # Configurar un temporizador para cerrar el popup después de 'duration' milisegundos
        popup.after(self.duration, popup.destroy)

        # Ejecutar el bucle principal de la interfaz gráfica
        popup.mainloop()

    def log_popup_event(self, event_type):
        # Obtener la fecha y hora actual
        now = datetime.now()
        # Formatear la fecha y hora según el formato deseado
        formatted_date_time = now.strftime('%Y/%m/%d %I:%M:%S %p')

        # Crear una cadena con la fecha, hora y tipo de evento (correcto o incorrecto)
        log_entry = f"{formatted_date_time} {event_type}\n"

        # Abrir el archivo en modo de escritura (append) y escribir la entrada de registro
        with open(self.log_filename, "a") as log_file:
            log_file.write(log_entry)

    def correct_response(self):
        # Lista de mensajes de felicitaciones
        congratulations_messages = [
            "¡Gran trabajo!",
            "¡Bien hecho!",
            "¡Excelente respuesta!"
        ]
        # Elegir un mensaje al azar de la lista
        message = random.choice(congratulations_messages)

        # Mostrar el popup con el mensaje
        self.show_popup(message)

        # Registrar el evento en el archivo
        self.log_popup_event("Correcto")

    def incorrect_response(self):
        # Lista de palabras de aliento
        encouragement_messages = [
            "No está bien, pero sigue intentándolo.",
            "No te preocupes, puedes hacerlo mejor la próxima vez.",
            "Sigue practicando, estás cerca."
        ]
        # Elegir un mensaje al azar de la lista
        message = random.choice(encouragement_messages)

        # Mostrar el popup con el mensaje
        self.show_popup(message)

        # Registrar el evento en el archivo
        self.log_popup_event("Incorrecto")

# Puedes importar y usar la clase PopupManager en otro archivo como este:
# from nombre_de_tu_archivo import PopupManager

# Crear una instancia de PopupManager
CongratulationWindow = CongratulationWindow()

# Llamar a las funciones correct_response o incorrect_response según sea necesario
#CongratulationWindow.correct_response()
#CongratulationWindow.incorrect_response()
