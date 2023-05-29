import json
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QRadioButton, QWidget, \
    QScrollArea, QMessageBox
from badge_system.badge_verification import BadgeVerification
app = QApplication(sys.argv)


class MainPage(QMainWindow):
    def __init__(self, data) -> None:
        super(MainPage, self).__init__()
        self.data = data
        self.setStyleSheet('background-color: #444444')

        self.setGeometry(100, 100, 900, 550)
        self.setWindowTitle(self.data["pedagogical"][0]["title"])
        layout = QVBoxLayout()

        for seccion in self.data['pedagogical']:
            titulo_label = QLabel(seccion['title'])
            titulo_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')
            titulo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(titulo_label)

        for block in self.data["pedagogical"][0]["blocks"]:
            if block["type"] == "info":
                label = QLabel(block["text"])
                label.setStyleSheet('font-size: 15px;')
                layout.addWidget(label)
            if block["type"] == "syntax":
                label = QLabel(block["text"])
                label.setStyleSheet('background-color: #D3D3D3; border: 1px; font-size: 15px;')
                layout.addWidget(label)
            if block["type"] == "hint1":
                label = QLabel(block["text"])
                label.setStyleSheet('font-size: 15px;')
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
        self.showMaximized()
        self.setCentralWidget(scroll)

    def open_question_page(self):
        self.question_page = QuestionPage(self.data)
        self.question_page.show()
        self.hide()


class QuestionPage(QMainWindow):
    def __init__(self, data) -> None:
        self.data = data
        super(QuestionPage, self).__init__()
        # Configura el estilo de fondo de la ventana
        self.setStyleSheet('background-color: #444444')

        self.setGeometry(100, 100, 900, 550)
        self.setWindowTitle(self.data["question"][0]["title"])
        layout = QVBoxLayout()

        # Crear la sección de títulos
        for seccion in self.data['question']:
            titulo_label = QLabel(seccion['title'])  # Crea un QLabel con el título de la sección actual
            titulo_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 5px; font-size: 18px; color: #555555;')  # Establece el estilo del QLabel
            titulo_label.setAlignment(Qt.AlignCenter)  # Centra el texto del QLabel
            layout.addWidget(titulo_label)  # Agrega el QLabel al layout vertical

        for block in self.data["question"][0]["blocks"]:
            if block["type"] == "info":
                label = QLabel(block["text"])
                label.setStyleSheet('font-size: 15px;')
                layout.addWidget(label)

        self.radio_buttons = []
        for answer in self.data["question"][0]["answers"]:
            radio_button = QRadioButton(answer["text"])
            radio_button.setStyleSheet("font-size: 15px")
            layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        submit_button = QPushButton("Enviar")
        submit_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        submit_button.clicked.connect(self.check_answer)
        layout.addWidget(submit_button)

        self.feedback_label = QLabel("")
        layout.addWidget(self.feedback_label)

        container = QWidget()
        container.setLayout(layout)
        self.showMaximized()
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
                self.feedback_label.setStyleSheet("font-size: 15px; color: green; font-weight: bold")
                self.radio_buttons[selected_answer].setStyleSheet("font-size: 15px; color: green")
                self.badge = BadgeVerification()
                self.badge.show()
            else:
                self.feedback_label.setText("Incorrecto")
                self.feedback_label.setStyleSheet("font-size: 15px; color: red; font-weight: bold")
                self.radio_buttons[selected_answer].setStyleSheet("font-size: 15px; color: red")
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona una respuesta antes de enviar.")

def main():
    app = QApplication(sys.argv)

    with open("data.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    main_page = MainPage(data)
    main_page.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
