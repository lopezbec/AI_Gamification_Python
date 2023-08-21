#badge_system/badge_verification.py
import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
main_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from module_1.lesson_1_codification import Main_Lesson_1
app = QApplication([])


class BadgeVerification(QMainWindow):
    def __init__(self) -> None:
        super(BadgeVerification, self).__init__()
        self.initUI()

    def closeEvent(self, event):
        self.hide()
        self.mod_1_lesson_1 = Main_Lesson_1.MainWindow()
        self.mod_1_lesson_1.show()


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
        directorio_hermano = os.path.join(directorio_actual, "..", "assets", "img")

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
