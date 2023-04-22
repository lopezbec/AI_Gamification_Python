import sys
import json
import csv

from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QRadioButton, QWidget, \
    QScrollArea, QMessageBox

app = QApplication([])


class MainPage(QMainWindow):
    def __init__(self, data, page_type):
        super().__init__()
        self.data = data  # Almacena los datos proporcionados
        self.setStyleSheet('background-color: #444444;')
        self.page_type = page_type  # Almacena el tipo de página (Pedagogical o Question)
        self.initUI()  # Llama a la función para crear la interfaz de usuario

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
            titulo_label.setStyleSheet(
                'background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
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
            continue_button.setStyleSheet(
                'font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
            continue_button.clicked.connect(
                self.open_secondary_page)  # Conecta el botón a la función open_secondary_page
            layout.addWidget(continue_button)

        container = QWidget()  # Crea un widget contenedor
        container.setLayout(layout)  # Asigna el layout al contenedor

        scroll = QScrollArea()  # Crea un área de desplazamiento
        scroll.setWidget(container)  # Añade el contenedor al área de desplazamiento
        scroll.setWidgetResizable(True)  # Habilita el redimensionamiento del widget
        self.setCentralWidget(scroll)  # Establece el área de desplazamiento como el widget central de la ventana

    # Función para abrir la página secundaria
    def open_secondary_page(self):
        self.question_page = QuestionPage(self.data)  # Crea una instancia de QuestionPage
        self.question_page.show()  # Muestra la página de preguntas
        self.hide()  # Oculta la página


# Clase QuestionPage hereda de QMainWindow
class QuestionPage(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.radio_buttons = []  # Lista para almacenar botones de opción
        self.feedback_label = QLabel("")  # Etiqueta para mostrar información de retroalimentación
        self.data = data  # Almacena los datos proporcionados
        self.setStyleSheet('background-color: #444444;')
        self.first_attempt = True  # Rastrea si es el primer intento en la sesión
        self.initUI()  # Llama a la función para crear la interfaz de usuario

    # Función para inicializar la interfaz de usuario
    def initUI(self):
        self.setGeometry(100, 100, 700, 550)  # Configura la geometría de la ventana
        self.setWindowTitle(self.data["question"][0]["title"])  # Establece el título de la ventana
        layout = QVBoxLayout()  # Crea un layout vertical
        font_size = 14

        # Crea y añade etiquetas de título para cada sección de preguntas
        for seccion in self.data['question']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet(
                'background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
            titulo_label.setFixedHeight(70)
            titulo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(titulo_label)

        # Crea y añade etiquetas para cada bloque de texto
        for block in self.data["question"][0]["blocks"]:
            if block["type"] == "info":
                label = QLabel(block["text"])
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                label.setFixedHeight(70)
                layout.addWidget(label)

        # Crea y añade botones de opción para cada respuesta
        for answer in self.data["question"][0]["answers"]:
            radio_button = QRadioButton(answer["text"])
            radio_button.setStyleSheet(radio_button.styleSheet() + "font-size: {}px;".format(font_size))
            radio_button.setFixedHeight(30)
            layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        # Crea y añade el botón de enviar
        submit_button = QPushButton("Enviar")
        submit_button.setStyleSheet(
            'font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        submit_button.clicked.connect(self.check_answer)  # Conecta el botón a la función check_answer
        layout.addWidget(submit_button)

        self.feedback_label.setFixedHeight(30)  # Establece un tamaño fijo para el bloque de feedback
        layout.addWidget(self.feedback_label)

        container = QWidget()  # Crea un widget contenedor
        container.setLayout(layout)  # Asigna el layout al contenedor
        self.setCentralWidget(container)  # Establece el contenedor como el widget central de la ventana

    def save_answer(self, answer_text, correct):
        with open('M1-L1-Coding-Part-1.csv', mode='a', newline='') as file:
            csv_writer = csv.writer(file)

            # Si es el primer intento en la sesión, escribe una línea vacía y luego la fecha y hora en el archivo CSV
            if self.first_attempt:
                csv_writer.writerow([])  # Agrega un salto de línea
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                csv_writer.writerow([current_time])
                self.first_attempt = False

            csv_writer.writerow([answer_text, correct])

    # Función para verificar la respuesta seleccionada
    def check_answer(self):
        selected_answer = None
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                selected_answer = i
                break

        # Verifica si se ha seleccionado una respuesta
        if selected_answer is not None:
            answer_text = self.data["question"][0]["answers"][selected_answer]["text"]
            correct = self.data["question"][0]["answers"][selected_answer]["correct"]

            # Guarda la respuesta en el archivo CSV
            self.save_answer(answer_text, correct)

            # Si la respuesta seleccionada es correcta, actualiza la etiqueta de retroalimentación y el estilo del botón de opción
            if correct:
                self.feedback_label.setText("Correcto")
                self.feedback_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px")
                self.radio_buttons[selected_answer].setStyleSheet("color: green; font-size: 14px")

            else:
                # Si la respuesta seleccionada es incorrecta, actualiza la etiqueta de retroalimentación y el estilo del botón de opción
                self.feedback_label.setText("Incorrecto")
                self.feedback_label.setStyleSheet("color: red; font-size: bold; font-size: 14px")
                self.radio_buttons[selected_answer].setStyleSheet("color: red; font-size: 14px")
        else:
            # Si no se ha seleccionado ninguna respuesta, muestra una advertencia al usuario
            QMessageBox.warning(self, "Advertencia", "Selecciona una respuesta antes de enviar.")

    # Función para abrir la siguiente página
    def open_next_page(self):
        self.next_page.show()  # Muestra la siguiente página
        self.hide()  # Oculta la página actual


# Función principal para ejecutar la aplicación
def main():
    app = QApplication(sys.argv)  # Crea una instancia de QApplication

    # Carga los datos del archivo JSON
    with open("M1-L1-Coding-Part-1.json", "r") as file:
        data1 = json.load(file)

    # Crea instancias de MainPage y QuestionPage
    main_page1 = MainPage(data1, "Pedagogical")

    main_page1.show()  # Muestra la página principal

    sys.exit(app.exec_())  # Ejecuta el bucle de eventos de la aplicación


window = main()
sys.exit(app.exec_())