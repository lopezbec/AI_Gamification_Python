import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QMainWindow, QVBoxLayout, QWidget


class BadgeVerification(QDialog):
    def __init__(self, badge_id: str) -> None:
        super(BadgeVerification, self).__init__()
        self.badge_id = badge_id  # Asignar badge_id como propiedad de la clase

        try:
            # Cargar los criterios de las insignias desde el archivo JSON
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_criteria.json"), "r", encoding='UTF-8') as file:
                self.badge_criteria = json.load(file)

            # Cargar la información de la insignia específica usando el badge_id
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_info.json"), "r", encoding='UTF-8') as finish_info:
                data = json.load(finish_info)

            # Seleccionar la información de la insignia específica basada en badge_id
            badge_info = next((badge for badge in data if badge["badge_id"] == self.badge_id), None)

            if badge_info:
                # Window properties
                self.setWindowTitle(badge_info["badge_text"])
                # Layouts
                layoutV = QVBoxLayout()
                # Label properties
                badge = QLabel(self)
                badge_title = badge_info["badge_title"]
                badge_description = badge_info["badge_description"]
                badge.setText(badge_title + '\n' + badge_description)
                font = QFont()
                font.setFamily(badge_info["badge_font_family"])
                badge.setFont(font)
                font.setPointSize(badge_info["badge_font_size"])
                badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
                badge.setMargin(badge_info["badge_margin"])

                label = QLabel()
                image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medal_icon.png')
                pixmap = QPixmap(image_path)

                if not pixmap.isNull():
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    pixmap = pixmap.scaledToWidth(200)
                    label.setPixmap(pixmap)
                    label.setFixedSize(pixmap.width(), pixmap.height())

                    # Vertical layout
                    layoutV.setSpacing(10)
                    layoutV.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
                    layoutV.addWidget(badge)
                    layoutV.addWidget(label)
                    self.setLayout(layoutV)
                else:
                    print("imagen no encontrada en el path especificado")
            else:
                print(f"No se encontró información para la insignia con ID '{self.badge_id}'")
        except Exception as e:
            print(f"Fallo en la creación de la clase: {e}")
            print(f"Error en linea {sys.exc_info()[2].tb_lineno}")

