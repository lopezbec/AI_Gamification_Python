import sys
import json
import csv
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QRadioButton, QWidget, QScrollArea, QMessageBox

app = QApplication([])

# Clase MainPage que hereda de QMainWindow
class MainPage(QMainWindow):
    # Constructor de la clase MainPage
    def __init__(self, data, page_type):
        super().__init__()
        self.data = data  # Almacena los datos proporcionados
        self.setStyleSheet('background-color: #444444;')  # Establece el estilo de fondo de la ventana
        self.page_type = page_type  # Almacena el tipo de página (Pedagogical o Question)
        self.initUI()  # Llama a la función para crear la interfaz de usuario
        self.start_time = datetime.now()  # Registra la hora de inicio

    # Función para inicializar la interfaz de usuario
    def initUI(self):
        self.setGeometry(100, 100, 700, 550)  # Configura la geometría de la ventana

        # Selecciona los bloques de datos en función del tipo de página
        if self.page_type == "Pedagogical":
            blocks = self.data["pedagogical"][0]["blocks"]
        else:
            blocks = self.data["question"][0]["blocks"]

        # Establece el título de la ventana
        self.setWindowTitle(self.data[self.page_type.lower()][0]["title"])
        layout = QVBoxLayout()  # Crea un layout vertical

        # Crea y añade etiquetas de título para cada sección pedagógica
        for seccion in self.data['pedagogical']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
            titulo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(titulo_label)

        font_size = 14

        # Crea y añade etiquetas para cada bloque de texto
        for block in blocks:
            label = QLabel(block["text"])
            label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
            layout.addWidget(label)

        # Si la página es de tipo pedagógico, añade un botón de continuar
        if self.page_type == "Pedagogical":
            continue_button = QPushButton("Continuar")
            continue_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
            continue_button.clicked.connect(self.open_secondary_page)  # Conecta el botón a la función open_secondary_page
            layout.addWidget(continue_button)

        container = QWidget()  # Crea un widget contenedor
        container.setLayout(layout)  # Asigna el layout al contenedor

        scroll = QScrollArea()  # Crea un área de desplazamiento
        scroll.setWidget(container)  # Añade el contenedor al área de desplazamiento
        scroll.setWidgetResizable(True)  # Habilita el redimensionamiento del widget
        self.setCentralWidget(scroll)  # Establece el área de desplazamiento como el widget central de la ventana

    # Función para abrir la página secundaria
    def open_secondary_page(self):
        elapsed_time = datetime.now() - self.start_time  # Calcula el tiempo transcurrido
        self.question_page = QuestionPage(self.data, elapsed_time)  # Crea una instancia de QuestionPage
        self.question_page.show()  # Muestra la instancia de QuestionPage
        self.hide()  # Oculta la página actual


    # Clase QuestionPage que hereda de QMainWindow
class QuestionPage(QMainWindow):
    # Constructor de la clase QuestionPage
    def __init__(self, data, elapsed_time_pedagogical):
        super().__init__()
        self.radio_buttons = []  # Inicializa la lista de botones de radio
        self.feedback_label = QLabel("")  # Inicializa la etiqueta de retroalimentación
        self.data = data  # Almacena los datos proporcionados
        self.setStyleSheet('background-color: #444444;')  # Establece el estilo de fondo de la ventana
        self.first_attempt = True  # Indica si es el primer intento de responder la pregunta
        self.elapsed_time_pedagogical = elapsed_time_pedagogical  # Almacena el tiempo transcurrido en la página pedagógica
        self.initUI()  # Llama a la función para crear la interfaz de usuario
        self.start_time = datetime.now()  # Registra la hora de inicio

    # Función para inicializar la interfaz de usuario
    def initUI(self):
        self.setGeometry(100, 100, 700, 550)  # Configura la geometría de la ventana
        self.setWindowTitle(self.data["question"][0]["title"])  # Establece el título de la ventana
        layout = QVBoxLayout()  # Crea un layout vertical
        font_size = 14

        # Crea y añade etiquetas de título para cada sección de preguntas
        for seccion in self.data['question']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
            titulo_label.setFixedHeight(70)  # Establece la altura fija de la etiqueta
            titulo_label.setAlignment(Qt.AlignCenter)  # Alinea la etiqueta al centro
            layout.addWidget(titulo_label)

        # Crea y añade etiquetas para cada bloque de texto en las preguntas
        for block in self.data["question"][0]["blocks"]:
            if block["type"] == "info":
                label = QLabel(block["text"])
                label.setStyleSheet(
                label.styleSheet() + "font-size: {}px;".format(font_size))  # Establece el tamaño de fuente
                label.setFixedHeight(70)  # Establece la altura fija de la etiqueta
                layout.addWidget(label)  # Añade la etiqueta al layout

        # Crea y añade botones de radio para cada respuesta
        for answer in self.data["question"][0]["answers"]:
            radio_button = QRadioButton(answer["text"])
            radio_button.setStyleSheet(
                radio_button.styleSheet() + "font-size: {}px;".format(font_size))  # Establece el tamaño de fuente
            radio_button.setFixedHeight(30)  # Establece la altura fija del botón de radio
            layout.addWidget(radio_button)  # Añade el botón de radio al layout
            self.radio_buttons.append(radio_button)  # Guarda el botón de radio en la lista

        # Crea y añade un botón de envío
        submit_button = QPushButton("Enviar")
        submit_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        submit_button.clicked.connect(self.check_answer)  # Conecta el botón de envío con la función check_answer
        layout.addWidget(submit_button)

        # Configura y añade la etiqueta de retroalimentación al layout
        self.feedback_label.setFixedHeight(30)
        layout.addWidget(self.feedback_label)

        # Crea un contenedor QWidget y establece su layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)  # Establece el contenedor como widget central

    # Función para guardar la respuesta del usuario en un archivo CSV
    def save_answer(self, answer_text, correct):
        with open('Respuestas_Main_Part_1.csv', mode='a', newline='') as file:
            csv_writer = csv.writer(file)

            # Si es el primer intento, escribe la información adicional en el archivo
            if self.first_attempt:
                csv_writer.writerow([])
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                csv_writer.writerow([current_time])
                elapsed_time_question = datetime.now() - self.start_time
                csv_writer.writerow(
                    ["El tiempo en Pedagogical:", self.elapsed_time_pedagogical, " El tiempo en Question:",
                     elapsed_time_question])
                self.first_attempt = False

            # Escribe la respuesta y su corrección en el archivo
            csv_writer.writerow([answer_text, correct])

    # Función para verificar y mostrar si la respuesta seleccionada es correcta o incorrecta
    def check_answer(self):
        selected_answer = None
        # Busca el botón de radio seleccionado
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                selected_answer = i
                break

        # Si se seleccionó una respuesta
        if selected_answer is not None:
            answer_text = self.data["question"][0]["answers"][selected_answer]["text"]
            correct = self.data["question"][0]["answers"][selected_answer]["correct"]

            self.save_answer(answer_text, correct)  # Guarda la respuesta en el archivo CSV

            # Muestra la retroalimentación según si la respuesta es correcta o incorrecta
            if correct:
                self.feedback_label.setText("Correcto")
                self.feedback_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px")
                self.radio_buttons[selected_answer].setStyleSheet("color: green; font-size: 14px")
            else:
                self.feedback_label.setText("Incorrecto")
                self.feedback_label.setStyleSheet("color: red; font-size: bold; font-size:")
                self.radio_buttons[selected_answer].setStyleSheet("color: red; font-size: 14px")

        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona una respuesta antes de enviar.")


# Función principal del programa
def main():
    app = QApplication(sys.argv)  # Crea una aplicación Qt

    # Abre el archivo JSON y carga los datos en la variable data1
    with open("M1-L1-Coding-Part-1.json", "r") as file:
        data1 = json.load(file)

    # Crea una instancia de la clase MainPage y le pasa los datos y el tipo de página "Pedagogical"
    main_page1 = MainPage(data1, "Pedagogical")

    main_page1.show()  # Muestra la página principal

    sys.exit(app.exec_())  # Ejecuta la aplicación y cierra cuando se cierra la ventana

# Punto de entrada del programa, llama a la función main()
if __name__ == "__main__":
    main()
