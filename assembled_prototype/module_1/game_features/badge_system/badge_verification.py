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
    def __init__(self, badge_types:list[str]) -> None:
        self.badge_types = badge_types
        self.current_badge_index = 0
        self.load_badges_data()
        super(BadgeVerification, self).__init__()
        
        validation, badge_type = self.validateBadgeTypes()
        if validation:
            self.initUI(badge_type)
        else:
            self.hide()

    def load_badges_data(self):
        with open(main_directory_path + "\\badge_info.json", "r", encoding='utf-8') as finish_info:
            self.data = json.load(finish_info)

    def validateBadgeTypes(self) -> bool:
        for badge_type in self.badge_types:
            if badge_type not in self.data:
                return False
            return True, badge_type

    def onAcceptClicked(self):
        self.current_badge_index += 1
        if self.current_badge_index < len(self.badge_types):
            self.initUI(self.badge_types[self.current_badge_index])
        else:
            self.close()

    def initUI(self, badge_type): 
        badge = self.data.get(badge_type, None)
        
        if badge:
            badge = self.data[badge_type]
            #Window properties
            self.setWindowTitle(badge["badge_window_title"])
            #Layouts
            layoutV = QVBoxLayout()
        
            #Label properties
            badge_label = QLabel(self)
            badge_label.setText(badge["badge_text"] + "\n" + badge["badge_title"])
            font = QFont()
            font.setFamily(badge["badge_font_family"])
            badge_label.setFont(font)
            font.setPointSize(badge["badge_font_size"])
            badge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge_label.setMargin(badge["badge_margin"])
            
            # close button
            accept_button = QPushButton("Aceptar")
            accept_button.setFixedSize(250, 30)
            accept_button.clicked.connect(self.onAcceptClicked)

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
            layoutV.addWidget(badge_label)

            layoutV.addStretch()
            layoutV.addWidget(frame, alignment=Qt.AlignmentFlag.AlignHCenter)
            layoutV.addStretch()
            layoutV.addWidget(accept_button, alignment=Qt.AlignmentFlag.AlignHCenter)
            #Widget/Container initialization
            widget = QWidget()
            widget.setLayout(layoutV)
            self.setCentralWidget(widget)
 

    def count_correct_answers(self, filename):

        with open(filename) as file:
            reader = csv.reader(file)

            correctas_sucesivas = 0
            max_correctas_sucesivas = 0

            for i, row in enumerate(reader):
                if i % 2 != 0: 
                    if len(row) > 1:
                        evento = row[0]
                        if evento.startswith("Parte"):
                            correctas_sucesivas += 1
                            if correctas_sucesivas > max_correctas_sucesivas:
                                max_correctas_sucesivas = correctas_sucesivas
                        else:
                            correctas_sucesivas = 0
       
        return max_correctas_sucesivas
    
        self.current_badge_index += 1
        if self.current_badge_index < len(self.badge_types):
           self.initUI()
        else:
            self.close()

def main():
    app = QApplication(sys.argv)

    main_page = BadgeVerification()
    main_page.count_correct_answers("C:\\Users\\Admin\\VSCode\\AI_Gamification_Python\\assembled_prototype\\module_1\\LESSON_1_Codification\\Entradas_Salidas_Clics_Lesson_1.csv")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
