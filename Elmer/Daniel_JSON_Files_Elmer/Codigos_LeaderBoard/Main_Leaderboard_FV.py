import csv
import os
##import geocoder
import json
import sys
from PyQt6.QtGui import QColor
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

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.menubar = self.menuBar()
        self.setup_menus()
        self.menuBar().setMouseTracking(True)

        # Crear título
        self.create_title()

        # Crear barra de búsqueda
        self.create_search_bar()
        theme_data = self.styles['themes'][self.theme]
        self.create_refresh_button(theme_data)


        # Crear tabla
        self.leaderboard_table = QtWidgets.QTableWidget()
        self.layout.addWidget(self.leaderboard_table)
        self.leaderboard_table.setColumnCount(4)
        self.leaderboard_table.setSortingEnabled(True)
        self.leaderboard_table.setHorizontalHeaderLabels(["Nombre", "Puntos", "Nivel", "Última vez activo"])
        self.leaderboard_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Crear estadísticas
        self.create_statistics_panel()
        
        self.apply_theme(self.theme)
        self.apply_filter('Todos')
        self.apply_order()


    def create_title(self):
        # Crear el título de la ventana
        self.title = QtWidgets.QLabel("Tabla de Clasificación")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        theme_data = self.styles['themes'][self.theme]
        font_size = theme_data['font_size_titles']  # Obtener el tamaño de la fuente desde el archivo de estilos
        font = QtGui.QFont('Arial', font_size)  # Definir la fuente y el tamaño
        self.title.setFont(font)  # Aplicar la fuente al título
        self.title.setStyleSheet(
            f"background: qlineargradient("
            f"spread:pad, x1:0, y1:0, x2:1, y2:1, "
            f"stop:0 {theme_data['title_background_color']}, "
            f"stop:1 {theme_data['title_border_color']});"
            f"color: {theme_data['title_text_color']};"
            f"font-size: 20px;"
            f"font-weight: bold;"
            f"text-align: center;"
            f"padding: 15px;"
            f"border-radius: 10px;"
            f"border: 2px solid {theme_data['title_border_color']};"
        )
        self.layout.addWidget(self.title)
        
    def create_refresh_button(self, theme_data):
        # Crear layout para el botón de refrescar
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)  # Alinear a la derecha

        # Botón de refrescar
        self.refresh_button = QtWidgets.QPushButton("↻")  # Símbolo Unicode para recargar
        self.refresh_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.refresh_button.setToolTip("Refrescar tabla")  # Tooltip al pasar el mouse
        self.refresh_button.clicked.connect(self.refresh_table)

        # Estilo del botón de reiniciar
        self.refresh_button.setStyleSheet(
            f"QPushButton {{"
            f"background-color: {theme_data['continue_button_color']};"  # Color de fondo del botón
            f"color: {theme_data['text_color']};"  # Color del texto
            f"border: none;"
            f"padding: 8px;"
            f"border-radius: 8px;"
            f"font-weight: bold;"
            f"}}"
            f"QPushButton:hover {{"
            f"background-color: {theme_data['menu_item_selected_background']};"
            f"color: {theme_data['menu_item_selected_text']};"
            f"}}"
        )

        # Añadir el botón al layout
        self.button_layout.addWidget(self.refresh_button)
        self.layout.addLayout(self.button_layout)

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

    def refresh_table(self):
        try:
            # Recargar los datos desde el archivo JSON
            leaderboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")
            with open(leaderboard_path, encoding='utf-8') as leaderboard_file:
                self.leaderboard = json.load(leaderboard_file)  # Actualizar los datos en memoria

            # Actualizar la tabla con los nuevos datos
            self.populate_leaderboard_table()

            # Actualizar estadísticas
            self.update_statistics()

            # Mostrar mensaje de confirmación
            QtWidgets.QMessageBox.information(self, "Refrescar", "La tabla ha sido actualizada correctamente.")
        except Exception as e:
            # Mostrar mensaje de error si ocurre un problema
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo actualizar la tabla: {str(e)}")


    def setup_menus(self):
        # Menú Archivo
        file_menu = self.menubar.addMenu("Archivo")

        # Submenú para exportar
        export_menu = file_menu.addMenu("Exportar")

        # Opción para exportar datos a CSV
        export_csv_action = QAction("Exportar a CSV", self)
        export_csv_action.triggered.connect(self.export_to_csv)  # Conectar a la función export_to_csv
        export_menu.addAction(export_csv_action)

        # Opción para exportar datos a Excel
        export_excel_action = QAction("Exportar a Excel", self)
        export_excel_action.triggered.connect(self.export_to_excel)  # Conectar a la función export_to_excel
        export_menu.addAction(export_excel_action)

        # Opción para exportar datos a PDF
        export_pdf_action = QAction("Exportar a PDF", self)
        export_pdf_action.triggered.connect(self.export_to_pdf)  # Conectar a la función export_to_pdf
        export_menu.addAction(export_pdf_action)

        # Opción para cerrar la aplicación
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)  # Conectar al método close
        file_menu.addAction(exit_action)

        # Menú Ver
        view_menu = self.menubar.addMenu("Ver")

        # Submenú Tema
        theme_menu = view_menu.addMenu("Tema")
        light_theme_action = QAction("Claro", self)
        light_theme_action.triggered.connect(lambda: self.apply_theme('light'))  # Cambiar al tema claro
        theme_menu.addAction(light_theme_action)

        dark_theme_action = QAction("Oscuro", self)
        dark_theme_action.triggered.connect(lambda: self.apply_theme('dark'))  # Cambiar al tema oscuro
        theme_menu.addAction(dark_theme_action)


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
        
    def export_to_excel(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Guardar como...", filter="Excel files (*.xlsx)")
        if file_name:
            try:
                import pandas as pd
                # Extraer datos de la tabla
                data = []
                for row in range(self.leaderboard_table.rowCount()):
                    row_data = []
                    for column in range(self.leaderboard_table.columnCount()):
                        item = self.leaderboard_table.item(row, column)
                        row_data.append(item.text() if item else "")
                    data.append(row_data)

                # Crear un DataFrame y guardarlo como Excel
                headers = [self.leaderboard_table.horizontalHeaderItem(i).text() for i in range(self.leaderboard_table.columnCount())]
                df = pd.DataFrame(data, columns=headers)
                df.to_excel(file_name, index=False, engine='openpyxl')
                QtWidgets.QMessageBox.information(self, "Éxito", "Tabla exportada a Excel con éxito.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Error al exportar a Excel: {e}")

    def export_to_pdf(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Guardar como...", filter="PDF files (*.pdf)")
        if file_name:
            try:
                from fpdf import FPDF
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Título
                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(200, 10, txt="Tabla de Clasificación", ln=True, align="C")
                pdf.ln(10)

                # Encabezados
                pdf.set_font("Arial", style="B", size=12)
                headers = [self.leaderboard_table.horizontalHeaderItem(i).text() for i in range(self.leaderboard_table.columnCount())]
                for header in headers:
                    pdf.cell(48, 10, txt=header, border=1, align="C")
                pdf.ln()

                # Datos
                pdf.set_font("Arial", size=10)
                for row in range(self.leaderboard_table.rowCount()):
                    for column in range(self.leaderboard_table.columnCount()):
                        item = self.leaderboard_table.item(row, column)
                        pdf.cell(48, 10, txt=item.text() if item else "", border=1, align="C")
                    pdf.ln()

                # Guardar PDF
                pdf.output(file_name)
                QtWidgets.QMessageBox.information(self, "Éxito", "Tabla exportada a PDF con éxito.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Error al exportar a PDF: {e}")

        
    def create_search_bar(self):
        # Layout para la barra de búsqueda
        self.search_layout = QtWidgets.QHBoxLayout()

        # Etiqueta
        self.search_label = QtWidgets.QLabel("Buscar:")
        self.search_label.setStyleSheet("font-weight: bold;")
        self.search_layout.addWidget(self.search_label)

        # Barra de búsqueda
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Ingrese el texto para buscar...")
        self.search_bar.textChanged.connect(self.search_table)  # Conectar al método de búsqueda
        self.search_bar.setStyleSheet(
            "QLineEdit {"
            "border: 1px solid #B5E2FF;"
            "padding: 5px;"
            "border-radius: 5px;"
            "font-size: 14px;"
            "}"
            "QLineEdit:focus {"
            "border: 2px solid #00BFFF;"
            "background-color: #ECF8FF;"
            "}"
        )

        self.search_layout.addWidget(self.search_bar)

        self.layout.addLayout(self.search_layout)


    def search_table(self, text):
        # Iterar sobre todas las filas de la tabla
        for row in range(self.leaderboard_table.rowCount()):
            row_matches = False  # Indicador de si la fila tiene coincidencias

            for column in range(self.leaderboard_table.columnCount()):
                item = self.leaderboard_table.item(row, column)
                if item:
                    # Limpiar el fondo previamente establecido
                    item.setBackground(QColor("white"))

                    # Verificar coincidencias y resaltar
                    if text.lower() in item.text().lower():
                        item.setBackground(QColor("yellow"))  # Resaltar coincidencia
                        row_matches = True  # Marcar fila como coincidente

            # Ocultar filas sin coincidencias
            self.leaderboard_table.setRowHidden(row, not row_matches)

    def create_statistics_panel(self):
        # Crear un grupo para las estadísticas
        self.stats_group = QtWidgets.QGroupBox("Estadísticas")
        self.stats_group.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.stats_layout = QtWidgets.QVBoxLayout(self.stats_group)

        # Etiquetas para estadísticas
        self.total_users_label = QtWidgets.QLabel("Total de usuarios: 0")
        self.top_user_label = QtWidgets.QLabel("Usuario con más puntos: N/A")
        self.avg_points_label = QtWidgets.QLabel("Promedio de puntos: 0")

        # Agregar etiquetas al layout
        self.stats_layout.addWidget(self.total_users_label)
        self.stats_layout.addWidget(self.top_user_label)
        self.stats_layout.addWidget(self.avg_points_label)

        # Añadir el grupo de estadísticas al layout principal
        self.layout.addWidget(self.stats_group)

        # Calcular estadísticas iniciales
        self.update_statistics()
        
    def update_statistics(self):
        if not self.leaderboard:
            self.total_users_label.setText("Total de usuarios: 0")
            self.top_user_label.setText("Usuario con más puntos: N/A")
            self.avg_points_label.setText("Promedio de puntos: 0")
            return

        # Total de usuarios
        total_users = len(self.leaderboard)

        # Usuario con más puntos
        top_user = max(self.leaderboard, key=lambda x: x['points'])
        top_user_text = f"{top_user['name']} ({top_user['points']})"

        # Promedio de puntos
        avg_points = sum(user['points'] for user in self.leaderboard) / total_users

        # Actualizar las etiquetas
        self.total_users_label.setText(f"Total de usuarios: {total_users}")
        self.top_user_label.setText(f"Usuario con más puntos: {top_user_text}")
        self.avg_points_label.setText(f"Promedio de puntos: {avg_points:.2f}")



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

            # Estilo del título
            self.title.setStyleSheet(
                f"background: qlineargradient("
                f"spread:pad, x1:0, y1:0, x2:1, y2:1, "
                f"stop:0 {theme_data['title_background_color']}, "
                f"stop:1 {theme_data['title_border_color']});"
                f"color: {theme_data['title_text_color']};"
                f"font-size: 20px;"
                f"font-weight: bold;"
                f"text-align: center;"
                f"padding: 15px;"
                f"border-radius: 10px;"
                f"border: 2px solid {theme_data['title_border_color']};"
            )

            # Estilo del encabezado de la tabla
            self.leaderboard_table.horizontalHeader().setStyleSheet(
                f"QHeaderView::section {{"
                f"background-color: {theme_data['header_background_color']};"
                f"color: {theme_data['text_color']};"
                f"font-size: 14px;"
                f"font-weight: bold;"
                f"text-transform: uppercase;"  # Texto en mayúsculas
                f"border: 1px solid {theme_data['header_border_color']};"
                f"padding: 5px;"
                f"}}"
            )


            # Estilo para las celdas de la tabla
            self.leaderboard_table.setAlternatingRowColors(True)
            self.leaderboard_table.setStyleSheet(
                f"QTableWidget {{"
                f"background-color: {theme_data['main_background_color']};"
                f"color: {theme_data['text_color']};"
                f"gridline-color: {theme_data['header_border_color']};"
                f"}}"
                f"QTableWidget::item {{"
                f"background-color: {theme_data['table_row_even_color']};"
                f"color: {theme_data['text_color']};"
                f"}}"
                f"QTableWidget::item:alternate {{"
                f"background-color: {theme_data['table_row_odd_color']};"
                f"color: {theme_data['text_color']};"
                f"}}"
                f"QTableWidget::item:hover {{"
                f"background-color: {theme_data['hover_background_color']};"
                f"color: {theme_data['text_color']};"  # Asegura que el texto sea visible en hover
                f"border: 1px solid {theme_data['action_highlight_color']};"  # Borde para resaltar el hover
                f"}}"
            )
            
            # Actualizar etiquetas individuales dentro del grupo de estadísticas
            self.total_users_label.setStyleSheet(f"color: {theme_data['text_color']};")
            self.top_user_label.setStyleSheet(f"color: {theme_data['text_color']};")
            self.avg_points_label.setStyleSheet(f"color: {theme_data['text_color']};")


        except KeyError as e:
            print(f"Error al aplicar el tema: clave {e} no encontrada.")
            QMessageBox.critical(self, "Error", f"Falta la clave {e} en el tema seleccionado.")
        except Exception as e:
            print(f"Error inesperado al aplicar el tema: {e}")
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado al cambiar el tema: {e}")


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
    return window  # Retornar la ventana en lugar de ejecutar la aplicación

