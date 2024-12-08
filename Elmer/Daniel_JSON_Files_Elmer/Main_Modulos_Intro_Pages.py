import os
import sys
import json
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard
from welcome_window import WelcomeWindow
from PyQt6.QtWidgets import QMessageBox, QMenu, QApplication, QToolButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QWidgetAction, QProgressBar, QGridLayout  # Se agrega QGridLayout
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6 import QtWidgets, QtCore, QtGui
from badge_system.badge_verification import save_badge_progress_per_user, create_lessons_date_completion, \
    add_user_streak_per_module
from badge_system.display_cabinet import BadgeDisplayCabinet
from Codigos_LeaderBoard.Main_Leaderboard_FV import LeaderBoard, get_instance
from PyQt6.QtCore import Qt



class UserGuideDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guía de Usuario")
        self.setWindowIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))  # Establece el ícono de la ventana
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
        leaderboard_instance = get_instance()
        self.user_score = leaderboard_instance.get_current_user_score()

        # Inicialización de módulos y configuración de lecciones
        self.new_instance = None
        self.init_modules()

        self.estado_lecciones = {}

        self.usuario_actual = self.load_current_user()
        self.progreso_usuario = self.load_user_progress(self.usuario_actual)
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

        # Configuración de la UI
        self.setup_ui()

    def init_modules(self):
        # Módulo 1
        self.m1_lesson1_window = None
        self.m1_lesson2_window = None
        self.m1_lesson3_window = None
        self.m1_lesson4_window = None
        self.m1_lesson5_window = None

        # Módulo 2
        self.m2_lesson1_window = None
        self.m2_lesson2_window = None
        self.m2_lesson3_window = None

        # Módulo 3
        self.m3_lesson1_window = None
        self.m3_lesson2_window = None
        self.m3_lesson3_window = None
        self.m3_lesson4_window = None
        self.m3_lesson5_window = None

        # Módulo 4
        self.m4_lesson1_window = None
        self.m4_lesson2_window = None
        self.m4_lesson3_window = None
        self.m4_lesson4_window = None
        self.m4_lesson5_window = None

        # Módulo 5
        self.m5_lesson1_window = None
        self.m5_lesson2_window = None
        self.m5_lesson3_window = None
        self.m5_lesson4_window = None
        self.m5_lesson5_window = None
        self.m5_lesson6_window = None
        self.m5_lesson7_window = None

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Layout para manejar la alineación del título y el nombre del usuario
        title_layout = QHBoxLayout()

        # Título del menú
        title = QLabel("Menú - Módulos")
        title.setStyleSheet(
            "background-color: #1E88E5;"
            "border: none;"
            "color: white;"
            "font-size: 24px;"
            "font-weight: bold;"
            "padding: 10px;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        title.setFixedHeight(50)

        # Nombre del usuario alineado a la derecha
        user_name = QLabel(f"Bienvenido, {self.usuario_actual}")
        user_name.setStyleSheet(
            "background-color: #1E88E5;"
            "color: white;"
            "font-size: 18px;"
            "padding-right: 15px;")
        user_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        user_name.setFixedHeight(50)

        # Agregar el título y el nombre del usuario al layout
        title_layout.addWidget(title)
        title_layout.addWidget(user_name)
        layout.addLayout(title_layout)

        self.puntos = QLabel(f"Puntuación Actual: {self.user_score}")
        self.puntos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.puntos.setStyleSheet("background-color: grey; color: white; border: 2px solid black")
        puntos_font = QFont()
        puntos_font.setPointSize(self.styles["font_size_normal"])
        self.puntos.setFont(puntos_font)
        self.puntos.setFixedHeight(60)
        self.puntos.setMargin(10)
        layout.addWidget(self.puntos)

        # Widget para los módulos
        self.modulos_menu_widget = QWidget()
        modulos_layout = QGridLayout(self.modulos_menu_widget)
        modulos_layout.setHorizontalSpacing(30)
        modulos_layout.setVerticalSpacing(30)

        self.usuario_actual = self.cargar_usuario_actual()
        self.lecciones_completadas_usuario = self.cargar_lecciones_completadas()

        # Configurar menús de módulos con estilo moderno
        self.modulo1_btn, self.modulo1_quiz_btn = self.setup_modulos_menu("Modulo 1", 5, 2, True)
        self.modulo2_btn, self.modulo2_quiz_btn = self.setup_modulos_menu("Modulo 2", 3, 3, self.is_modulo_completado("Modulo 1"))
        self.modulo3_btn, self.modulo3_quiz_btn = self.setup_modulos_menu("Modulo 3", 5, 3, self.is_modulo_completado("Modulo 2"))
        self.modulo4_btn, self.modulo4_quiz_btn = self.setup_modulos_menu("Modulo 4", 5, 3, self.is_modulo_completado("Modulo 3"))
        self.modulo5_btn, self.modulo5_quiz_btn = self.setup_modulos_menu("Modulo 5", 7, 2, self.is_modulo_completado("Modulo 4"))

        # Añadir los botones de los módulos y quizzes al layout de la cuadrícula
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo1_btn, self.modulo1_quiz_btn, 0)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo2_btn, self.modulo2_quiz_btn, 1)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo3_btn, self.modulo3_quiz_btn, 2)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo4_btn, self.modulo4_quiz_btn, 3)
        self.add_module_buttons_to_grid_layout(modulos_layout, 0, self.modulo5_btn, self.modulo5_quiz_btn, 4)

        layout.addWidget(self.modulos_menu_widget)

        # Layout horizontal para los botones inferiores
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)

        leaderboard_btn = QtWidgets.QPushButton("Leaderboard")
        leaderboard_btn.setStyleSheet(
            "background-color: #26A69A;"
            "color: white;"
            "font-size: 16px;"
            "border-radius: 15px;"
            "padding: 8px 20px;")
        leaderboard_btn.clicked.connect(self.abrir_leaderboard)
        leaderboard_btn.setIcon(QtGui.QIcon('Icons/leaderboard_icon.png'))

        guia_usuario_btn = QtWidgets.QPushButton("Guía de usuarios")
        guia_usuario_btn.setStyleSheet(
            "background-color: #26A69A;"
            "color: white;"
            "font-size: 16px;"
            "border-radius: 15px;"
            "padding: 8px 20px;")
        guia_usuario_btn.clicked.connect(self.abrir_guia_usuario)
        guia_usuario_btn.setIcon(QtGui.QIcon('Icons/guia_usuario_icon.jpeg'))

        display_cabinet_btn = QtWidgets.QPushButton("Mis insignias")
        display_cabinet_btn.setStyleSheet(
            "background-color: #26A69A;"
            "color: white;"
            "font-size: 16px;"
            "border-radius: 15px;"
            "padding: 8px 20px;")
        display_cabinet_btn.clicked.connect(self.abrir_display_cabinet)
        display_cabinet_btn.setIcon(QtGui.QIcon('Icons/display_cabinet_icon.png'))

        # Agregar botones al layout solo si están activos en la configuración
        if Config.load_active_widgets().get("Leaderboard", True):
            button_layout.addWidget(leaderboard_btn)
        if Config.load_active_widgets().get("Guía de usuarios", True):
            button_layout.addWidget(guia_usuario_btn)
        if Config.load_active_widgets().get("display_cabinet", True):
            button_layout.addWidget(display_cabinet_btn)

        layout.addLayout(button_layout)


    def cargar_usuario_actual(self):
        # Cargar el usuario actual desde el archivo JSON
        with open("current_user.json", "r") as file:
            data = json.load(file)
        return data["current_user"]

    def cargar_lecciones_completadas(self):
        # Cargar el progreso de lecciones completadas del usuario actual
        with open("leccion_completada.json", "r") as file:
            data = json.load(file)
        return data.get(self.usuario_actual, {})

    def is_modulo_completado(self, nombre_modulo):
        lecciones = self.lecciones_completadas_usuario.get(nombre_modulo, {})
        for key, value in lecciones.items():
            if not value:
                return False
        return True


    def abrir_quiz_con_motivo(self, nombre_modulo, numero_quiz, motivo):
        """En esta seccionn se maneja cual Quizz sera abierto o no 
        (esta se dispara en el metodo añadir_submenu_quiz)"""
        try:
            #importamos la ventana de los quizzzes aqui para evitar referencias circulares
            from Main_Modulos_Quizzes_Window import Main_Modulos_Quizzes_Window as MMQW
            #Obtenemos el objeto JSON del modulo en cuestion {Leccion1: true, Leccion2: false, ...}
            estado_modulo = self.progreso_usuario.get(nombre_modulo.replace(" ", ""), {})
            #Formamos la clave del quiz a mostrar (Quiz1, Quiz2)
            quiz_clave = f"Quiz{numero_quiz}"
            #Obtenemos el valor booleano de esa clave
            estado_quiz = estado_modulo.get(quiz_clave, False)

            # Si estado_quiz es false se muestra un mensaje de que este quiz esta bloqueado
            if not estado_quiz:
                self.mostrar_mensaje_bloqueado(f"{nombre_modulo} - Quiz {numero_quiz}", motivo)
                return

            #mapeo de los JSON de los quizzes
            quiz_mapping = {
                "Modulo 1": ["M1_Q1_Main.json", "M1_Q2_Main.json"],
                "Modulo 2": ["M2_Q1_Main.json", "M2_Q2_Main.json", "M2_Q3_Main.json"],
                "Modulo 3": ["M3_Q1_Main.json", "M3_Q2_Main.json", "M3_Q3_Main.json"],
                "Modulo 4": ["M4_Q1_Main.json", "M4_Q2_Main.json", "M4_Q3_Main.json"],
                "Modulo 5": ["M5_Q1_Main.json", "M5_Q2_Main.json", "M5_Q3_Main.json"]
            }

            #Comprobar si nombre_modulo es una clave en quiz mapping y, por igua, si numero_quiz
            #es menor o igual a la cantidad de quizzes disponibles en la lista correspondiente a ese módulo.
            if nombre_modulo in quiz_mapping and numero_quiz <= len(quiz_mapping[nombre_modulo]):
                #Si es asi se obtiene el quiz file del modulo correspondiente en la posición solicitada
                #NOTA: a la posicion del quiz se le resta 1 porque la primera posición de una lista es 0 
                quiz_file = quiz_mapping[nombre_modulo][numero_quiz - 1]
                #Se crea de manera dinamica la ruta absoluta del archivo quiz_file
                quiz_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Quizzes', quiz_file)
                #Se instancia la venta de Quizzes con esta ruta, el numero del quiz y el numero del modulo
                #NOTA: si el nombre modulo es "Modulo1" o "Modulo 1" con hacer nombre_modulo[-1] obtenemos el numero
                self.quiz_window = MMQW(quiz_path, numero_quiz, nombre_modulo[-1], self.usuario_actual)
                #Se muestra la ventana completa
                self.quiz_window.showMaximized()
                #Se cierra el menu principal para liberar recursos y actualizar el menu al final de cada quizz/leccion
                self.close()
            else:
                print(f"Quiz {numero_quiz} no disponible para {nombre_modulo}")       
        except Exception as e:
            print(f"Error al abrir {nombre_modulo} - Quiz {numero_quiz}: {e}")
            print(f"Error en línea {sys.exc_info()[2].tb_lineno}")



    def setup_modulos_menu(self, nombre_modulo, numero_lecciones, numero_quizzes, modulo_anterior_completado):
        modulos_btn = QToolButton()
        modulos_btn.setText(nombre_modulo)
        modulos_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;"
            "border: 2px solid black; border-radius: 10px; padding: 5px;")
        modulos_btn.setFixedSize(171, 80)

        quizzes_btn = QToolButton()
        quizzes_btn.setText(f"Quizzes {nombre_modulo}")
        quizzes_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")

        modulos_menu = QMenu()
        quizzes_menu = QMenu()

        if modulo_anterior_completado:
            self.añadir_submenu(nombre_modulo, numero_lecciones, modulos_menu)
            self.añadir_submenu_quiz(nombre_modulo, quizzes_menu, numero_quizzes)
        else:
            # Mostrar mensaje de advertencia si el módulo anterior no está completado
            modulos_btn.setEnabled(False)
            quizzes_btn.setEnabled(False)
            modulos_btn.setToolTip("Debes completar el módulo anterior para desbloquear este módulo.")
            quizzes_btn.setToolTip("Debes completar el módulo anterior para desbloquear los quizzes.")

        modulos_btn.setMenu(modulos_menu)
        modulos_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        quizzes_btn.setMenu(quizzes_menu)
        quizzes_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        return modulos_btn, quizzes_btn
        
    
    def calcular_progreso_del_modulo(self, estado_modulo):
        lecciones_completadas = sum(estado == True for estado in estado_modulo.values())
        return lecciones_completadas


    def load_lesson_completed(self, username):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leccion_completada.json'), 'r', encoding='UTF-8') as file:
                all_users_progress = json.load(file)
            return all_users_progress.get(username, {})
        except FileNotFoundError:
            print("Archivo leccion_completada.json no encontrado.")
            return {}


    def add_module_buttons_to_grid_layout(self, layout, row, modulo_btn, quizzes_btn, col):
        layout.addWidget(modulo_btn, row, col, 1, 1)
        layout.addWidget(quizzes_btn, row + 1, col, 1, 1)

    def añadir_submenu(self, nombre_modulo, numero_lecciones, boton_modulo):
        # Obtener el estado de progreso del usuario
        estado_modulo = self.progreso_usuario.get(nombre_modulo.replace(" ", ""), {})
        estado_progreso_modulo = self.lecciones_completadas_usuario.get(nombre_modulo.replace(" ", ""), {})
        estado_completado = self.load_lesson_completed(self.usuario_actual)

        # Ajustar el número de lecciones según el módulo
        if nombre_modulo == "Modulo 2":
            numero_lecciones = 3
        elif nombre_modulo == "Modulo 5":
            numero_lecciones = 7
        else:
            numero_lecciones = 5

        todas_bloqueadas = True

        # Iterar sobre las lecciones para crear acciones y establecer íconos
        for leccion_numero in range(1, numero_lecciones + 1):
            leccion_clave = f"Leccion{leccion_numero}"
            estado_leccion = estado_modulo.get(leccion_clave, False)

            leccion_completada = estado_completado.get(nombre_modulo.replace(" ", ""), {}).get(
                f"Leccion_completada{leccion_numero}", False)

            if leccion_completada or estado_leccion:
                todas_bloqueadas = False

            if leccion_completada:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'completado_icon.png')
            elif estado_leccion:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'abierto_icon.png')
            else:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'cerrado_icon.jpg')

            # Crear la acción para la lección con el ícono correspondiente
            accion_leccion = QAction(f"Lección {leccion_numero}", self)
            accion_leccion.setIcon(QIcon(icono))
            accion_leccion.triggered.connect(lambda _, n=leccion_numero, m=nombre_modulo: self.abrir_leccion(m, n))
            boton_modulo.addAction(accion_leccion)

        # Calcular y agregar la barra de progreso
        progreso = self.calcular_progreso_del_modulo(estado_progreso_modulo)
        barra_progreso = QProgressBar()
        barra_progreso.setValue(progreso)
        barra_progreso.setMaximum(numero_lecciones)
        barra_progreso.setTextVisible(True)
        barra_progreso_action = QWidgetAction(self)
        barra_progreso_action.setDefaultWidget(barra_progreso)
        boton_modulo.addAction(barra_progreso_action)

        return todas_bloqueadas


    def añadir_submenu_quiz(self, nombre_modulo, boton_quiz, numero_quizzes):
        estado_modulo = self.progreso_usuario.get(nombre_modulo.replace(" ", ""), {})
        estado_completado = self.load_lesson_completed(self.usuario_actual)

        for quiz_numero in range(1, numero_quizzes + 1):
            quiz_clave = f"Quiz{quiz_numero}"
            quiz_completado_clave = f"Quiz_completado{quiz_numero}"
            
            estado_quiz = estado_modulo.get(quiz_clave, False)
            quiz_completado = estado_completado.get(nombre_modulo.replace(" ", ""), {}).get(quiz_completado_clave, False)

            if nombre_modulo in ["Modulo 4", "Modulo 5"]:
                icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'cerrado_icon.jpg')
                accion_quiz = QAction(f"Quiz {quiz_numero} (Muy pronto)", self)
                accion_quiz.setIcon(QIcon(icono))
                accion_quiz.setEnabled(False)
                accion_quiz.triggered.connect(
                    lambda _, n=quiz_numero, m=nombre_modulo: self.mostrar_mensaje_no_disponible(m, n))
            else:
                if estado_quiz and quiz_completado:
                    icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'completado_icon.png')
                    desbloqueado = True
                elif estado_quiz and not quiz_completado:
                    icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'abierto_icon.png')
                    desbloqueado = True
                else:
                    icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons', 'cerrado_icon.jpg')
                    desbloqueado = False

                accion_quiz = QAction(f"Quiz {quiz_numero}", self)
                accion_quiz.setIcon(QIcon(icono))
                accion_quiz.setEnabled(desbloqueado)
                if desbloqueado:
                    accion_quiz.triggered.connect(
                        lambda _, n=quiz_numero, m=nombre_modulo: self.abrir_quiz_con_motivo(m, n, ""))
                else:
                    accion_quiz.triggered.connect(
                        lambda _, n=quiz_numero, m=nombre_modulo: self.mostrar_mensaje_bloqueado(f"{m} - Quiz {n}", "Completa las lecciones necesarias."))

            boton_quiz.addAction(accion_quiz)

    def abrir_display_cabinet(self, username):
        self.display_cabinet = BadgeDisplayCabinet(self.usuario_actual)
        self.display_cabinet.show()

    def abrir_leaderboard(self):
        LeaderBoard()

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
        # Modulo 1
        self.estado_lecciones = {
            "Modulo1": {
                "Leccion1": estado_usuario.get("Modulo1", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo1", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo1", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo1", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo1", {}).get("Leccion5", False),
            },
            "Modulo2": {
                "Leccion1": estado_usuario.get("Modulo2", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo2", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo2", {}).get("Leccion3", False),
            },
            "Modulo3": {
                "Leccion1": estado_usuario.get("Modulo3", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo3", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo3", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo3", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo3", {}).get("Leccion5", False),
            },
            "Modulo4": {
                "Leccion1": estado_usuario.get("Modulo4", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo4", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo4", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo4", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo4", {}).get("Leccion5", False),
            },
            "Modulo5": {
                "Leccion1": estado_usuario.get("Modulo5", {}).get("Leccion1", False),
                "Leccion2": estado_usuario.get("Modulo5", {}).get("Leccion2", False),
                "Leccion3": estado_usuario.get("Modulo5", {}).get("Leccion3", False),
                "Leccion4": estado_usuario.get("Modulo5", {}).get("Leccion4", False),
                "Leccion5": estado_usuario.get("Modulo5", {}).get("Leccion5", False),
                "Leccion6": estado_usuario.get("Modulo5", {}).get("Leccion6", False),
                "Leccion7": estado_usuario.get("Modulo5", {}).get("Leccion7", False)
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

    def abrir_leccion(self, nombre_modulo, numero_leccion):
        try:
            # Aquí mantendremos las importaciones necesarias como se manejan en ambos códigos
            # Importar Lecciones
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
                    elif numero_leccion == 2:
                        if not self.m2_lesson2_window:
                            self.m2_lesson2_window = m2l2()
                        self.close()
                        self.m2_lesson2_window.showMaximized()
                    elif numero_leccion == 3:
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
                    elif numero_leccion == 2:
                        if not self.m3_lesson2_window:
                            self.m3_lesson2_window = m3l2()
                        self.close()
                        self.m3_lesson2_window.showMaximized()
                    elif numero_leccion == 3:
                        if not self.m3_lesson3_window:
                            self.m3_lesson3_window = m3l3()
                        self.close()
                        self.m3_lesson3_window.showMaximized()
                    elif numero_leccion == 4:
                        if not self.m3_lesson4_window:
                            self.m3_lesson4_window = m3l4()
                        self.close()
                        self.m3_lesson4_window.showMaximized()
                    elif numero_leccion == 5:
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
                    elif numero_leccion == 2:
                        if not self.m4_lesson2_window:
                            self.m4_lesson2_window = m4l2()
                        self.close()
                        self.m4_lesson2_window.showMaximized()
                    elif numero_leccion == 3:
                        if not self.m4_lesson3_window:
                            self.m4_lesson3_window = m4l3()
                        self.close()
                        self.m4_lesson3_window.showMaximized()
                    elif numero_leccion == 4:
                        if not self.m4_lesson4_window:
                            self.m4_lesson4_window = m4l4()
                        self.close()
                        self.m4_lesson4_window.showMaximized()
                    elif numero_leccion == 5:
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
                    elif numero_leccion == 2:
                        if not self.m5_lesson2_window:
                            self.m5_lesson2_window = m5l2()
                        self.close()
                        self.m5_lesson2_window.showMaximized()
                    elif numero_leccion == 3:
                        if not self.m5_lesson3_window:
                            self.m5_lesson3_window = m5l3()
                        self.close()
                        self.m5_lesson3_window.showMaximized()
                    elif numero_leccion == 4:
                        if not self.m5_lesson4_window:
                            self.m5_lesson4_window = m5l4()
                        self.close()
                        self.m5_lesson4_window.showMaximized()
                    elif numero_leccion == 5:
                        if not self.m5_lesson5_window:
                            self.m5_lesson5_window = m5l5()
                        self.close()
                        self.m5_lesson5_window.showMaximized()
                    elif numero_leccion == 6:
                        if not self.m5_lesson6_window:
                            self.m5_lesson6_window = m5l6()
                        self.close()
                        self.m5_lesson6_window.showMaximized()
                    elif numero_leccion == 7:
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

    @staticmethod
    def load_styles(file):
        with open(file, 'r') as json_file:
            data = json.load(json_file)
        return data

    def abrir_guia_usuario(self):
        dialog = UserGuideDialog(self)
        dialog.exec()

    def abrir_leaderboard(self):
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
