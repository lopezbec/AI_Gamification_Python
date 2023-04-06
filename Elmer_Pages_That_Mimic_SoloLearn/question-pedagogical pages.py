import sys
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QButtonGroup, QRadioButton, QMessageBox


class PedagogicalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pedagogical')
        self.data = self.read_json_file('data.json')
        self.setStyleSheet('background-color: #444444')
        self.blocks = self.data['pedagogical'][0]['blocks']
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        for seccion in self.data['pedagogical']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
            titulo_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(titulo_label)

        font_size = 14

        for block in self.blocks:
            if block['type'] == 'info':
                label = QLabel(block['text'])
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                vbox.addWidget(label)
            elif block['type'] == 'syntax':
                label = QLabel(block['text'])
                label.setStyleSheet('font-weight: bold; background-color: #808080;  padding: 5px; font-size: 11.5px;')
                vbox.addWidget(label)
            elif block['type'] == 'hint':
                label = QLabel(block['text'])
                label.setStyleSheet('font-size: 11.5px; background-color: {};'.format(block['background-color']))
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                vbox.addWidget(label)
            elif block['type'] == 'hint1':
                label = QLabel(block['text'])
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                vbox.addWidget(label)

        vbox.addStretch()

        continue_button = QPushButton('Continuar', self)
        continue_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        continue_button.clicked.connect(self.open_question_window)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(continue_button)

        vbox.addLayout(hbox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def read_json_file(self, filename):
        with open(filename) as file:
            data = json.load(file)
        return data

    def open_question_window(self):
        self.question_window = QuestionWindow(self)
        self.question_window.show()
        self.hide()


class QuestionWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Question')
        self.parent = parent
        self.data = self.read_json_file('data.json')
        self.blocks = self.data['question'][0]['blocks']
        self.init_ui()

    def init_ui(self):
        # Crear el diseño de la ventana
        vbox = QVBoxLayout()

        # Crear la sección de títulos
        for seccion in self.data['question']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
            titulo_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(titulo_label)

        # Crear la sección de preguntas
        vbox_questions = QVBoxLayout()

        font_size = 14

        for block in self.blocks:
            if block['type'] == 'info':
                label = QLabel(block['text'])
                label.setStyleSheet(label.styleSheet() + "font-size: {}px;".format(font_size))
                vbox_questions.addWidget(label)

        vbox.addLayout(vbox_questions)

        # Crear los radio buttons
        self.radio_button_list = []
        for answer in self.data['question'][0]['answers']:
            radio_button = QRadioButton(answer['text'])
            radio_button.setStyleSheet('font-weight: bold; background-color: #808080;  padding: 5px; font-size: 11.5px;')
            radio_button.clicked.connect(lambda checked, ans=answer: self.check_answer1(ans))
            vbox.addWidget(radio_button)
            self.radio_button_list.append(radio_button)

        vbox.addStretch()

        # Crear el botón Enviar
        send_button = QPushButton('Enviar', self)
        send_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        send_button.clicked.connect(self.check_answer)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(send_button)

        vbox.addLayout(hbox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def read_json_file(self, filename):
        with open(filename) as file:
            data = json.load(file)
        return data

    def closeEvent(self, event):
        self.parent.close()
        event.accept()

    def check_answer1(self, selected_answer):
        if selected_answer['correct']:
            self.message = '¡Correcto!'
        else:
            self.message = 'Incorrecto!'

    def check_answer(self):
        # Crear un objeto de QMessageBox
        msg_box = QMessageBox()

        # Configurar el mensaje y los botones
        msg_box.setText(self.message)
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Mostrar la ventana emergente y esperar a que el usuario cierre la ventana
        msg_box.exec_()

        # Salir de la aplicación
        app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pedagogical_window = PedagogicalWindow()
    pedagogical_window.show()
    sys.exit(app.exec_())
