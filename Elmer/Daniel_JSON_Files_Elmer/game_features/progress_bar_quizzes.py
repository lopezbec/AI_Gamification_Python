import json
import os
from PyQt6.QtWidgets import QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt


class ProgressBar(QProgressBar):
    def __init__(self, lesson_data, current_quiz_index, current_module_index):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)  # Comienza desde 0
        
        self.lesson_data = lesson_data  # Guardamos los datos de la lección
        self.current_quiz_index = current_quiz_index
        self.current_module_index = current_module_index
        
        # Asegurarnos de que quiz_data se inicializa correctamente
        if "quizzes" in lesson_data:
            self.quiz_data = lesson_data["quizzes"]  # Asegúrate de que esta es la clave correcta en los datos
        else:
            self.quiz_data = []  # Si no se encuentra "quizzes", asignar una lista vacía
        
        self.current_section_index = 0
        self.styles = self.load_json_styles()  # Cargar estilos
        self.initUI()

    def set_value(self, value):
        self.setValue(value)

    def load_json_styles(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.json')) as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Error loading json styles for ProgressBar")
            return {}

    def initUI(self):
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

    def get_style_sheet(self):
        return """
        QProgressBar{
            border: """ + str(self.styles["progress_bar_border_width"]) + """px solid """ + self.styles["progress_bar_border_color"] + """;
            border-radius: """ + str(self.styles["progress_bar_border_radius"]) + """px;
            text-align: center;
        }

        QProgressBar::chunk {
            background-color: """ + self.styles["progress_bar_color"] + """;
            width: """ + str(self.styles["progress_bar_chunk_width"]) + """px;
        }
        """

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