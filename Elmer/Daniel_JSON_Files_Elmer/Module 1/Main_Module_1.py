import sys
import os
import json

from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, QtCore, QtGui
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard
from LESSON_1_Codification.Main_Lesson_1 import main_lesson_1 as ml1
from LESSON_2_Working_with_Numerical_Data.Main_Lesson_2 import main_lesson_2 as ml2
from LESSON_3_Working_with_Text_Data.Main_Lesson_3 import main_lesson_3 as ml3


class UserGuideDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guía de Usuario")
        self.setWindowIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))  # Establece el ícono de la ventana
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Aquí va la guía de usuario...")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.lesson1_window = None
        self.lesson2_window = None
        self.lesson3_window = None

        self.styles = self.load_styles("styles.json")

        self.setWindowTitle("Mi Aplicación")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet(f"background-color: {self.styles['main_background_color']};")

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        title = QtWidgets.QLabel("Menú")
        title.setStyleSheet(f"background-color: {self.styles['title_background_color']};"f"border: 1px solid {self.styles['title_border_color']};"f"color: {self.styles['title_text_color']};"f"font-size: {self.styles['font_size_titles']}px;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(50)  # Esto hará que el título tenga un alto fijo de 50 píxeles
        layout.addWidget(title)

        # Añadimos los botones a nuestro layout vertical
        button_layout = QtWidgets.QHBoxLayout()

        leaderboard_btn = QtWidgets.QPushButton("Leaderboard")
        leaderboard_btn.setStyleSheet(f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        leaderboard_btn.clicked.connect(self.abrir_leaderboard)
        leaderboard_btn.setIcon(QtGui.QIcon('Icons/leaderboard_icon.png'))  # Agrega ícono al botón
        button_layout.addWidget(leaderboard_btn)

        guia_usuario_btn = QtWidgets.QPushButton("Guía de Usuario")
        guia_usuario_btn.setStyleSheet(f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        guia_usuario_btn.clicked.connect(self.abrir_guia_usuario)
        guia_usuario_btn.setIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))  # Agrega ícono al botón
        button_layout.addWidget(guia_usuario_btn)

        lecciones_btn = QtWidgets.QToolButton()
        lecciones_btn.setText("Lecciones")
        lecciones_btn.setStyleSheet(f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")

        lecciones_menu = QtWidgets.QMenu()

        lecciones_menu.addAction("Lección 1", self.abrir_leccion1)

        leccion2_action = QtGui.QAction("Lección 2", lecciones_menu)
        leccion2_action.triggered.connect(self.abrir_leccion2)
        leccion2_action.setIcon(QtGui.QIcon("Icons/candado_icon.png"))
        lecciones_menu.addAction(leccion2_action)

        leccion3_action = QtGui.QAction("Lección 3", lecciones_menu)
        leccion3_action.triggered.connect(self.abrir_leccion3)
        leccion3_action.setIcon(QtGui.QIcon("Icons/candado_icon.png"))
        lecciones_menu.addAction(leccion3_action)

        lecciones_btn.setMenu(lecciones_menu)
        lecciones_btn.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        button_layout.addWidget(lecciones_btn)

        layout.addLayout(button_layout)

    def load_styles(self, file):
        with open(file, 'r') as json_file:
            data = json.load(json_file)
        return data

    def abrir_leccion1(self):
        self.lesson1_window = ml1()

    def abrir_leccion2(self):
        self.lesson2_window = ml2()

    def abrir_leccion3(self):
        self.lesson3_window = ml3()

    def abrir_guia_usuario(self):
        dialog = UserGuideDialog(self)
        dialog.exec()

    def abrir_leaderboard(self):
        LeaderBoard()


if __name__ == "__main__":
    # Crear una instancia de QApplication
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana principal del menú
    mainWin = MainWindow()
    mainWin.showMaximized()

    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())

#TODO RECUERDA ARREGLAR LAS IMPORTACIONES PARA QUE SE ABRAN LA LECCION 3
#TODO UNA VEZ ARREGLADO ESO, RECUERDA PONER A QUE SE LE VAYAN QUITANDO LOS CANDADOS SEGÚN VAYA COMPLETANDO LAS LECCIONES.
#TODO RECUERDA ARREGLAR LO DE LOS PUNTOS, PARA QUE NO APAREZCA EL 0 DESDE QUE CAMBIA DE PAGINAS
#TODO RECUERDA TAMBIEN ARREGLAR LO DE LA PRIMERA PAGINA DE PREGUNTA EN LA LECCION 1
#TODO RECUERDA AGREGAR LO DE LOS PUNTOS LECCION 2 Y 3