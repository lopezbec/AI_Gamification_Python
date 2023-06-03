import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

class BadgeVerification(QMainWindow):
    def __init__(self) -> None:
        super(BadgeVerification, self).__init__()

        
        joined_path = os.path.join(os.path.dirname(os.path.abspath("app.py")), "badge_info.json")
        with open(joined_path, "r", encoding='utf-8') as finish_info:
            data = json.load(finish_info)


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
        directorio_hermano = os.path.join(directorio_actual, "..", "assets", "img")

        #usar el directorio heramno donde esta el archuivo medal
        image_path = os.path.join(directorio_hermano, 'medal_5.jpg')
        pixmap = QPixmap(image_path)

        # Establecer la imagen en la etiqueta
        label.setPixmap(pixmap)

        # Ajustar el tamaño de la etiqueta a la imagen
        label.setFixedSize(pixmap.width(), pixmap.height())
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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

        def initialize_user_data(self):
            datos = {
                "lesson_1_completed": 0,
                "lesson_2_completed": 0,
                "lesson_3_completed": 0,
                "items_respondidos_correctamente": 0,
                "ultima_racha_items_respondidos": 0,
                "lecciones_completadas": 0
            }

            with open("./user_data/user_progress.json", "r", encoding="utf-8") as archivo:
                json.dump(datos, archivo)

def main():
    app = QApplication(sys.argv)

    main_page = BadgeVerification()
    main_page.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()