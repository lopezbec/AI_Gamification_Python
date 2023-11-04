import sys
import os
import json

from pathlib import Path
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, QtCore, QtGui
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard
from M5_LESSON_1_Functions.M5_L1_Main import M5_L1_Main as ml1
from M5_LESSON_2_List_Functions.M5_L2_Main import M5_L2_Main as ml2
from M5_LESSON_3_String_Functions.M5_L3_Main import M5_L3_Main as ml3
from M5_LESSON_4_Making_Your_Own_Functions.M5_L4_Main import M5_L4_Main as ml4
from M5_LESSON_5_Function_Arguments.M5_L5_Main import M5_L5_Main as ml5
from M5_LESSON_6_Returning_From_Functions.M5_L6_Main import M5_L6_Main as ml6
from M5_LESSON_7_Comments_and_Docstrings.M5_L7_Main import M5_L7_Main as ml7


class Leccion:
    def __init__(self, nombre, funcion_apertura, menu, leccion_anterior=None):
        self.proxima_leccion = None
        self.nombre = nombre
        self.funcion_apertura = funcion_apertura
        self.completada = False
        self.bloqueada = leccion_anterior is not None
        self.icono_bloqueado = "Icons/cerrado_icon.jpg"
        self.icono_abierto = "Icons/abierto_icon.jpg"
        self.icono_completado = "Icons/completado_icon.png"
        self.leccion_anterior = leccion_anterior
        self.accion = QtGui.QAction(nombre, menu)
        self.accion.triggered.connect(self.abrir)
        icono_inicial = self.icono_bloqueado if self.bloqueada else self.icono_abierto
        self.accion.setIcon(QtGui.QIcon(icono_inicial))
        menu.addAction(self.accion)

    def abrir(self):
        try:
            if not self.bloqueada:
                leccion_completada = self.funcion_apertura()  # Ahora `leccion_completada` será True o False
                if leccion_completada:
                    self.completada = True
                    self.accion.setIcon(QtGui.QIcon(self.icono_completado))
                    if self.proxima_leccion:
                        self.proxima_leccion.desbloquear()
            else:
                self.mostrar_advertencia()
        except Exception as e:
            print(f"Error: {e}")

    def mostrar_advertencia(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setWindowTitle("Lección Bloqueada")
        msg.setText(f"Recuerda terminar la {self.leccion_anterior.nombre} para desbloquear esta leccion")
        msg.exec()

    def desbloquear(self):
        if self.leccion_anterior and self.leccion_anterior.completada:
            self.leccion_anterior.completada = False
            self.leccion_anterior.accion.setIcon(QtGui.QIcon(self.leccion_anterior.icono_completado))
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
            if self.lecciones[i].completada and not self.lecciones[i + 1].bloqueada:
                self.lecciones[i + 1].desbloquear()


class UserGuideDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guía de Usuario")
        self.setWindowIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))  # Establece el ícono de la ventana
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Sistema de puntos:\nCompletar una página = 1 punto\nResponder respuesta correctamente al primer intento = 2 puntos\nResponder respuesta correctamente al segundo o más intentos = 1 punto\nFinalizar una lessión = 5 puntos")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.lesson1_window = None
        self.lesson2_window = None
        self.lesson3_window = None
        self.lesson4_window = None
        self.lesson5_window = None
        self.lesson6_window = None
        self.lesson7_window = None

        self.styles = self.load_styles("styles.json")

        self.setWindowTitle("Menú - Módulo 5")
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
        self.lecciones.append(Leccion("Lección 4", self.abrir_leccion4, lecciones_menu, self.lecciones[2]))
        self.lecciones.append(Leccion("Lección 5", self.abrir_leccion5, lecciones_menu, self.lecciones[3]))
        self.lecciones.append(Leccion("Lección 6", self.abrir_leccion6, lecciones_menu, self.lecciones[4]))
        self.lecciones.append(Leccion("Lección 7", self.abrir_leccion7, lecciones_menu, self.lecciones[5]))

        self.lecciones[0].proxima_leccion = self.lecciones[1]
        self.lecciones[1].proxima_leccion = self.lecciones[2]
        self.lecciones[2].proxima_leccion = self.lecciones[3]
        self.lecciones[3].proxima_leccion = self.lecciones[4]
        self.lecciones[4].proxima_leccion = self.lecciones[5]
        self.lecciones[5].proxima_leccion = self.lecciones[6]

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
            self.curso.verificar_estado_lecciones()
            self.lesson1_window = ml1()
            return self.lesson1_window  # Retorna la ventana de la lección
        except Exception as e:
            print(f"Error al abrir la lección 1: {e}")

    def abrir_leccion2(self):
        try:
            self.lesson2_window = ml2()
            self.lesson2_window.destroyed.connect(self.curso.verificar_estado_lecciones)
            return self.lesson2_window  # Retorna la ventana de la lección
        except Exception as e:
            print(f"Error al abrir la lección 2: {e}")

    def abrir_leccion3(self):
        try:
            self.lesson3_window = ml3()
            self.lesson3_window.destroyed.connect(self.curso.verificar_estado_lecciones)
            return self.lesson3_window  # Retorna la ventana de la lección
        except Exception as e:
            print(f"Error al abrir la lección 3: {e}")

    def abrir_leccion4(self):
        try:
            self.lesson4_window = ml4()
            self.lesson4_window.destroyed.connect(self.curso.verificar_estado_lecciones)
            return self.lesson4_window  # Retorna la ventana de la lección
        except Exception as e:
            print(f"Error al abrir la lección 4: {e}")

    def abrir_leccion5(self):
        try:
            self.lesson5_window = ml5()
            self.lesson5_window.destroyed.connect(self.curso.verificar_estado_lecciones)
            return self.lesson5_window  # Retorna la ventana de la lección
        except Exception as e:
            print(f"Error al abrir la lección 5: {e}")

    def abrir_leccion6(self):
        try:
            self.lesson6_window = ml6()
            self.lesson6_window.destroyed.connect(self.curso.verificar_estado_lecciones)
            return self.lesson6_window  # Retorna la ventana de la lección
        except Exception as e:
            print(f"Error al abrir la lección 6: {e}")

    def abrir_leccion7(self):
        try:
            self.lesson7_window = ml7()
            self.lesson7_window.destroyed.connect(self.curso.verificar_estado_lecciones)
            return self.lesson7_window  # Retorna la ventana de la lección
        except Exception as e:
            print(f"Error al abrir la lección 7: {e}")

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