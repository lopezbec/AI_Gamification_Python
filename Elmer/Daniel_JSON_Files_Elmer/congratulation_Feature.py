import tkinter as tk
import random
from datetime import datetime
class CongratulationWindow:
    def __init__(self, log_filename="popup_log.txt", duration=3000):
        self.log_filename = log_filename
        self.duration = duration

    def show_popup(self, message, bg_color="#00BFFF"):
        # Crear una ventana emergente (popup)
        popup = tk.Tk()
        popup.title("Mensaje")
        label_font = ('Helvetica', 16)
        popup.configure(bg=bg_color)
        # Crear una etiqueta con el mensaje
        label = tk.Label(popup, text=message, font=label_font, bg=bg_color)
        label.pack(pady=110, padx=250)

        # Actualizar la ventana para asegurarse de que tenga sus dimensiones antes de calcular las coordenadas
        popup.update_idletasks()

        # Obtener las dimensiones de la pantalla del dispositivo
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana emergente
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        x_coordinate = (screen_width - popup_width) // 2
        y_coordinate = (screen_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")

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

        # Mostrar el popup con el mensaje en verde
        self.show_popup(message, bg_color="#00FF00")

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

        # Mostrar el popup con el mensaje en rosa
        self.show_popup(message, bg_color="#FFC0CB")

        # Registrar el evento en el archivo
        self.log_popup_event("Incorrecto")

# Crear una instancia de PopupManager
CongratulationWindow = CongratulationWindow()

# Llamar a las funciones correct_response o incorrect_response según sea necesario
#CongratulationWindow.correct_response()
#CongratulationWindow.incorrect_response()