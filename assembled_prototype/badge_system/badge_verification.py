import json
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import  QLabel, QMainWindow, QVBoxLayout, QWidget

class BadgeVerification(QMainWindow):
    def __init__(self) -> None:
        super(BadgeVerification, self).__init__()

        
        joined_path = os.path.join(os.path.dirname(os.path.abspath("app.py")), "badge_system")
        file_path = joined_path + "\\badge_info.json"
        print("Antes de leer el json")
        with open("C:\\Users\\Admin\VSCode\\AI_Gamification_Python\\assembled_prototype\\badge_system\\badge_info.json", "r", encoding='utf-8') as finish_info:
            data = json.load(finish_info)
            print("Despues de leer el json")

        print(data["badge_text"])
        #Window properties
        self.setWindowTitle = data["badge_text"]
        #Layouts
        layoutV = QVBoxLayout()
      
        #Label properties
        badge = QLabel(self)
        badge.setText(data["badge_title"])
        font = QFont()
        font.setFamily(data["badge_font_family"])
        badge.setFont(font)
        font.setPointSize(data["badge_font_size"])
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setMargin(data["badge_margin"])

        label = QLabel()

        #obtener directorio del archivo actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        
        # Obtener la ruta del directorio hermano, assets
        directorio_hermano = os.path.join(directorio_actual, "..", "assets")

        #usar el directorio heramno donde esta el archuivo medal
        image_path = os.path.join(directorio_hermano, 'medal_5.jpg')
        pixmap = QPixmap(image_path)

        # Establecer la imagen en la etiqueta
        label.setPixmap(pixmap)

        # Ajustar el tamaño de la etiqueta a la imagen
        label.setFixedSize(pixmap.width(), pixmap.height())

        #Add widgets to Layouts
            #Horizontal Layout
      
        #Vertical layout
        layoutV.setSpacing(10)
        layoutV.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layoutV.addWidget(badge)
        layoutV.addWidget(label)
        #Widget/Container initialization
        widget = QWidget()
        widget.setLayout(layoutV)
        self.setCentralWidget(widget)
