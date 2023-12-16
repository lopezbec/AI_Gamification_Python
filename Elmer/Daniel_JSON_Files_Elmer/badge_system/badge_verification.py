import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import  QLabel, QMainWindow, QVBoxLayout, QWidget
sys.path.append(r"C:\Users\Admin\VSCode\AI_Gamification_Python")

class BadgeVerification(QMainWindow):
    def __init__(self) -> None:
        super(BadgeVerification, self).__init__()


        with open("badge_info.json", "r") as finish_info:
            data = json.load(finish_info)

        #Window properties
        self.setWindowTitle = data["badge_text"]
        #Layouts
        layoutV = QVBoxLayout()
      
        #Label properties
        badge = QLabel(self)
        badge_title = data["badge_title"]
        badge.setText(badge_title.encode('utf-8').decode('unicode_escape'))
        font = QFont()
        font.setFamily(data["badge_font_family"])
        badge.setFont(font)
        font.setPointSize(data["badge_font_size"])
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setMargin(data["badge_margin"])

        label = QLabel()
        image_path = 'medal_5.jpg'
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

    def check_badge(page_type):
        if page_type == 'multiplechoice' or page_type == 'draganddrop':
            return "Felicidades! Conseguiste la medalla \"Un pequeño, gran paso\" (completa tu primera pregunta)"
        