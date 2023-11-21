# game_features/progress_bar.py
import json
import sys
from PyQt6.QtWidgets import QApplication, QProgressBar, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt


class ProgressBar(QWidget):
    def __init__(self, data, current_lesson):
        super().__init__()

        self.label = None
        self.progress = None
        self.progress_bar = None
        self.styles = self.load_json_styles()
        self.lesson_data = data

        self.current_lesson = current_lesson
        self.current_page = 0

        self.initUI()

    def load_json_styles(self):
        with open('styles.json') as f:
            data = json.load(f)
        return data

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
        self.current_page = value
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
        if self.current_page < len(self.lesson_data["lessons"][self.current_lesson]["pages"]) - 1:
            self.current_page += 1
            self.update_progress()

    def decrement_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_progress()

    def update_progress(self):
        total_pages = len(self.lesson_data["lessons"][self.current_lesson]["pages"])
        self.progress = ((self.current_page + 1) / total_pages) * 100
        self.progress_bar.setValue(int(self.progress))
        self.update_label()

    def update_label(self):
        self.label.setText(f'Lección: {self.current_lesson + 1}, Página {self.current_page + 1} de {len(self.lesson_data["lessons"][self.current_lesson]["pages"])}, {self.progress:.2f}% completo')


if __name__ == '__main__':
    with open('page_order.json') as f:
        lesson_data = json.load(f)

    app = QApplication(sys.argv)
    window = ProgressBar(lesson_data)
    window.show()
    sys.exit(app.exec())
