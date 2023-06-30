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


class Leccion:
    def __init__(self, nombre, funcion_apertura, menu, leccion_anterior=None):
        self.proxima_leccion = None
        self.nombre = nombre
        self.funcion_apertura = funcion_apertura
        self.completada = False
        self.bloqueada = leccion_anterior is not None
        self.icono_bloqueado = "Icons/cerrado_icon.jpg"
        self.icono_abierto = "Icons/abierto_icon.jpg"  # Nuevo icono para las lecciones abiertas
        self.icono_completado = "Icons/completado_icon.png"
        self.leccion_anterior = leccion_anterior
        self.accion = QtGui.QAction(nombre, menu)
        self.accion.triggered.connect(self.abrir)
        icono_inicial = self.icono_bloqueado if self.bloqueada else self.icono_abierto
        self.accion.setIcon(QtGui.QIcon(icono_inicial))
        menu.addAction(self.accion)

    def abrir(self):
        if not self.bloqueada:
            self.funcion_apertura()
            self.completada = True
            self.accion.setIcon(QtGui.QIcon(self.icono_completado))
        else:
            self.mostrar_advertencia()

    def mostrar_advertencia(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setWindowTitle("Lección Bloqueada")
        msg.setText(f"Recuerda terminar la {self.leccion_anterior.nombre} para desbloquear esta leccion")
        msg.exec()

    def desbloquear(self):
        self.bloqueada = False
        self.accion.setIcon(QtGui.QIcon(self.icono_abierto))  # Actualizar el icono al desbloquear la lección

    def marcar_como_completada(self):
        self.completada = True
        self.accion.setIcon(QtGui.QIcon(self.icono_completado))
        if self.proxima_leccion:
            self.proxima_leccion.desbloquear()


class Curso:
    def __init__(self, lecciones):
        self.lecciones = lecciones
        self.lecciones[0].desbloquear()  # Desbloqueamos la primera lección al inicio

    def verificar_estado_lecciones(self):
        for i in range(len(self.lecciones) - 1):
            if self.lecciones[i].completada:
                self.lecciones[i + 1].desbloquear()


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

        self.lecciones = []
        self.lecciones.append(Leccion("Lección 1", self.abrir_leccion1, lecciones_menu))
        self.lecciones.append(Leccion("Lección 2", self.abrir_leccion2, lecciones_menu, self.lecciones[0]))
        self.lecciones.append(Leccion("Lección 3", self.abrir_leccion3, lecciones_menu, self.lecciones[1]))

        self.lecciones[0].proxima_leccion = self.lecciones[1]
        self.lecciones[1].proxima_leccion = self.lecciones[2]

        self.curso = Curso(self.lecciones)

        lecciones_btn.setMenu(lecciones_menu)
        lecciones_btn.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        button_layout.addWidget(lecciones_btn)

        layout.addLayout(button_layout)

    def load_styles(self, file):
        with open(file, 'r') as json_file:
            data = json.load(json_file)
        return data

    def abrir_leccion1(self):
        try:
            self.lesson1_window = ml1()
            self.lesson1_window.destroyed.connect(self.curso.verificar_estado_lecciones)
        except Exception as e:
            print(f"Error al abrir la lección 1: {e}")

    def abrir_leccion2(self):
        try:
            self.lesson2_window = ml2()
            self.lesson2_window.destroyed.connect(self.curso.verificar_estado_lecciones)
        except Exception as e:
            print(f"Error al abrir la lección 1: {e}")

    def abrir_leccion3(self):
        try:
            self.lesson3_window = ml3()
            self.lesson3_window.destroyed.connect(self.curso.verificar_estado_lecciones)
        except Exception as e:
            print(f"Error al abrir la lección 1: {e}")
    def abrir_guia_usuario(self):
        dialog = UserGuideDialog(self)
        dialog.exec()

    def abrir_leaderboard(self):
        LeaderBoard()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec())


#TODO RECUERDA ARREGLAR LO DEL BOTON DE REINICIAR EN LOS DRAGNADDROPS.
#TODO RECUERDA ARREGLAR LO DE LOS PUNTOS, PARA QUE NO APAREZCA EL 0 DESDE QUE CAMBIA DE PAGINAS