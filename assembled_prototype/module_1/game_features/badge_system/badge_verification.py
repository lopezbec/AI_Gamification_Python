#badge_system/badge_verification.py
import csv
import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
app = QApplication([])
main_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class BadgeVerification(QMainWindow):
    def __init__(self) -> None:
        super(BadgeVerification, self).__init__()
        self.initUI()

    def closeEvent(self, event):
        self.hide()

    def initUI(self): 
        with open(main_directory_path + "\\badge_info.json", "r", encoding='utf-8') as finish_info:
            data = json.load(finish_info)
        #Window properties
        self.setWindowTitle(data["badge_window_title"])
        #Layouts
        layoutV = QVBoxLayout()
    
        #Label properties
        badge = QLabel(self)
        badge.setText(data["badge_text"] + "\n" + data["badge_title"])
        font = QFont()
        font.setFamily(data["badge_font_family"])
        badge.setFont(font)
        font.setPointSize(data["badge_font_size"])
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setMargin(data["badge_margin"])
        
        # close button
        accept_button = QPushButton("Aceptar")
        accept_button.setFixedSize(250, 30)
        accept_button.clicked.connect(self.closeEvent)

        frame = QFrame()
        label = QLabel(frame)

        #obtener directorio del archivo actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        
        # Obtener la ruta del directorio hermano, assets
        directorio_hermano = os.path.join(directorio_actual, "img")

        #usar el directorio heramno donde esta el archuivo medal
        image_path = os.path.join(directorio_hermano, 'medal_5.jpg')
        pixmap = QPixmap(image_path)

        frame.setFixedSize(pixmap.width(), pixmap.height())

        # Establecer la imagen en la etiqueta
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        label.setFixedSize(pixmap.width(), pixmap.height())

        #Add widgets to Layouts
            #Horizontal Layout
    
        #Vertical layout
        layoutV.setSpacing(10)
        layoutV.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutV.addWidget(badge)

        layoutV.addStretch()
        layoutV.addWidget(frame, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutV.addStretch()
        layoutV.addWidget(accept_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        #Widget/Container initialization
        widget = QWidget()
        widget.setLayout(layoutV)
        self.setCentralWidget(widget)

           

    def count_correct_answers(self, filename):

        # Abre el archivo CSV
        with open(filename) as file:
            reader = csv.reader(file)

            # Inicializa variables
            correctas_sucesivas = 0
            max_correctas_sucesivas = 0

            # Itera sobre las filas del archivo CSV
            for row in reader:
                if len(row) > 1:
                    respuesta = row[1]
                    
                    # Comprueba si es una respuesta correcta
                    if "Correct Answer Selected" in respuesta:
                        correctas_sucesivas += 1
                        if correctas_sucesivas > max_correctas_sucesivas:
                            max_correctas_sucesivas = correctas_sucesivas
                    else:
                        correctas_sucesivas = 0

        # Imprime el número máximo de respuestas correctas sucesivas
        print("El número máximo de respuestas correctas sucesivas es:", max_correctas_sucesivas)



def main():
    app = QApplication(sys.argv)

    main_page = BadgeVerification()
    main_page.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
