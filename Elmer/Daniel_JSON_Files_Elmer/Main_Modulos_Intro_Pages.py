import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QToolButton, QMenu, QWidgetAction, QProgressBar, QMessageBox, QGridLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtWidgets, QtCore, QtGui
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
        self.setWindowIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(
            "Sistema de puntos:\nCompletar una página = 1 punto\nResponder respuesta correctamente al primer intento = 2 puntos\nResponder respuesta correctamente al segundo o más intentos = 1 punto\nFinalizar una lección = 5 puntos")
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

        self.new_instance = None
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
        self.lecciones_completadas_usuario = self.load_lesson_completed(self.usuario_actual)
        self.actualizar_lecciones(self.progreso_usuario)
        save_badge_progress_per_user(self.usuario_actual)
        create_lessons_date_completion(self.usuario_actual)
        add_user_streak_per_module(self.usuario_actual)

        self.menuBar().clear()

        self.styles = self.load_styles(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.json"))
        self.setWindowTitle("Menú - Principal")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f"background-color: {self.styles['main_background_color']};")

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QMenu {
                background-color: #87CEEB;
                border: none;
            }
            QMenu::item {
                background-color: white;
            }
            QMenu::item:selected {
                background-color: #ADD8E6;
                color: black;
            }
        """)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        title = QtWidgets.QLabel("Menú - Módulos")
        title.setStyleSheet(
            f"background-color: {self.styles['title_background_color']};"
            f"border: 1px solid {self.styles['title_border_color']};"
            f"color: {self.styles['title_text_color']};"
            f"font-size: {self.styles['font_size_titles']}px;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(50)
        layout.addWidget(title)

        self.modulos_menu_widget = QtWidgets.QWidget()
        modulos_layout = QGridLayout(self.modulos_menu_widget)

        self.modulo1_btn, self.modulo1_quiz_btn = self.setup_modulos_menu("Modulo 1", 5, 2)
        self.modulo2_btn, self.modulo2_quiz_btn = self.setup_modulos_menu("Modulo 2", 3, 2)
        self.modulo3_btn, self.modulo3_quiz_btn = self.setup_modulos_menu("Modulo 3", 5, 2)
        self.modulo4_btn, self.modulo4_quiz_btn = self.setup_modulos_menu("Modulo 4", 5, 2)
        self.modulo5_btn, self.modulo5_quiz_btn = self.setup_modulos_menu("Modulo 5", 7, 2)

        # Reorganizar los botones de los módulos y quizzes
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo1_btn, self.modulo1_quiz_btn, 0)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo2_btn, self.modulo2_quiz_btn, 1)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo3_btn, self.modulo3_quiz_btn, 2)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo4_btn, self.modulo4_quiz_btn, 3)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo5_btn, self.modulo5_quiz_btn, 4)

        layout.addWidget(self.modulos_menu_widget)

        button_layout = QtWidgets.QHBoxLayout()
        button_reset_layout = QtWidgets.QVBoxLayout()

        leaderboard_btn = QtWidgets.QPushButton("Leaderboard")
        leaderboard_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        leaderboard_btn.clicked.connect(self.abrir_leaderboard)
        leaderboard_btn.setIcon(QtGui.QIcon('Icons/leaderboard_icon.png'))
        #button_layout.addWidget(leaderboard_btn)

        guia_usuario_btn = QtWidgets.QPushButton("Guía de usuarios")
        guia_usuario_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        guia_usuario_btn.clicked.connect(self.abrir_guia_usuario)
        guia_usuario_btn.setIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))
        button_layout.addWidget(guia_usuario_btn)

        #boton para Vitrina (display cabinet)
        display_cabinet_btn = QtWidgets.QPushButton("Mis insignias")
        display_cabinet_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        display_cabinet_btn.clicked.connect(self.abrir_display_cabinet)
        display_cabinet_btn.setIcon(QtGui.QIcon('Icons/display_cabinet_icon.png'))
        #button_layout.addWidget(display_cabinet_btn)

        if Config.load_active_widgets().get("Leaderboard", True):
            button_layout.addWidget(leaderboard_btn)
        if Config.load_active_widgets().get("display_cabinet", True):
            button_layout.addWidget(display_cabinet_btn)

        layout.addLayout(button_layout)
        layout.addLayout(button_reset_layout)

    # Función para actualizar los íconos de las lecciones en la interfaz de usuario
    def update_lesson_icons(self, estado_usuario):
        for nombre_modulo, lecciones in estado_usuario.items():
            for nombre_leccion, estado in lecciones.items():
                nombre_ventana = f"m{nombre_modulo[-1]}_lesson{nombre_leccion[-1]}_window"
                ventana_leccion = getattr(self, nombre_ventana, None)

                if ventana_leccion:
                    accion_leccion = ventana_leccion.menuAction()
                    icon_path = 'Icons/cerrado_icon.jpg' if estado else 'Icons/cerrado_icon.jpg'
                    accion_leccion.setIcon(QIcon(icon_path))
                    accion_leccion.setEnabled(estado)

    def reiniciar_aplicacion(self):
        self.close()
        self.new_instance = MainWindow()
        self.new_instance.showMaximized()

    def recargar_progreso_usuario(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progreso.json'), 'r',
                      encoding='UTF-8') as file:
                progreso = json.load(file)
            self.progreso_usuario = progreso.get(self.usuario_actual, {})
            self.actualizar_lecciones(self.progreso_usuario)
            self.actualizar_quizzes()
        except Exception as e:
            print(f"Error al recargar el progreso del usuario: {e}")

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
        self.estado_lecciones = {
            "Modulo1": {
                "Leccion1": estado_usuario.get("Modulo1", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo1", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo1", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo1", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo1", {}).get("Leccion5", False),
                "Quiz1": estado_usuario.get("Modulo1", {}).get("Quiz1", False),
                "Quiz2": estado_usuario.get("Modulo1", {}).get("Quiz2", False)
            },
            "Modulo2": {
                "Leccion1": estado_usuario.get("Modulo2", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo2", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo2", {}).get("Leccion3", False),
                "Quiz1": estado_usuario.get("Modulo2", {}).get("Quiz1", False),
                "Quiz2": estado_usuario.get("Modulo2", {}).get("Quiz2", False)
            },
            "Modulo3": {
                "Leccion1": estado_usuario.get("Modulo3", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo3", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo3", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo3", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo3", {}).get("Leccion5", False),
                "Quiz1": estado_usuario.get("Modulo3", {}).get("Quiz1", False),
                "Quiz2": estado_usuario.get("Modulo3", {}).get("Quiz2", False)
            },
            "Modulo4": {
                "Leccion1": estado_usuario.get("Modulo4", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo4", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo4", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo4", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo4", {}).get("Leccion5", False),
                "Quiz1": estado_usuario.get("Modulo4", {}).get("Quiz1", False),
                "Quiz2": estado_usuario.get("Modulo4", {}).get("Quiz2", False)
            },
            "Modulo5": {
                "Leccion1": estado_usuario.get("Modulo5", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo5", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo5", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo5", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo5", {}).get("Leccion5", False),
                "Leccion6": estado_usuario.get("Modulo5", {}).get("Leccion6", False),
                "Leccion7": estado_usuario.get("Modulo5", {}).get("Leccion7", False),
                "Quiz1": estado_usuario.get("Modulo5", {}).get("Quiz1", False),
                "Quiz2": estado_usuario.get("Modulo5", {}).get("Quiz2", False)
            }
        }

    def actualizar_quizzes(self):
        for modulo, lecciones in self.estado_lecciones.items():
            for i in range(1, len(lecciones) // 2 + 1):
                if i < len(lecciones) // 2:
                    leccion_actual = f"Leccion{i}"
                    leccion_siguiente = f"Leccion{i+1}"
                    if lecciones[leccion_actual] and not lecciones[leccion_siguiente]:
                        lecciones[leccion_siguiente] = True
                else:
                    quiz_actual = f"Quiz{i - len(lecciones) // 2 + 1}"
                    if lecciones[f"Leccion{i}"] and not lecciones[quiz_actual]:
                        lecciones[quiz_actual] = True

    def desbloquear_quiz1(self, estado_modulo):
        todas_lecciones_completadas = all(estado for clave, estado in estado_modulo.items() if 'Leccion' in clave)
        return todas_lecciones_completadas

    def desbloquear_quiz2(self, estado_modulo):
        quiz1_completado = estado_modulo.get("Quiz1", False)
        return quiz1_completado

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

    def añadir_submenu(self, nombre_modulo, numero_lecciones, boton_modulo):
        # Eliminamos la creación de un submenú adicional y en su lugar
        # añadimos las acciones directamente al botón del módulo.
        estado_modulo = self.progreso_usuario.get(nombre_modulo.replace(" ", ""), {})
        estado_progreso_modulo = self.lecciones_completadas_usuario.get(nombre_modulo.replace(" ", ""), {})
        estado_completado = self.load_lesson_completed(self.usuario_actual)

        for leccion_numero in range(1, numero_lecciones + 1):
            leccion_clave = f"Leccion{leccion_numero}"
            estado_leccion = estado_modulo.get(leccion_clave, False)

            leccion_completada = estado_completado.get(nombre_modulo.replace(" ", ""), {}).get(
                f"Leccion_completada{leccion_numero}", False)
            
            if leccion_completada:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'completado_icon.png')
            elif estado_leccion:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'abierto_icon.png')
            else:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'cerrado_icon.jpg')

            accion_leccion = QAction(f"Lección {leccion_numero}", self)
            accion_leccion.setIcon(QIcon(icono))
            accion_leccion.setEnabled(estado_leccion)
            accion_leccion.triggered.connect(lambda _, n=leccion_numero, m=nombre_modulo: self.abrir_leccion(m, n))
            boton_modulo.addAction(accion_leccion)

        # Agrega una barra de progreso al final de cada menú desplegable
        progreso = self.calcular_progreso_del_modulo(estado_progreso_modulo)
        barra_progreso = QtWidgets.QProgressBar()
        barra_progreso.setValue(progreso)
        barra_progreso.setMaximum(numero_lecciones)
        barra_progreso.setTextVisible(True)
        barra_progreso_action = QWidgetAction(self)
        barra_progreso_action.setDefaultWidget(barra_progreso)
        boton_modulo.addAction(barra_progreso_action)

    def añadir_submenu_quiz(self, nombre_modulo, boton_quiz, numero_quizzes):
        estado_modulo = self.progreso_usuario.get(nombre_modulo.replace(" ", ""), {})
        estado_completado = self.load_lesson_completed(self.usuario_actual)

        for quiz_numero in range(1, numero_quizzes + 1):
            quiz_clave = f"Quiz{quiz_numero}"
            estado_quiz = estado_modulo.get(quiz_clave, False)
            quiz_completado = estado_completado.get(nombre_modulo.replace(" ", ""), {}).get(
                f"Quiz_completado{quiz_numero}", False)

            if nombre_modulo in ["Modulo 4", "Modulo 5"]:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'cerrado_icon.jpg')
                accion_quiz = QAction(f"Quiz {quiz_numero} (Muy pronto)", self)
                accion_quiz.setIcon(QIcon(icono))
                accion_quiz.setEnabled(False)
                accion_quiz.triggered.connect(
                    lambda _, n=quiz_numero, m=nombre_modulo: self.mostrar_mensaje_no_disponible(m, n))
            else:
                if quiz_numero == 1:
                    desbloqueado = self.desbloquear_quiz1(estado_modulo)
                    motivo = "por favor completa todas las lecciones."
                else:
                    desbloqueado = self.desbloquear_quiz2(estado_modulo)
                    motivo = "por favor completa el Quiz 1."

                if quiz_completado:
                    icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'completado_icon.png')
                elif desbloqueado:
                    icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'abierto_icon.png')
                else:
                    icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'cerrado_icon.jpg')

                accion_quiz = QAction(f"Quiz {quiz_numero}", self)
                accion_quiz.setIcon(QIcon(icono))
                accion_quiz.setEnabled(desbloqueado)
                accion_quiz.triggered.connect(
                    lambda _, n=quiz_numero, m=nombre_modulo, mot=motivo: self.abrir_quiz_con_motivo(m, n, mot))

            boton_quiz.addAction(accion_quiz)

    def mostrar_mensaje_no_disponible(self, nombre_modulo, numero_quiz):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Quiz No Disponible")
        msg.setText(f"Lo siento, el {nombre_modulo} - Quiz {numero_quiz} no está disponible. ¡Muy pronto!")
        msg.exec()

    def abrir_quiz_con_motivo(self, nombre_modulo, numero_quiz, motivo):
        try:
            estado_modulo = self.progreso_usuario.get(nombre_modulo.replace(" ", ""), {})
            quiz_clave = f"Quiz{numero_quiz}"
            estado_quiz = estado_modulo.get(quiz_clave, False)

            if numero_quiz == 1 and not self.desbloquear_quiz1(estado_modulo):
                self.mostrar_mensaje_bloqueado(f"{nombre_modulo} - Quiz {numero_quiz}", motivo)
                return
            elif numero_quiz == 2 and not self.desbloquear_quiz2(estado_modulo):
                self.mostrar_mensaje_bloqueado(f"{nombre_modulo} - Quiz {numero_quiz}", motivo)
                return

            quiz_mapping = {
                "Modulo 1": ["M1_Q1_Main.json", "M1_Q2_Main.json"],
                "Modulo 2": ["M2_Q1_Main.json", "M2_Q2_Main.json"],
                "Modulo 3": ["M3_Q1_Main.json", "M3_Q2_Main.json"],
                "Modulo 4": ["M4_Q1_Main.json", "M4_Q2_Main.json"],
                "Modulo 5": ["M5_Q1_Main.json", "M5_Q2_Main.json"]
            }

            if nombre_modulo in quiz_mapping and numero_quiz <= len(quiz_mapping[nombre_modulo]):
                quiz_file = quiz_mapping[nombre_modulo][numero_quiz - 1]
                quiz_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Quizzes', quiz_file)
                self.quiz_window = MMQW(quiz_path)
                self.quiz_window.showMaximized()
            else:
                print(f"Quiz {numero_quiz} no disponible para {nombre_modulo}")
        except Exception as e:
            print(f"Error al abrir {nombre_modulo} - Quiz {numero_quiz}: {e}")
            print(f"Error en línea {sys.exc_info()[2].tb_lineno}")

    def calcular_progreso_del_modulo(self, estado_modulo):
        lecciones_completadas = sum(estado == True for estado in estado_modulo.values())
        return lecciones_completadas

    def abrir_leccion(self, nombre_modulo, numero_leccion):
        try:
            from M1_LESSON_1_Codification.M1_L1_Main import M1_L1_Main as m1l1
            from M1_LESSON_2_Working_with_Numerical_Data.M1_L2_Main import M1_L2_Main as m1l2
            from M1_LESSON_3_Working_with_Text_Data.M1_L3_Main import M1_L3_Main as m1l3
            from M1_LESSON_4_Mixing_things_up.M1_L4_Main import M1_L4_Main as m1l4
            from M1_LESSON_5_Labeling_Storing_and_Handling_Data_with_Variables.M1_L5_Main import M1_L5_Main as m1l5
            from M2_LESSON_1_Taking_User_Input.M2_L1_Main import M2_L1_Main as m2l1
            from M2_LESSON_2_Working_with_Input.M2_L2_Main import M2_L2_Main as m2l2
            from M2_LESSON_3_In_Place_Operators.M2_L3_Main import M2_L3_Main as m2l3
            from M3_LESSON_1_Booleans_and_Comparisons.M3_L1_Main import M3_L1_Main as m3l1
            from M3_LESSON_2_If_Statements.M3_L2_Main import M3_L2_Main as m3l2
            from M3_LESSON_3_Else_Statements.M3_L3_Main import M3_L3_Main as m3l3
            from M3_LESSON_4_Boolean_Logic.M3_L4_Main import M3_L4_Main as m3l4
            from M3_LESSON_5_while_Loops.M3_L5_Main import M3_L5_Main as m3l5
            from M4_LESSON_1_Lists.M4_L1_Main import M4_L1_Main as m4l1
            from M4_LESSON_2_List_Operations.M4_L2_Main import M4_L2_Main as m4l2
            from M4_LESSON_3_For_Loops.M4_L3_Main import M4_L3_Main as m4l3
            from M4_LESSON_4_Ranges.M4_L4_Main import M4_L4_Main as m4l4
            from M4_LESSON_5_List_Slices.M4_L5_Main import M4_L5_Main as m4l5
            from M5_LESSON_1_Functions.M5_L1_Main import M5_L1_Main as m5l1
            from M5_LESSON_2_List_Functions.M5_L2_Main import M5_L2_Main as m5l2
            from M5_LESSON_3_String_Functions.M5_L3_Main import M5_L3_Main as m5l3
            from M5_LESSON_4_Making_Your_Own_Functions.M5_L4_Main import M5_L4_Main as m5l4
            from M5_LESSON_5_Function_Arguments.M5_L5_Main import M5_L5_Main as m5l5
            from M5_LESSON_6_Returning_From_Functions.M5_L6_Main import M5_L6_Main as m5l6
            from M5_LESSON_7_Comments_and_Docstrings.M5_L7_Main import M5_L7_Main as m5l7
            # Importar otros modulos solo necesarios en este metodo

            nombre_modulo_key = nombre_modulo.replace(" ", "")
            if self.estado_lecciones[nombre_modulo_key]["Leccion" + str(numero_leccion)]:
                if nombre_modulo == "Modulo 1":
                    if numero_leccion == 1:
                        if not self.m1_lesson1_window:
                            self.m1_lesson1_window = m1l1()
                        self.close()
                        self.m1_lesson1_window.showMaximized()
                    elif numero_leccion == 2:
                        if not self.m1_lesson2_window:
                            self.m1_lesson2_window = m1l2()
                        self.close()
                        self.m1_lesson2_window.showMaximized()
                    elif numero_leccion == 3:
                        if not self.m1_lesson3_window:
                            self.m1_lesson3_window = m1l3()
                        self.close()
                        self.m1_lesson3_window.showMaximized()
                    elif numero_leccion == 4:
                        if not self.m1_lesson4_window:
                            self.m1_lesson4_window = m1l4()
                        self.close()
                        self.m1_lesson4_window.showMaximized()
                    elif numero_leccion == 5:
                        if not self.m1_lesson5_window:
                            self.m1_lesson5_window = m1l5()
                        self.close()
                        self.m1_lesson5_window.showMaximized()
                elif nombre_modulo == "Modulo 2":
                    if numero_leccion == 1:
                        if not self.m2_lesson1_window:
                            self.m2_lesson1_window = m2l1()
                        self.close()
                        self.m2_lesson1_window.showMaximized()
                    if numero_leccion == 2:
                        if not self.m2_lesson2_window:
                            self.m2_lesson2_window = m2l2()
                        self.close()
                        self.m2_lesson2_window.showMaximized()
                    if numero_leccion == 3:
                        if not self.m2_lesson3_window:
                            self.m2_lesson3_window = m2l3()
                        self.close()
                        self.m2_lesson3_window.showMaximized()
                elif nombre_modulo == "Modulo 3":
                    if numero_leccion == 1:
                        if not self.m3_lesson1_window:
                            self.m3_lesson1_window = m3l1()
                        self.close()
                        self.m3_lesson1_window.showMaximized()
                    if numero_leccion == 2:
                        if not self.m3_lesson2_window:
                            self.m3_lesson2_window = m3l2()
                        self.close()
                        self.m3_lesson2_window.showMaximized()
                    if numero_leccion == 3:
                        if not self.m3_lesson3_window:
                            self.m3_lesson3_window = m3l3()
                        self.close()
                        self.m3_lesson3_window.showMaximized()
                    if numero_leccion == 4:
                        if not self.m3_lesson4_window:
                            self.m3_lesson4_window = m3l4()
                        self.close()
                        self.m3_lesson4_window.showMaximized()
                    if numero_leccion == 5:
                        if not self.m3_lesson5_window:
                            self.m3_lesson5_window = m3l5()
                        self.close()
                        self.m3_lesson5_window.showMaximized()
                elif nombre_modulo == "Modulo 4":
                    if numero_leccion == 1:
                        if not self.m4_lesson1_window:
                            self.m4_lesson1_window = m4l1()
                        self.close()
                        self.m4_lesson1_window.showMaximized()
                    if numero_leccion == 2:
                        if not self.m4_lesson2_window:
                            self.m4_lesson2_window = m4l2()
                        self.close()
                        self.m4_lesson2_window.showMaximized()
                    if numero_leccion == 3:
                        if not self.m4_lesson3_window:
                            self.m4_lesson3_window = m4l3()
                        self.close()
                        self.m4_lesson3_window.showMaximized()
                    if numero_leccion == 4:
                        if not self.m4_lesson4_window:
                            self.m4_lesson4_window = m4l4()
                        self.close()
                        self.m4_lesson4_window.showMaximized()
                    if numero_leccion == 5:
                        if not self.m4_lesson5_window:
                            self.m4_lesson5_window = m4l5()
                        self.close()
                        self.m4_lesson5_window.showMaximized()
                elif nombre_modulo == "Modulo 5":
                    if numero_leccion == 1:
                        if not self.m5_lesson1_window:
                            self.m5_lesson1_window = m5l1()
                        self.close()
                        self.m5_lesson1_window.showMaximized()
                    if numero_leccion == 2:
                        if not self.m5_lesson2_window:
                            self.m5_lesson2_window = m5l2()
                        self.close()
                        self.m5_lesson2_window.showMaximized()
                    if numero_leccion == 3:
                        if not self.m5_lesson3_window:
                            self.m5_lesson3_window = m5l3()
                        self.close()
                        self.m5_lesson3_window.showMaximized()
                    if numero_leccion == 4:
                        if not self.m5_lesson4_window:
                            self.m5_lesson4_window = m5l4()
                        self.close()
                        self.m5_lesson4_window.showMaximized()
                    if numero_leccion == 5:
                        if not self.m5_lesson5_window:
                            self.m5_lesson5_window = m5l5()
                        self.close()
                        self.m5_lesson5_window.showMaximized()
                    if numero_leccion == 6:
                        if not self.m5_lesson6_window:
                            self.m5_lesson6_window = m5l6()
                        self.close()
                        self.m5_lesson6_window.showMaximized()
                    if numero_leccion == 7:
                        if not self.m5_lesson7_window:
                            self.m5_lesson7_window = m5l7()
                        self.close()
                        self.m5_lesson7_window.showMaximized()
            else:
                self.mostrar_mensaje_bloqueado(f"{nombre_modulo} - Lección {numero_leccion}", "por favor completa la lección anterior.")
        except Exception as e:
            print(f"Error al abrir {nombre_modulo} - Lección {numero_leccion}: {e}")
            print(f"Error en línea {sys.exc_info()[2].tb_lineno}")

    @staticmethod
    def mostrar_mensaje_bloqueado(nombre_modulo, motivo):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Contenido Bloqueado")
        msg.setText(f"Lo siento, {nombre_modulo} está bloqueado. {motivo}")
        msg.exec()

    # Estilos de los botones del Main (Comments by Daniel)
    def setup_modulos_menu(self, nombre_modulo, numero_lecciones):
        modulos_btn = QtWidgets.QToolButton()
        modulos_btn.setText(nombre_modulo)
        modulos_btn.setStyleSheet(
            f"""
            background-color: {self.styles['submit_button_color']};
            font-size: {self.styles['font_size_buttons']}px;
            border: 2px solid black;
            border-radius: 10px;
            padding: 5px;
            """
        )
        # Para cambiar las dimensiones de los botones Modulo.
        modulos_btn.setFixedSize(171, 80)  # Ajusta el tamaño (ancho, alto) // Botones Modulo 1, Modulo 2, etc.

        quizzes_btn = QtWidgets.QToolButton()
        quizzes_btn.setText(f"Quizzes {nombre_modulo}")
        quizzes_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")

        modulos_menu = QtWidgets.QMenu()
        quizzes_menu = QtWidgets.QMenu()

        self.añadir_submenu(nombre_modulo, numero_lecciones, modulos_menu)
        self.añadir_submenu_quiz(nombre_modulo, quizzes_menu, numero_quizzes)

        modulos_btn.setMenu(modulos_menu)
        modulos_btn.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)

        return modulos_btn
    
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
