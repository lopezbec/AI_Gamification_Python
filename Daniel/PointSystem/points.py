import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class SoloLearnXP(QMainWindow):

    def __init__(self):
        super().__init__()

        # Llama al método para inicializar la interfaz de usuario.
        self.initUI()

    def initUI(self):

        # Establece la geometría de la ventana principal (posición x, posición y, ancho, alto).
        self.setGeometry(300, 300, 400, 300)  # Height increased to 300 to accommodate the extra button
        self.setWindowTitle('XP') #Titulo de la ventana principal

        # Crea una etiqueta para el sistema de XP.
        self.xp_label = QLabel('XP', self)
        self.xp_label.move(150, 20)

        # Crea una etiqueta para el XP actual.
        self.current_xp_label = QLabel('Current XP: 0', self)
        self.current_xp_label.move(150, 60)

        # Crea un botón para ganar XP.
        self.earn_xp_button = QPushButton('Earn XP', self)
        self.earn_xp_button.move(150, 100)
        self.earn_xp_button.clicked.connect(self.earnXP)

        # Crea una segunda etiqueta para el XP actual.
        self.current_xp_label2 = QLabel('Current XP2: 0', self)
        self.current_xp_label2.move(150, 140)  # Position adjusted to accommodate the new button

        # Crea un segundo botón para ganar XP.
        self.earn_xp_button2 = QPushButton('Earn XP 2', self)
        self.earn_xp_button2.move(150, 180)  # Position adjusted to accommodate the new button
        self.earn_xp_button2.clicked.connect(self.earnXP2)

        # Create a vertical layout to hold the labels and buttons
        xp_layout = QVBoxLayout()
        xp_layout.addWidget(self.xp_label)
        xp_layout.addWidget(self.current_xp_label)
        xp_layout.addWidget(self.earn_xp_button)
        xp_layout.addWidget(self.current_xp_label2)
        xp_layout.addWidget(self.earn_xp_button2)

        # Create a widget to hold the XP layout
        widget = QWidget()
        widget.setLayout(xp_layout)
        self.setCentralWidget(widget)

        # Muestra la ventana principal y todos sus widgets.
        self.show()

    def earnXP(self): #Este sera el earn xp de cada pregunta completada
        # Obtiene el XP actual de la etiqueta, lo incrementa en 10 y actualiza la etiqueta.
        current_xp = int(self.current_xp_label.text().split(': ')[1])
        current_xp += 1
        self.current_xp_label.setText('Current XP: {}'.format(current_xp))

    def earnXP2(self): #Este sera el Arn XP de cada lession completada
        # Similar to earnXP, but updates the second label
        current_xp2 = int(self.current_xp_label2.text().split(': ')[1])
        current_xp2 += 3
        self.current_xp_label2.setText('Current XP2: {}'.format(current_xp2))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    solo_learn_xp = SoloLearnXP()
    sys.exit(app.exec())
