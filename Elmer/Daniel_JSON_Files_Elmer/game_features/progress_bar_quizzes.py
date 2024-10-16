# game_features/progress_bar_quizzes.py
import json
import os
from PyQt6.QtWidgets import QWidget, QProgressBar, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class ProgressBarQuizzes(QWidget):
    def __init__(self, current_quiz):
        super().__init__()

        self.label = None
        self.progress = None
        self.progress_bar = None
        self.styles = self.load_json_styles()
        self.quiz_data = self.load_quiz_data()  # Cargar los datos del archivo JSON
        self.current_quiz = current_quiz
        self.current_section = 0

        self.initUI()

    def load_json_styles(self):
        """Cargar estilos desde styles.json."""
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.json')) as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Error loading json styles for ProgressBarQuizzes:", e)
            return {}

    def load_quiz_data(self):
        """Cargar los datos de los quizzes desde el archivo page_order_quizzes.json."""
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_order_quizzes.json')) as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Error loading quiz data from page_order_quizzes.json:", e)
            return {}

    def initUI(self):
        """Inicializar la interfaz de usuario."""
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedSize(506, 15)
        self.progress_bar.setFormat('%p%')
        self.progress_bar.setStyleSheet(self.get_style_sheet())

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
        self.update_progress()

    def setValue(self, value):
        """Actualizar el valor de la sección actual."""
        self.current_section = value
        self.update_progress()

    def get_style_sheet(self):
        """Obtener la hoja de estilo para la barra de progreso."""
        return """
        QProgressBar{
            border: """ + str(self.styles.get("quiz_progress_bar_border_width", self.styles.get("progress_bar_border_width", 1))) + """px solid """ + self.styles.get("quiz_progress_bar_border_color", self.styles.get("progress_bar_border_color", "#000000")) + """;
            border-radius: """ + str(self.styles.get("quiz_progress_bar_border_radius", self.styles.get("progress_bar_border_radius", 5))) + """px;
            text-align: center;
        }

        QProgressBar::chunk {
            background-color: """ + self.styles.get("quiz_progress_bar_color", self.styles.get("progress_bar_color", "#4CAF50")) + """;
            width: """ + str(self.styles.get("quiz_progress_bar_chunk_width", self.styles.get("progress_bar_chunk_width", 5))) + """px;
        }
        """

    def increment_section(self):
        """Incrementar la sección actual y actualizar el progreso."""
        if self.current_section < len(self.quiz_data["quizzes"][self.current_quiz]["sections"]) - 1:
            self.current_section += 1
            self.update_progress()

    def decrement_section(self):
        """Decrementar la sección actual y actualizar el progreso."""
        if self.current_section > 0:
            self.current_section -= 1
            self.update_progress()

    def update_progress(self):
        """Actualizar la barra de progreso basada en la sección actual."""
        total_sections = len(self.quiz_data["quizzes"][self.current_quiz]["sections"])
        self.progress = ((self.current_section + 1) / total_sections) * 100
        self.progress_bar.setValue(int(self.progress))
        self.update_label()

    def update_label(self):
        """Actualizar el texto de la barra de progreso."""
        total_sections = len(self.quiz_data["quizzes"][self.current_quiz]["sections"])
        self.label.setText(f'Quiz: {self.current_quiz + 1}, Sección {self.current_section + 1} de {total_sections}, {self.progress:.2f}% completo')
