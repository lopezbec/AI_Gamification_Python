import csv
import os
##import geocoder
import json
import sys
from config import Config
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMessageBox


class UserGuideDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guía de Usuario")
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Aquí va la guía de usuario...")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.styles = {}
        self.leaderboard = []
        self.levels = []

        self.load_data()

        self.theme = 'light'
        self.setWindowTitle("Tabla de Clasificación")
        self.current_user = 'Seleccionar Usuario'
        self.current_filter = 'Todos'
        self.current_order = 'Nombre (A-Z)'

        self.leaderboard_table = QtWidgets.QTableWidget(self)
        self.populate_leaderboard_table()

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.menubar = self.menuBar()
        self.setup_menus()
        # Subrayar opciones de menú al pasar el mouse
        self.menuBar().setMouseTracking(True)

        # Agregamos un título
        self.title = QtWidgets.QLabel("Tabla de Clasificación")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        theme_data = self.styles['themes'][self.theme]
        font_size = theme_data['font_size_titles']  # Obtener el tamaño de la fuente desde el archivo de estilos
        font = QtGui.QFont('Arial', font_size)  # Definir la fuente y el tamaño
        self.title.setFont(font)  # Aplicar la fuente al título
        self.title.setStyleSheet(f"background-color: {theme_data['title_background_color']}; "f"border-color: {theme_data['font_size_titles']}; "f"color: {theme_data['title_text_color']};")
        self.layout.addWidget(self.title)
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)

        self.filter_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.filter_layout)

        # self.user_combo_box = QtWidgets.QComboBox()
        # self.populate_user_combo_box()
        # self.user_combo_box.setStyleSheet(
        # f"background-color: {self.styles['themes']['light']['header_border_color']};")
        # self.user_combo_box.currentIndexChanged.connect(self.apply_user_filter)
        # self.filter_layout.addWidget(self.user_combo_box)

        self.leaderboard_table = QtWidgets.QTableWidget()
        self.layout.addWidget(self.leaderboard_table)
        self.leaderboard_table.setColumnCount(4)
        self.leaderboard_table.setHorizontalHeaderLabels(["Nombre", "Puntos", "Nivel", "Última vez activo"])
        self.leaderboard_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.apply_theme(self.theme)
        self.apply_filter('Todos')
        self.apply_order()

    def load_data(self):
        try:
            # Usa rutas de archivo relativas que apunten desde Carpeta principal a Codigos_LeaderBoard
            styles_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles_leaderboard.json")
            leaderboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")
            levels_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levels.json") 

            # Ahora, puedes cargar los archivos JSON normalmente
            with open(styles_path, encoding='utf-8') as styles_file:
                self.styles = json.load(styles_file)
            with open(leaderboard_path, encoding='utf-8') as leaderboard_file:
                self.leaderboard = json.load(leaderboard_file)
            with open(levels_path, encoding='utf-8') as levels_file:
                self.levels = json.load(levels_file)

        except FileNotFoundError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Archivo no encontrado: {e.filename}")
            sys.exit(1)
        except json.JSONDecodeError:
            QtWidgets.QMessageBox.critical(self, "Error", "Formato de archivo JSON inválido")
            sys.exit(1)

    def export_to_csv(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Guardar como...", filter="CSV files (*.csv)")
        if file_name:
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                for row in range(self.leaderboard_table.rowCount()):
                    row_data = []
                    for column in range(self.leaderboard_table.columnCount()):
                        item = self.leaderboard_table.item(row, column)
                        row_data.append(item.text())
                    writer.writerow(
                        [','.join(row_data)])  # Concatenar los valores en una sola cadena separada por comas

            QtWidgets.QMessageBox.information(self, "Éxito", "Tabla de clasificación exportada con éxito.")

    def setup_menus(self):
        file_menu = self.menubar.addMenu("Archivo")

        export_csv_action = QAction("Cargar datos a CSV", self)
        export_csv_action.triggered.connect(self.export_to_csv)

        file_menu.addAction(export_csv_action)
        file_menu.addAction("Salir", self.close)

        view_menu = self.menubar.addMenu("Ver")
        theme_menu = view_menu.addMenu("Tema")
        theme_menu.addAction("Claro", lambda: self.apply_theme('light'))
        theme_menu.addAction("Oscuro", lambda: self.apply_theme('dark'))
        """
        filter_menu = view_menu.addMenu("Filtro")
        filter_menu.addAction("Todos", lambda: self.apply_filter('Todos'))
        filter_menu.addAction("Amigos", lambda: self.apply_filter('Amigos'))
        filter_menu.addAction("País", lambda: self.apply_filter('País'))
        filter_menu.addAction("Ciudad", lambda: self.apply_filter('Ciudad'))

        order_menu = view_menu.addMenu("Orden")
        order_menu.addAction("Nombre (A-Z)", lambda: self.apply_order('Nombre (A-Z)'))
        order_menu.addAction("Nombre (Z-A)", lambda: self.apply_order('Nombre (Z-A)'))
        order_menu.addAction("Puntos (Ascendente)", lambda: self.apply_order('Puntos (Ascendente)'))
        order_menu.addAction("Puntos (Descendente)", lambda: self.apply_order('Puntos (Descendente)'))

        help_menu = self.menubar.addMenu("Ayuda")
        help_menu.addAction("Guía de Usuario", self.show_user_guide)
        """
    def filter_combo_box_changed(self, index):
        filter_type = self.filter_combo_box.currentText()
        self.apply_filter(filter_type)

    def order_combo_box_changed(self, index):
        order_type = self.order_combo_box.currentText()
        self.apply_order(order_type)

    def apply_theme(self, theme):
        try:
            theme_data = self.styles['themes'][theme]

            # Establecer el estilo general de la ventana
            self.setStyleSheet(
                f"QMainWindow {{background-color: {theme_data['main_background_color']}; color: {theme_data['text_color']};}}"
                f"QMenu {{background-color: {theme_data['menu_background_color']}; color: {theme_data['menu_text_color']};}}"
                f"QMenu::item:selected {{background-color: {theme_data['menu_item_selected_background']}; color: {theme_data['menu_item_selected_text']};}}"
            )

            # Actualizar el estilo del título
            self.title.setStyleSheet(
                f"background-color: {theme_data['title_background_color']}; "
                f"border-color: {theme_data['title_border_color']}; "
                f"color: {theme_data['title_text_color']};"
            )

            # Estilos para la tabla de clasificación y sus encabezados
            self.leaderboard_table.horizontalHeader().setStyleSheet(
                f"QHeaderView::section {{"
                f"background-color: {theme_data['header_background_color']};"
                f"color: {theme_data['text_color']};"
                f"border: 1px solid {theme_data['header_border_color']};"
                f"}}"
            )

            # Alternar colores de las filas de la tabla
            self.leaderboard_table.setAlternatingRowColors(True)
            self.leaderboard_table.setStyleSheet(
                f"QTableWidget {{"
                f"background-color: {theme_data['main_background_color']};"
                f"color: {theme_data['text_color']};"
                f"gridline-color: {theme_data['header_border_color']};"
                f"}}"
                f"QTableWidget::item {{"
                f"background-color: {theme_data['table_row_even_color']};"
                f"}}"
                f"QTableWidget::item:alternate {{"
                f"background-color: {theme_data['table_row_odd_color']};"
                f"}}"
                f"QTableWidget::item:hover {{"
                f"background-color: {theme_data['hover_background_color']};"
                f"}}"
                f"QTableWidget::item:active {{"
                f"color: {theme_data['text_color']};"
                f"}}"
            )

        except Exception as e:
            print(f"Error al aplicar el tema: {e}")
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cambiar el tema: {e}")

    def populate_user_combo_box(self):
        self.user_combo_box.clear()
        self.user_combo_box.addItem("Seleccionar Usuario")
        for user in self.leaderboard:
            self.user_combo_box.addItem(user['name'])

    def apply_user_filter(self):
        selected_user = self.user_combo_box.currentText()
        self.current_user = selected_user
        self.populate_leaderboard_table()

    # Dentro del método add_user_to_leaderboard
    def add_user_to_leaderboard(self, row, user):
        item_name = QtWidgets.QTableWidgetItem(user['name'])
        item_name.setFlags(item_name.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        item_points = QtWidgets.QTableWidgetItem(str(user['points']))
        item_points.setFlags(item_points.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        item_level = QtWidgets.QTableWidgetItem(self.get_level(user['points']))
        item_level.setFlags(item_level.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        item_last_active = QtWidgets.QTableWidgetItem(user.get('last_active', 'N/A'))
        item_last_active.setFlags(item_last_active.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        # Alineación del texto en la columna de puntos
        item_points.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item_level.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item_last_active.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item_name.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Establecer tooltip en la columna de última vez activo
        item_last_active.setToolTip(user.get('last_active', 'N/A'))

        self.leaderboard_table.setItem(row, 0, item_name)
        self.leaderboard_table.setItem(row, 1, item_points)
        self.leaderboard_table.setItem(row, 2, item_level)
        self.leaderboard_table.setItem(row, 3, item_last_active)

    def get_level(self, points):
        for level in self.levels:
            range_string = level['range']
            range_values = range_string.split("-")
            if len(range_values) == 2:
                range_min, range_max = int(range_values[0]), int(range_values[1])
                if range_min <= points <= range_max:
                    return level['name']
            elif range_string.startswith("<="):
                max_points = int(range_string[3:].strip())
                if points <= max_points:
                    return level['name']
            elif range_string.startswith(">="):
                min_points = int(range_string[3:].strip())
                if points >= min_points:
                    return level['name']
        return "N/A"

    def apply_filter(self, filter_type):
        self.current_filter = filter_type
        if self.current_filter == 'Amigos' and self.user_combo_box.currentText() == 'Seleccionar Usuario':
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione un usuario antes de aplicar el filtro de amigos.")
        elif self.current_filter == 'País' and self.user_combo_box.currentText() == 'Seleccionar Usuario':
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione un usuario antes de aplicar el filtro de país.")
        elif self.current_filter == 'Ciudad' and self.user_combo_box.currentText() == 'Seleccionar Usuario':
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione un usuario antes de aplicar el filtro de ciudad.")
        else:
            self.populate_leaderboard_table()

    def apply_order(self, order_type='Puntos (Descendente)'):
        self.current_order = order_type
        self.populate_leaderboard_table()

    def populate_leaderboard_table(self):
        self.leaderboard_table.clearContents()
        self.leaderboard_table.setRowCount(0)

        filtered_users = self.filter_leaderboard()
        ordered_users = self.order_leaderboard(filtered_users)

        self.leaderboard_table.setRowCount(len(ordered_users))
        for row, user in enumerate(ordered_users):
            self.add_user_to_leaderboard(row, user)

        # Ajustar automáticamente el ancho de la columna "Última vez activo" al contenido
        self.leaderboard_table.resizeColumnToContents(3)

    def filter_leaderboard(self):
        if self.current_filter == 'Todos':
            return self.leaderboard

        filtered_users = []
        for user in self.leaderboard:
            if self.current_filter == 'Amigos':
                if user['name'] in self.get_current_user().get('friends', []):
                    filtered_users.append(user)
            elif self.current_filter == 'País':
                if user['country'] == self.get_current_user().get('country'):
                    filtered_users.append(user)
            elif self.current_filter == 'Ciudad':
                if user['city'] == self.get_current_user().get('city'):
                    filtered_users.append(user)

        return filtered_users

    def order_leaderboard(self, users):
        if self.current_order == 'Nombre (A-Z)':
            return sorted(users, key=lambda x: x['name'])
        elif self.current_order == 'Nombre (Z-A)':
            return sorted(users, key=lambda x: x['name'], reverse=True)
        elif self.current_order == 'Puntos (Ascendente)':
            return sorted(users, key=lambda x: x['points'])
        elif self.current_order == 'Puntos (Descendente)':
            return sorted(users, key=lambda x: x['points'], reverse=True)

        return users

    def get_current_user(self):
        if self.current_user == 'Todos':
            return {}

        for user in self.leaderboard:
            if user['name'] == self.current_user:
                return user

        return {}

    def show_user_guide(self):
        dialog = UserGuideDialog(self)
        dialog.exec()

    def get_current_user_score(self):
        
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "current_user.json")) as current_user:
            data = json.load(current_user)
        
        for user in self.leaderboard:
            if user['name'] == data['current_user']:
                return int(user['points'])

def get_instance():
    return MainWindow()

def LeaderBoard():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    return app.exec()
