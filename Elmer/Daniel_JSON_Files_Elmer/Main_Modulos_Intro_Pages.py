import os
import sys
import json
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard
from welcome_window import WelcomeWindow
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from name_window import NameWindow
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMenu
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QAction, QIcon
from badge_system.badge_verification import save_badge_progress_per_user, create_lessons_date_completion, \
    add_user_streak_per_module
from badge_system.display_cabinet import BadgeDisplayCabinet

class UserGuideDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guía de Usuario")
        self.setWindowIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))  # Establece el ícono de la ventana
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(
            "Sistema de puntos:\nCompletar una página = 1 punto\nResponder respuesta correctamente al primer intento = 2 puntos\nResponder respuesta correctamente al segundo o más intentos = 1 punto\nFinalizar una lessión = 5 puntos")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

class Config():
    def __init__(self):
        super().__init__()

    @staticmethod
    def load_active_widgets():
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "active_widgets", "game_elements_visibility.json")) as active_widgets:
            widgets = json.load(active_widgets)
        return widgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Definir módulos con identificadores únicos
        self.modulos = {
            "modulo_1": {"nombre": "Módulo 1", "lecciones": 5},
            "modulo_2": {"nombre": "Módulo 2", "lecciones": 3},
            "modulo_3": {"nombre": "Módulo 3", "lecciones": 5},
            "modulo_4": {"nombre": "Módulo 4", "lecciones": 5},
            "modulo_5": {"nombre": "Módulo 5", "lecciones": 7}
        }

        # Inicializar las ventanas de lecciones para cada módulo
        self.m1_lesson1_window = None
        self.m1_lesson2_window = None
        self.m1_lesson3_window = None
        self.m1_lesson4_window = None
        self.m1_lesson5_window = None

        self.m2_lesson1_window = None
        self.m2_lesson2_window = None
        self.m2_lesson3_window = None

        self.m3_lesson1_window = None
        self.m3_lesson2_window = None
        self.m3_lesson3_window = None
        self.m3_lesson4_window = None
        self.m3_lesson5_window = None

        self.m4_lesson1_window = None
        self.m4_lesson2_window = None
        self.m4_lesson3_window = None
        self.m4_lesson4_window = None
        self.m4_lesson5_window = None

        self.m5_lesson1_window = None
        self.m5_lesson2_window = None
        self.m5_lesson3_window = None
        self.m5_lesson4_window = None
        self.m5_lesson5_window = None
        self.m5_lesson6_window = None
        self.m5_lesson7_window = None

        self.estado_lecciones = {}

        self.usuario_actual = self.load_current_user()  # Carga el usuario actual
        self.progreso_usuario = self.load_user_progress(self.usuario_actual)  # Carga el progreso del usuario
        self.actualizar_lecciones(self.progreso_usuario)
        save_badge_progress_per_user(self.usuario_actual)
        create_lessons_date_completion(self.usuario_actual)
        add_user_streak_per_module(self.usuario_actual)

        self.menuBar().clear()  # Limpia la barra de menús actual

        self.styles = self.load_styles(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.json"))
        self.setWindowTitle("Menú - Principal")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f"background-color: {self.styles['main_background_color']};")

        # Configura la hoja de estilos para los menús aquí
        self.setStyleSheet("""
            /* Estilo general para el menú */
            QMenu {
                background-color: #87CEEB; /* Color de fondo */
                border: none; /* Sin bordes */
            }

            /* Estilo para cada ítem del menú */
            QMenu::item {
                background-color: white; /* Color de fondo blanco para coincidir con el ícono */
            }

            /* Estilo para el ítem del menú cuando está seleccionado (hover) */
            QMenu::item:selected {
                background-color: #ADD8E6; /* Color de fondo al pasar el ratón */
                color: black; /* Color de texto */
            }
        """)

        # Configuración del widget central y layout principal
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Creación y configuración del título
        title = QtWidgets.QLabel("Menú - Módulos")
        title.setStyleSheet(
            f"background-color: {self.styles['title_background_color']};"
            f"border: 1px solid {self.styles['title_border_color']};"
            f"color: {self.styles['title_text_color']};"
            f"font-size: {self.styles['font_size_titles']}px;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(50)
        layout.addWidget(title)

        # Añadir botones de módulo debajo del título
        self.modulos_menu_widget = QtWidgets.QWidget()
        modulos_layout = QtWidgets.QHBoxLayout(self.modulos_menu_widget)

        # Configurar los botones de módulo utilizando los identificadores únicos
        self.modulo1_btn = self.setup_modulos_menu("modulo_1")
        self.modulo2_btn = self.setup_modulos_menu("modulo_2")
        self.modulo3_btn = self.setup_modulos_menu("modulo_3")
        self.modulo4_btn = self.setup_modulos_menu("modulo_4")
        self.modulo5_btn = self.setup_modulos_menu("modulo_5")

        # Añadir los botones al layout horizontal
        modulos_layout.addWidget(self.modulo1_btn)
        modulos_layout.addWidget(self.modulo2_btn)
        modulos_layout.addWidget(self.modulo3_btn)
        modulos_layout.addWidget(self.modulo4_btn)
        modulos_layout.addWidget(self.modulo5_btn)

        # Añadir el widget de módulos al layout principal
        layout.addWidget(self.modulos_menu_widget)

        # Configuración del layout para botones adicionales
        button_layout = QtWidgets.QHBoxLayout()
        button_reset_layout = QtWidgets.QVBoxLayout()

        # Botón Leaderboard
        leaderboard_btn = QtWidgets.QPushButton("Leaderboard")
        leaderboard_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        leaderboard_btn.clicked.connect(self.abrir_leaderboard)
        leaderboard_btn.setIcon(QtGui.QIcon('Icons/leaderboard_icon.png'))
        if Config.load_active_widgets().get("Leaderboard", True):
            button_layout.addWidget(leaderboard_btn)

        # Botón Guía de usuarios
        guia_usuario_btn = QtWidgets.QPushButton("Guía de usuarios")
        guia_usuario_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        guia_usuario_btn.clicked.connect(self.abrir_guia_usuario)
        guia_usuario_btn.setIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))
        button_layout.addWidget(guia_usuario_btn)

        # Botón para Vitrina (display cabinet)
        display_cabinet_btn = QtWidgets.QPushButton("Mis insignias")
        display_cabinet_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        display_cabinet_btn.clicked.connect(self.abrir_display_cabinet)
        display_cabinet_btn.setIcon(QtGui.QIcon('Icons/display_cabinet_icon.png'))
        if Config.load_active_widgets().get("display_cabinet", True):
            button_layout.addWidget(display_cabinet_btn)

        layout.addLayout(button_layout)
        layout.addLayout(button_reset_layout)

    def setup_modulos_menu(self, id_modulo):
        datos_modulo = self.modulos[id_modulo]
        modulos_btn = QtWidgets.QToolButton()
        modulos_btn.setText(datos_modulo["nombre"])
        modulos_btn.setStyleSheet(
            f"""
            background-color: {self.styles['submit_button_color']};
            font-size: {self.styles['font_size_buttons']}px;
            border: 2px solid black;
            border-radius: 10px;
            padding: 5px;
            """
        )
        modulos_btn.setFixedSize(171, 80)  # Ajusta el tamaño (ancho, alto)

        modulos_menu = QtWidgets.QMenu()
        self.añadir_submenu(id_modulo, modulos_menu)
        modulos_btn.setMenu(modulos_menu)
        modulos_btn.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)

        return modulos_btn

    def añadir_submenu(self, id_modulo, boton_modulo):
        datos_modulo = self.modulos[id_modulo]
        estado_modulo = self.progreso_usuario.get(id_modulo, {})
        estado_completado = self.load_lesson_completed(self.usuario_actual)

        for leccion_numero in range(1, datos_modulo["lecciones"] + 1):
            leccion_clave = f"Leccion{leccion_numero}"
            estado_leccion = estado_modulo.get(leccion_clave, False)

            leccion_completada = estado_completado.get(id_modulo, {}).get(f"Leccion_completada{leccion_numero}", False)

            if leccion_completada:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'completado_icon.png')
            elif estado_leccion:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'abierto_icon.png')
            else:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'cerrado_icon.jpg')

            accion_leccion = QAction(f"Lección {leccion_numero}", self)
            accion_leccion.setIcon(QIcon(icono))
            accion_leccion.triggered.connect(lambda _, n=leccion_numero, m=id_modulo: self.abrir_leccion(m, n))
            boton_modulo.addAction(accion_leccion)

        # Añadir barra de progreso al menú desplegable
        progreso = self.calcular_progreso_del_modulo(estado_modulo)
        barra_progreso = QtWidgets.QProgressBar()
        barra_progreso.setValue(progreso)
        barra_progreso.setMaximum(datos_modulo["lecciones"])
        barra_progreso.setTextVisible(True)
        barra_progreso_action = QtWidgets.QWidgetAction(self)
        barra_progreso_action.setDefaultWidget(barra_progreso)
        boton_modulo.addAction(barra_progreso_action)

    def abrir_leccion(self, id_modulo, numero_leccion):
        try:
            print(f"Intentando abrir {id_modulo} - Lección {numero_leccion}")

            # Verifica si la lección está desbloqueada
            leccion_bloqueada = not self.estado_lecciones.get(id_modulo, {}).get(f"Leccion{numero_leccion}", False)
            print(
                f"Estado de la lección {numero_leccion} en {id_modulo}: {'Bloqueada' if leccion_bloqueada else 'Desbloqueada'}")

            if leccion_bloqueada:
                self.mostrar_mensaje_bloqueado(id_modulo, numero_leccion)
                return  # Sal de la función si la lección está bloqueada

            # Si la lección está desbloqueada, procede a abrirla
            if id_modulo == "modulo_1":
                from M1_LESSON_1_Codification.M1_L1_Main import M1_L1_Main as m1l1
                from M1_LESSON_2_Working_with_Numerical_Data.M1_L2_Main import M1_L2_Main as m1l2
                from M1_LESSON_3_Working_with_Text_Data.M1_L3_Main import M1_L3_Main as m1l3
                from M1_LESSON_4_Mixing_things_up.M1_L4_Main import M1_L4_Main as m1l4
                from M1_LESSON_5_Labeling_Storing_and_Handling_Data_with_Variables.M1_L5_Main import M1_L5_Main as m1l5

                if numero_leccion == 1:
                    print("Abriendo ventana para Lección 1 del Módulo 1")
                    if not self.m1_lesson1_window:
                        self.m1_lesson1_window = m1l1()
                    self.close()
                    self.m1_lesson1_window.showMaximized()

                elif numero_leccion == 2:
                    print("Abriendo ventana para Lección 2 del Módulo 1")
                    if not self.m1_lesson2_window:
                        self.m1_lesson2_window = m1l2()
                    self.close()
                    self.m1_lesson2_window.showMaximized()

                elif numero_leccion == 3:
                    print("Abriendo ventana para Lección 3 del Módulo 1")
                    if not self.m1_lesson3_window:
                        self.m1_lesson3_window = m1l3()
                    self.close()
                    self.m1_lesson3_window.showMaximized()

                elif numero_leccion == 4:
                    print("Abriendo ventana para Lección 4 del Módulo 1")
                    if not self.m1_lesson4_window:
                        self.m1_lesson4_window = m1l4()
                    self.close()
                    self.m1_lesson4_window.showMaximized()

                elif numero_leccion == 5:
                    print("Abriendo ventana para Lección 5 del Módulo 1")
                    if not self.m1_lesson5_window:
                        self.m1_lesson5_window = m1l5()
                    self.close()
                    self.m1_lesson5_window.showMaximized()

            elif id_modulo == "modulo_2":
                print(f"Preparando lecciones del {id_modulo}")
                from M2_LESSON_1_Taking_User_Input.M2_L1_Main import M2_L1_Main as m2l1
                from M2_LESSON_2_Working_with_Input.M2_L2_Main import M2_L2_Main as m2l2
                from M2_LESSON_3_In_Place_Operators.M2_L3_Main import M2_L3_Main as m2l3

                if numero_leccion == 1:
                    print("Abriendo ventana para Lección 1 del Módulo 2")
                    if not self.m2_lesson1_window:
                        self.m2_lesson1_window = m2l1()
                    self.close()
                    self.m2_lesson1_window.showMaximized()

                elif numero_leccion == 2:
                    print("Abriendo ventana para Lección 2 del Módulo 2")
                    if not self.m2_lesson2_window:
                        self.m2_lesson2_window = m2l2()
                    self.close()
                    self.m2_lesson2_window.showMaximized()

                elif numero_leccion == 3:
                    print("Abriendo ventana para Lección 3 del Módulo 2")
                    if not self.m2_lesson3_window:
                        self.m2_lesson3_window = m2l3()
                    self.close()
                    self.m2_lesson3_window.showMaximized()

            elif id_modulo == "modulo_3":
                print(f"Preparando lecciones del {id_modulo}")
                from M3_LESSON_1_Booleans_and_Comparisons.M3_L1_Main import M3_L1_Main as m3l1
                from M3_LESSON_2_If_Statements.M3_L2_Main import M3_L2_Main as m3l2
                from M3_LESSON_3_Else_Statements.M3_L3_Main import M3_L3_Main as m3l3
                from M3_LESSON_4_Boolean_Logic.M3_L4_Main import M3_L4_Main as m3l4
                from M3_LESSON_5_while_Loops.M3_L5_Main import M3_L5_Main as m3l5

                if numero_leccion == 1:
                    print("Abriendo ventana para Lección 1 del Módulo 3")
                    if not self.m3_lesson1_window:
                        self.m3_lesson1_window = m3l1()
                    self.close()
                    self.m3_lesson1_window.showMaximized()

                elif numero_leccion == 2:
                    print("Abriendo ventana para Lección 2 del Módulo 3")
                    if not self.m3_lesson2_window:
                        self.m3_lesson2_window = m3l2()
                    self.close()
                    self.m3_lesson2_window.showMaximized()

                elif numero_leccion == 3:
                    print("Abriendo ventana para Lección 3 del Módulo 3")
                    if not self.m3_lesson3_window:
                        self.m3_lesson3_window = m3l3()
                    self.close()
                    self.m3_lesson3_window.showMaximized()

                elif numero_leccion == 4:
                    print("Abriendo ventana para Lección 4 del Módulo 3")
                    if not self.m3_lesson4_window:
                        self.m3_lesson4_window = m3l4()
                    self.close()
                    self.m3_lesson4_window.showMaximized()

                elif numero_leccion == 5:
                    print("Abriendo ventana para Lección 5 del Módulo 3")
                    if not self.m3_lesson5_window:
                        self.m3_lesson5_window = m3l5()
                    self.close()
                    self.m3_lesson5_window.showMaximized()

            elif id_modulo == "modulo_4":
                print(f"Preparando lecciones del {id_modulo}")
                from M4_LESSON_1_Lists.M4_L1_Main import M4_L1_Main as m4l1
                from M4_LESSON_2_List_Operations.M4_L2_Main import M4_L2_Main as m4l2
                from M4_LESSON_3_For_Loops.M4_L3_Main import M4_L3_Main as m4l3
                from M4_LESSON_4_Ranges.M4_L4_Main import M4_L4_Main as m4l4
                from M4_LESSON_5_List_Slices.M4_L5_Main import M4_L5_Main as m4l5

                if numero_leccion == 1:
                    print("Abriendo ventana para Lección 1 del Módulo 4")
                    if not self.m4_lesson1_window:
                        self.m4_lesson1_window = m4l1()
                    self.close()
                    self.m4_lesson1_window.showMaximized()

                elif numero_leccion == 2:
                    print("Abriendo ventana para Lección 2 del Módulo 4")
                    if not self.m4_lesson2_window:
                        self.m4_lesson2_window = m4l2()
                    self.close()
                    self.m4_lesson2_window.showMaximized()

                elif numero_leccion == 3:
                    print("Abriendo ventana para Lección 3 del Módulo 4")
                    if not self.m4_lesson3_window:
                        self.m4_lesson3_window = m4l3()
                    self.close()
                    self.m4_lesson3_window.showMaximized()

                elif numero_leccion == 4:
                    print("Abriendo ventana para Lección 4 del Módulo 4")
                    if not self.m4_lesson4_window:
                        self.m4_lesson4_window = m4l4()
                    self.close()
                    self.m4_lesson4_window.showMaximized()

                elif numero_leccion == 5:
                    print("Abriendo ventana para Lección 5 del Módulo 4")
                    if not self.m4_lesson5_window:
                        self.m4_lesson5_window = m4l5()
                    self.close()
                    self.m4_lesson5_window.showMaximized()

            elif id_modulo == "modulo_5":
                print(f"Preparando lecciones del {id_modulo}")
                from M5_LESSON_1_Functions.M5_L1_Main import M5_L1_Main as m5l1
                from M5_LESSON_2_List_Functions.M5_L2_Main import M5_L2_Main as m5l2
                from M5_LESSON_3_String_Functions.M5_L3_Main import M5_L3_Main as m5l3
                from M5_LESSON_4_Making_Your_Own_Functions.M5_L4_Main import M5_L4_Main as m5l4
                from M5_LESSON_5_Function_Arguments.M5_L5_Main import M5_L5_Main as m5l5
                from M5_LESSON_6_Returning_From_Functions.M5_L6_Main import M5_L6_Main as m5l6
                from M5_LESSON_7_Comments_and_Docstrings.M5_L7_Main import M5_L7_Main as m5l7

                if numero_leccion == 1:
                    print("Abriendo ventana para Lección 1 del Módulo 5")
                    if not self.m5_lesson1_window:
                        self.m5_lesson1_window = m5l1()
                    self.close()
                    self.m5_lesson1_window.showMaximized()

                elif numero_leccion == 2:
                    print("Abriendo ventana para Lección 2 del Módulo 5")
                    if not self.m5_lesson2_window:
                        self.m5_lesson2_window = m5l2()
                    self.close()
                    self.m5_lesson2_window.showMaximized()

                elif numero_leccion == 3:
                    print("Abriendo ventana para Lección 3 del Módulo 5")
                    if not self.m5_lesson3_window:
                        self.m5_lesson3_window = m5l3()
                    self.close()
                    self.m5_lesson3_window.showMaximized()

                elif numero_leccion == 4:
                    print("Abriendo ventana para Lección 4 del Módulo 5")
                    if not self.m5_lesson4_window:
                        self.m5_lesson4_window = m5l4()
                    self.close()
                    self.m5_lesson4_window.showMaximized()

                elif numero_leccion == 5:
                    print("Abriendo ventana para Lección 5 del Módulo 5")
                    if not self.m5_lesson5_window:
                        self.m5_lesson5_window = m5l5()
                    self.close()
                    self.m5_lesson5_window.showMaximized()

                elif numero_leccion == 6:
                    print("Abriendo ventana para Lección 6 del Módulo 5")
                    if not self.m5_lesson6_window:
                        self.m5_lesson6_window = m5l6()
                    self.close()
                    self.m5_lesson6_window.showMaximized()

                elif numero_leccion == 7:
                    print("Abriendo ventana para Lección 7 del Módulo 5")
                    if not self.m5_lesson7_window:
                        self.m5_lesson7_window = m5l7()
                    self.close()
                    self.m5_lesson7_window.showMaximized()

        except Exception as e:
            print(f"Error al abrir {id_modulo} - Lección {numero_leccion}: {e}")
            print(f"Error en línea {sys.exc_info()[2].tb_lineno}")

    @staticmethod
    def mostrar_mensaje_bloqueado(id_modulo, numero_leccion):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Lección Bloqueada")
        msg.setText(f"Lo siento, {id_modulo.replace('_', ' ')}, Lección {numero_leccion}, está bloqueado.")
        msg.exec()

    @staticmethod
    def load_lesson_completed(username):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leccion_completada.json'), 'r',
                      encoding='UTF-8') as file:
                all_users_progress = json.load(file)
            return all_users_progress.get(username, {})
        except FileNotFoundError:
            print("Archivo leccion_completada.json no encontrado.")
            return {}

    @staticmethod
    def load_current_user():
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'current_user.json'), 'r',
                      encoding='UTF-8') as file:
                user_data = json.load(file)
            return user_data.get("current_user")
        except FileNotFoundError:
            print("Archivo current_user.json no encontrado.")
            return None

    @staticmethod
    def load_user_progress(username):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progreso.json'), 'r',
                      encoding='UTF-8') as file:
                progreso = json.load(file)
            return progreso.get(username, {})
        except FileNotFoundError:
            print("Archivo progreso.json no encontrado.")
            return {}

    def actualizar_lecciones(self, estado_usuario):
        # Módulo 1
        self.estado_lecciones = {
            "modulo_1": {
                "Leccion1": estado_usuario.get("modulo_1", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("modulo_1", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("modulo_1", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("modulo_1", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("modulo_1", {}).get("Leccion5", False),
            },
            "modulo_2": {
                "Leccion1": estado_usuario.get("modulo_2", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("modulo_2", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("modulo_2", {}).get("Leccion3", False),
            },
            "modulo_3": {
                "Leccion1": estado_usuario.get("modulo_3", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("modulo_3", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("modulo_3", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("modulo_3", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("modulo_3", {}).get("Leccion5", False),
            },
            "modulo_4": {
                "Leccion1": estado_usuario.get("modulo_4", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("modulo_4", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("modulo_4", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("modulo_4", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("modulo_4", {}).get("Leccion5", False),
            },
            "modulo_5": {
                "Leccion1": estado_usuario.get("modulo_5", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("modulo_5", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("modulo_5", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("modulo_5", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("modulo_5", {}).get("Leccion5", False),
                "Leccion6": estado_usuario.get("modulo_5", {}).get("Leccion6", False),
                "Leccion7": estado_usuario.get("modulo_5", {}).get("Leccion7", False)
            }
        }

    def calcular_progreso_del_modulo(self, estado_modulo):
        lecciones_completadas = sum(estado == True for estado in estado_modulo.values())
        return lecciones_completadas

    def abrir_display_cabinet(self, username):
        self.display_cabinet = BadgeDisplayCabinet(self.usuario_actual)
        self.display_cabinet.show()

    @staticmethod
    def load_styles(file):
        with open(file, 'r') as json_file:
            data = json.load(json_file)
        return data

    def abrir_guia_usuario(self):
        dialog = UserGuideDialog(self)
        dialog.exec()

    @staticmethod
    def abrir_leaderboard():
        LeaderBoard()


def open_main_window():
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    intro_pages = WelcomeWindow()
    intro_pages.showMaximized()
    app.exec()
    open_main_window()
