import sys
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QButtonGroup, QRadioButton, QMessageBox


class PedagogicalWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configura el título de la ventana
        self.setWindowTitle('Pedagogical')

        # Lee los datos de un archivo JSON
        self.data = self.read_json_file('data.json')

        # Configura el estilo de fondo de la ventana
        self.setStyleSheet('background-color: #444444')

        # Obtiene los bloques de información de los datos leídos
        self.blocks = self.data['pedagogical'][0]['blocks']

        # Configura el tamaño de la ventana
        self.resize(600, 400)

        # Inicializa la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Crea un layout vertical
        vbox = QVBoxLayout()

        # Agrega una sección de título para cada sección de información en los datos
        for seccion in self.data['pedagogical']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet(
                'background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
            titulo_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(titulo_label)

        # Configura el tamaño de fuente para los bloques de información
        font_size = 14

        # Agrega un bloque de información para cada bloque en los datos
        for block in self.blocks:
            if block['type'] == 'info':
                # Agrega un label para mostrar información de texto
                label = QLabel(block['text'])
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                vbox.addWidget(label)
            elif block['type'] == 'syntax':
                # Agrega un label para mostrar información de sintaxis
                label = QLabel(block['text'])
                label.setStyleSheet('font-weight: bold; background-color: #808080;  padding: 5px; font-size: 11.5px;')
                vbox.addWidget(label)
            elif block['type'] == 'hint':
                # Agrega un label para mostrar información de ayuda
                label = QLabel(block['text'])
                label.setStyleSheet('font-size: 11.5px; background-color: {};'.format(block['background-color']))
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                vbox.addWidget(label)
            elif block['type'] == 'hint1':
                # Agrega un label para mostrar información de ayuda
                label = QLabel(block['text'])
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                vbox.addWidget(label)

        # Agrega un espaciador
        vbox.addStretch()

        # Agrega un botón para continuar a la ventana de preguntas
        continue_button = QPushButton('Continuar', self)
        continue_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        continue_button.clicked.connect(self.open_question_window)

        # Crea un layout horizontal
        hbox = QHBoxLayout()
        hbox.addStretch()  # Agrega un espacio entre los widgets
        hbox.addWidget(continue_button)  # Agrega el botón continue_button al layout

        vbox.addLayout(hbox)  # Agrega el layout horizontal al layout vertical

        widget = QWidget()
        widget.setLayout(vbox)  # Establece el layout vertical como el layout del widget
        self.setCentralWidget(widget)  # Establece el widget como widget central de la ventana principal

    def read_json_file(self, filename):
        with open(filename) as file:
            data = json.load(file)  # Carga los datos del archivo JSON en un diccionario
        return data

    def open_question_window(self):
        self.question_window = QuestionWindow(self)  # Crea una nueva instancia de la clase QuestionWindow
        self.question_window.show()  # Muestra la ventana
        self.hide()  # Oculta la ventana actual

class QuestionWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Question')  # Establece el título de la ventana
        self.parent = parent
        self.data = self.read_json_file('data.json')  # Carga los datos del archivo JSON en un diccionario
        self.blocks = self.data['question'][0]['blocks']  # Obtiene los bloques de preguntas del diccionario
        self.init_ui()

    def init_ui(self):
        # Crear el diseño de la ventana
        vbox = QVBoxLayout()  # Crea un layout vertical

        # Crear la sección de títulos
        for seccion in self.data['question']:
            titulo_label = QLabel(seccion['title'])  # Crea un QLabel con el título de la sección actual
            titulo_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')  # Establece el estilo del QLabel
            titulo_label.setAlignment(Qt.AlignCenter)  # Centra el texto del QLabel
            vbox.addWidget(titulo_label)  # Agrega el QLabel al layout vertical

        # Crear la sección de preguntas
        vbox_questions = QVBoxLayout()  # Crea un layout vertical para las preguntas

        font_size = 14  # Establece el tamaño de fuente

        for block in self.blocks:
            if block['type'] == 'info':
                label = QLabel(block['text'])  # Crea un QLabel con el texto del bloque
                label.setStyleSheet(
                    label.styleSheet() + "font-size: {}px;".format(font_size))  # Establece el estilo del QLabel
                vbox_questions.addWidget(label)  # Agrega el QLabel al layout vertical para las preguntas

        vbox.addLayout(vbox_questions)  # Agrega el layout vertical para las preguntas al layout vertical principal

        # Crear los radio buttons
        self.radio_button_list = []
        for answer in self.data['question'][0]['answers']:
            radio_button = QRadioButton(answer['text'])  # Crea un QRadioButton con el texto de la respuesta
            radio_button.setStyleSheet(
                'font-weight: bold; background-color: #808080;  padding: 5px; font-size: 11.5px;')  # Establece el estilo del QRadioButton
            radio_button.clicked.connect(lambda checked, ans=answer: self.check_answer1(
                ans))  # Conecta la señal clicked del QRadioButton a la función check_answer1, pasando la respuesta como argumento
            vbox.addWidget(radio_button)  # Agrega el QRadioButton al layout vertical principal
            self.radio_button_list.append(radio_button)  # Agrega el QRadioButton a una lista de radio buttons

        vbox.addStretch()  # Agrega un espacio entre los radio buttons y el botón Enviar

        # Crear el botón Enviar
        send_button = QPushButton('Enviar', self)  # Crea un QPushButton con el texto 'Enviar'
        send_button.setStyleSheet(
            'font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')  # Establece el estilo del QPushButton
        send_button.clicked.connect(
            self.check_answer)  # Conecta la señal clicked del QPushButton a la función check_answer

        hbox = QHBoxLayout()  # Crea un layout horizontal
        hbox.addStretch()  # Agrega un espacio entre el QPushButton y el borde de la ventana
        hbox.addWidget(send_button)  # Agrega el QPushButton al layout horizontal

        vbox.addLayout(hbox)  # Agrega el layout horizontal al layout vertical principal

        widget = QWidget()
        widget.setLayout(vbox)  # Establece el layout vertical principal como el layout del widget
        self.setCentralWidget(widget)  # Establece el widget como widget central de la ventana principal

    def read_json_file(self, filename):
        # Abre y carga el archivo JSON en una variable "data" utilizando el módulo "json"
        with open(filename) as file:
            data = json.load(file)
        # Devuelve la variable "data"
        return data

    def closeEvent(self, event):
        # Cierra la ventana principal cuando se presiona el botón de cerrar ventana
        self.parent.close()
        event.accept()

    def check_answer1(self, selected_answer):
        if selected_answer['correct']:
            # Si la respuesta es correcta, establece el mensaje como "Correcto!"
            self.message = '¡Correcto!'
        else:
            # Si la respuesta es incorrecta, establece el mensaje como "Incorrecto!"
            self.message = 'Incorrecto!'

    def check_answer(self):
        # Crea un objeto de QMessageBox
        msg_box = QMessageBox()

        # Configura el mensaje y los botones del objeto QMessageBox
        msg_box.setText(self.message)
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Muestra la ventana emergente y espera a que el usuario cierre la ventana
        msg_box.exec_()

        # Sale de la aplicación
        app.quit()

if __name__ == '__main__':
    # Crea una instancia de QApplication y una ventana principal
    app = QApplication(sys.argv)
    pedagogical_window = PedagogicalWindow()

    # Muestra la ventana principal
    pedagogical_window.show()

    # Ejecuta el ciclo principal de la aplicación
    sys.exit(app.exec_())

