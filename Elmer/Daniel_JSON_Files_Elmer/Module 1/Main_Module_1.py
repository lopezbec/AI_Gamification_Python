import sys
import os
import json
from PyQt6 import QtWidgets, QtCore, QtGui

# Ruta al directorio Leaderboard_First_Version
leaderboard_dir = os.path.join(os.path.dirname(__file__), 'Leaderboard_First_Version')

# Agregar el directorio al sys.path
sys.path.insert(0, leaderboard_dir)

# Importar los archivos necesarios
import Main_Leaderboard_FV

# Ruta a los archivos
styles_file = os.path.join(leaderboard_dir, 'styles_leaderboard.json')
levels_file = os.path.join(leaderboard_dir, 'levels.json')
leaderboard_file = os.path.join(leaderboard_dir, 'leaderboard.json')



class UserGuideDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guía de Usuario")
        self.setWindowIcon(QtGui.QIcon('guia_usuario_icon.jpeg'))  # Establece el ícono de la ventana
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Aquí va la guía de usuario...")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.styles = self.load_styles("styles.json")

        self.setWindowTitle("Mi Aplicación")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet(f"background-color: {self.styles['main_background_color']};")

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        title = QtWidgets.QLabel("Menú")
        title.setStyleSheet(f"background-color: {self.styles['title_background_color']};"
                            f"border: 1px solid {self.styles['title_border_color']};"
                            f"color: {self.styles['title_text_color']};"
                            f"font-size: {self.styles['font_size_titles']}px;")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(50)  # Esto hará que el título tenga un alto fijo de 50 píxeles
        layout.addWidget(title)

        # Añadimos los botones a nuestro layout vertical
        button_layout = QtWidgets.QHBoxLayout()

        leaderboard_btn = QtWidgets.QPushButton("Leaderboard")
        leaderboard_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        leaderboard_btn.clicked.connect(self.abrir_leaderboard)
        leaderboard_btn.setIcon(QtGui.QIcon('leaderboard_icon.png'))  # Agrega ícono al botón
        button_layout.addWidget(leaderboard_btn)

        guia_usuario_btn = QtWidgets.QPushButton("Guía de Usuario")
        guia_usuario_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")
        guia_usuario_btn.clicked.connect(self.abrir_guia_usuario)
        guia_usuario_btn.setIcon(QtGui.QIcon('guia_usuario_icon.jpeg'))  # Agrega ícono al botón
        button_layout.addWidget(guia_usuario_btn)

        lecciones_btn = QtWidgets.QToolButton()
        lecciones_btn.setText("Lecciones")
        lecciones_btn.setStyleSheet(
            f"background-color: {self.styles['submit_button_color']}; font-size: {self.styles['font_size_buttons']}px;")

        lecciones_menu = QtWidgets.QMenu()

        lecciones_menu.addAction("Lección 1", self.abrir_leccion1)

        leccion2_action = QtGui.QAction("Lección 2", lecciones_menu)
        leccion2_action.triggered.connect(self.abrir_leccion2)
        leccion2_action.setIcon(QtGui.QIcon("candado_icon.png"))
        lecciones_menu.addAction(leccion2_action)

        leccion3_action = QtGui.QAction("Lección 3", lecciones_menu)
        leccion3_action.triggered.connect(self.abrir_leccion3)
        leccion3_action.setIcon(QtGui.QIcon("candado_icon.png"))
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
        print("Abrir lección 1...")  # Aquí pondrías el código para abrir la lección 1

    def abrir_leccion2(self):
        print("Abrir lección 2...")  # Aquí pondrías el código para abrir la lección 2

    def abrir_leccion3(self):
        print("Abrir lección 3...")  # Aquí pondrías el código para abrir la lección 3

    def abrir_guia_usuario(self):
        dialog = UserGuideDialog(self)
        dialog.exec()

    def abrir_leaderboard(self):
        run_leaderboard()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()  # Esta línea hará que la ventana se muestre maximizada
    sys.exit(app.exec())

#TODO RECUERDA ARREGLAR LAS IMPORTACIONES PARA QUE SE ABRA EL LEADEARBOARD Y LAS LECCIONES CORRESPONDIENTES.
#TODO UNA VEZ ARREGLADO ESO, RECUERDA PONER A QUE SE LE VAYAN QUITANDO LOS CANDADOS SEGÚN VAYA COMPLETANDO LAS LECCIONES.