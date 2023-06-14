#game_features/progress_bar.py
import csv
import json
import sys
from PyQt6.QtWidgets import QApplication, QProgressBar, QPushButton, QWidget
from PyQt6.QtCore import QBasicTimer, Qt
from PyQt6.QtWidgets import QVBoxLayout


class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.progress_bar = QProgressBar(self)
        self.timer = QBasicTimer()
        self.progress = 0
        self.step = 1

        self.progress_bar.setFixedSize(506, 15)
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

        
    def count_element_progress(self, nombre_archivo, lesson_number=0):
        punto_extension = "."
        punto_directorio_actual = nombre_archivo.index(punto_extension)  # Obtiene el índice del carácter especificado
        indice = nombre_archivo.find(punto_extension, punto_directorio_actual + 1)
        extension = nombre_archivo[indice+1:]
       
        if extension == 'json':
             with open(nombre_archivo) as archivo:
                data = json.load(archivo)
                # Specify the lesson_number for filtering

                # Find the lesson with the specified lesson_number
                lesson = next((l for l in data["lessons"] if l["lesson_number"] == lesson_number), None)

                if lesson:
                    # Get the number of objects in "pages" for the specified lesson_number
                    return len(lesson["pages"])
                else:
                    return
                
        elif extension == 'csv':
            with open(nombre_archivo) as archivo:
                lector = csv.reader(archivo)
                contador = sum(1 for _ in lector)
                return contador - 1 
                

    def increment_progress(self, number_of_pages):
        max_page = number_of_pages
        if self.step >= max_page:
            self.progress_bar.setValue(100)
            return
        
        self.progress += round(100 / max_page)
        self.progress_bar.setValue(self.progress)
        self.step += 1

    def resetProgress(self):
        self.progress = 0
        self.step = 0
        self.progress_bar.setValue(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec())
