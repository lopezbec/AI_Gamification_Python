import json
import os
from PyQt6.QtWidgets import QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QPropertyAnimation, Qt


class ProgressBar(QProgressBar):
    def __init__(self, lesson_data, current_quiz_index, current_module_index):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)  # Comienza desde 0
        
        self.lesson_data = lesson_data  # Guardamos los datos de la lección
        self.current_quiz_index = current_quiz_index
        self.current_module_index = current_module_index
        self.current_section_index = 0
        
        # Establecer el progreso inicial en 0 para evitar errores
        self.progress = 0

        # Asegurarnos de que quiz_data se inicializa correctamente
        if "quizzes" in lesson_data:
            self.quiz_data = lesson_data["quizzes"]  
        else:
            self.quiz_data = []  # Si no se encuentra "quizzes", asignar una lista vacía

        self.styles = self.load_json_styles() 
        self.apply_custom_style()


    def set_value(self, value):
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(500)  # Duración de la animación en milisegundos
        self.animation.setStartValue(self.value())
        self.animation.setEndValue(value)
        self.animation.start()

    def load_json_styles(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.json')) as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Error loading json styles for ProgressBar")
            return {}


    def apply_custom_style(self):
        self.setStyleSheet("""
        QProgressBar {
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            background-color: #E0E0E0;
            text-align: center;
            color: #333333;
            font-weight: bold;
            font-size: 14px;
            height: 25px;
            padding: 1px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

        QProgressBar::chunk {
            border-radius: 8px;
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #FF3E3E, stop:1 #32CD32
            );
            animation: shine 3s linear infinite;
        }

        @keyframes shine {
            0% {
                background-position: -200px 0;
            }
            100% {
                background-position: 200px 0;
            }
        }

        QProgressBar[text="100%"] {
            color: white;
            background-color: #32CD32;
        }

        QProgressBar {
            color: #333333;
            font-weight: bold;
            font-size: 14px;
            animation: textZoom 1s ease-in-out infinite alternate;
        }

        @keyframes textZoom {
            0% { font-size: 14px; color: #333333; }
            100% { font-size: 16px; color: #228B22; }
        }
        """)


    def increment_page(self):
        if self.current_section_index < len(self.quiz_data[self.current_quiz_index]["sections"]) - 1:
            self.current_section_index += 1
            self.update_progress()

    def decrement_page(self):
        if self.current_section_index > 0:
            self.current_section_index -= 1
            self.update_progress()

    def update_progress(self):
        if not self.quiz_data:  # Asegurarse de que hay datos
            return
        total_sections = len(self.quiz_data[self.current_quiz_index]["sections"])
        self.progress = ((self.current_section_index + 1) / total_sections) * 100
        self.progress_bar.setValue(int(self.progress))
        self.update_label()

    def update_label(self):
        self.label.setText(f'Quiz: {self.current_quiz_index + 1}, Sección {self.current_section_index + 1} de {len(self.quiz_data[self.current_quiz_index]["sections"])}, {self.progress:.2f}% completo')