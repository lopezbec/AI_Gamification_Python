import sys
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QRadioButton, QWidget, \
    QScrollArea, QMessageBox


class MainPage(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()
        self.setStyleSheet('background-color: #EDF1F5')

    def initUI(self):
        self.showMaximized()
        #self.setGeometry(100, 100, 900, 550)
        self.setWindowTitle(self.data["pedagogical"][0]["title"])
        layout = QVBoxLayout()

        for seccion in self.data['pedagogical']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet('background-color: #3572A5; border: 1px solid #3572A5; padding: 5px; font-size: 18px; color: #000000;')
            ############################################
            titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(titulo_label)

        for block in self.data["pedagogical"][0]["blocks"]:
            if block["type"] == "info":
                label = QLabel(block["text"])
                label.setStyleSheet('font-size: 17px;')
                layout.addWidget(label)
            if block["type"] == "syntax":
                label = QLabel(block["text"])
                label.setStyleSheet('background-color: #D3D3D3; border: 1px; font-size: 17px;')
                layout.addWidget(label)
            if block["type"] == "hint1":
                label = QLabel(block["text"])
                label.setStyleSheet('font-size: 17px;')
                layout.addWidget(label)
            if block["type"] == "hint":
                label = QLabel(block["text"])
                label.setStyleSheet("font-size: 15px; background-color: yellow")
                layout.addWidget(label)

        continue_button = QPushButton("Continuar")
        continue_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        continue_button.clicked.connect(self.open_question_page)
        layout.addWidget(continue_button)

        container = QWidget()
        container.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def open_question_page(self):
        self.question_page = QuestionPage(self.data)
        self.question_page.show()
        self.hide()


class QuestionPage(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()
        # Configura el estilo de fondo de la ventana
        self.setStyleSheet('background-color: #444444')

    def initUI(self):
        self.showMaximized()
        #self.setGeometry(100, 100, 900, 550)
        self.setWindowTitle(self.data["question"][0]["title"])
        layout = QVBoxLayout()

        # Crear la sección de títulos
        for seccion in self.data['question']:
            titulo_label = QLabel(seccion['title'])  # Crea un QLabel con el título de la sección actual
            titulo_label.setStyleSheet(f"background-color: #3572A5; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #000000")  # Establece el estilo del QLabel
            titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centra el texto del QLabel
            layout.addWidget(titulo_label)  # Agrega el QLabel al layout vertical

        for block in self.data["question"][0]["blocks"]:
            if block["type"] == "info":
                label = QLabel(block["text"])
                label.setStyleSheet('font-size: 17px;')
                layout.addWidget(label)

        self.radio_buttons = []
        for answer in self.data["question"][0]["answers"]:
            radio_button = QRadioButton(answer["text"])
            radio_button.setStyleSheet("font-size: 17px")
            layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        submit_button = QPushButton("Enviar")
        submit_button.setStyleSheet('font-size: 18px; color: white; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        submit_button.clicked.connect(self.check_answer)
        layout.addWidget(submit_button)

        self.feedback_label = QLabel("")
        layout.addWidget(self.feedback_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_answer(self):
        selected_answer = None
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                selected_answer = i
                break

        if selected_answer is not None:
            if self.data["question"][0]["answers"][selected_answer]["correct"]:
                self.feedback_label.setText("Correcto")
                self.feedback_label.setStyleSheet("font-size: 17px; color: green; font-weight: bold")
                self.radio_buttons[selected_answer].setStyleSheet("font-size: 17px; color: green")
            else:
                self.feedback_label.setText("Incorrecto")
                self.feedback_label.setStyleSheet("font-size: 17px; color: red; font-weight: bold")
                self.radio_buttons[selected_answer].setStyleSheet("font-size: 17px; color: red")
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona una respuesta antes de enviar.")

def main():
    app = QApplication(sys.argv)

    with open("data.json", "r", encoding='UTF-8') as file:
        data = json.load(file)

    main_page = MainPage(data)
    main_page.show()

    sys.exit(app.exec()) ###############################################

if __name__ == "__main__":
    main()