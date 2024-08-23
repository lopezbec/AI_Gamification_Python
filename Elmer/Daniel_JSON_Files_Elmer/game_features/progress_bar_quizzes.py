# game_features/progress_bar_quizzes.py
import json
import os
from PyQt6.QtWidgets import QWidget, QProgressBar, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class ProgressBarQuizzes(QWidget):
    def __init__(self, data, current_quiz):
        super().__init__()

        self.label = None
        self.progress = None
        self.progress_bar = None
        self.styles = self.load_json_styles()
        self.quiz_data = data

        self.current_quiz = current_quiz
        self.current_section = 0

        self.initUI()

    def load_json_styles(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.json')) as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Error loading json styles for ProgressBarQuizzes")
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

    def setValue(self, value):
        self.current_section = value
        self.update_progress()

    def get_style_sheet(self):
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
        if self.current_section < len(self.quiz_data["quizzes"][self.current_quiz]["sections"]) - 1:
            self.current_section += 1
            self.update_progress()

    def decrement_section(self):
        if self.current_section > 0:
            self.current_section -= 1
            self.update_progress()

    def update_progress(self):
        total_sections = len(self.quiz_data["quizzes"][self.current_quiz]["sections"])
        self.progress = ((self.current_section + 1) / total_sections) * 100
        self.progress_bar.setValue(int(self.progress))
        self.update_label()

    def update_label(self):
        self.label.setText(f'Quiz: {self.current_quiz + 1}, Sección {self.current_section + 1} de {len(self.quiz_data["quizzes"][self.current_quiz]["sections"])}, {self.progress:.2f}% completo')

