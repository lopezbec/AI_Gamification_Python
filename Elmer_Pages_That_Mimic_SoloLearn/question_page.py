import json
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, \
    QApplication, QMessageBox


class QuestionWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        # Create a layout for the widget
        layout = QVBoxLayout()
        layout.setSpacing(10)
        self.setStyleSheet('background-color: #f0f0f0;')

        # Add the title to the layout
        title_label = QLabel(data['title'])
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #00BFFF;')
        layout.addWidget(title_label)

        # Add the question and answer options to the layout
        question_label = QLabel(data['blocks'][0]['text'])
        question_label.setStyleSheet('font-size: 18px; color: #555555; background-color: #d0d0d0; padding: 5px;')
        layout.addWidget(question_label)

        answer_options = data['blocks'][1]['text'].split('\n')
        answer_group = QButtonGroup()

        for i, option in enumerate(answer_options):
            option_label = QRadioButton(option)
            option_label.setStyleSheet('font-size: 18px; color: #555555; background-color: #f0f0f0; padding: 5px;')
            answer_group.addButton(option_label, i)
            layout.addWidget(option_label)

        # Add the submit button to the layout
        submit_button = QPushButton('Enviar')
        submit_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
        submit_button.setCursor(Qt.PointingHandCursor)
        submit_button.setFixedSize(submit_button.sizeHint())  # add this line to set the size of the button
        submit_button.clicked.connect(self.submit)
        layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        # Set the layout for the widget
        self.setLayout(layout)

    def submit(self):
        # Get the selected answer
        answer = self.sender().parent().findChild(QButtonGroup).checkedButton().text()

        # Show a message box with the answer
        msg_box = QMessageBox()
        msg_box.setText(f'La respuesta seleccionada es: {answer}')
        msg_box.exec()


# Create the QApplication instance
app = QApplication(sys.argv)

# Load the data from the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Create a list of QuestionWidget instances based on the data
question_widgets = [QuestionWidget(page_data) for page_data in data['question']]

# Create the main window and set its properties
window = QWidget()
window.setWindowTitle('My SoloLearn Course')
window.setGeometry(100, 100, 800, 600)

# Create a vertical layout for the window and add the widgets to it
window_layout = QVBoxLayout()

# Create the navigation bar
nav_layout = QHBoxLayout()
nav_layout.setSpacing(20)

# Add the 'Pedagogical' page button
pedagogical_button = QPushButton('Pedagogical')
pedagogical_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #555555; padding: 10px 20px; border-radius: 5px;')
nav_layout.addWidget(pedagogical_button)

# Add the 'Questions' page button
questions_button = QPushButton('Questions')
questions_button.setStyleSheet('font-size: 18px; color: #FFFFFF; background-color: #00BFFF; padding: 10px 20px; border-radius: 5px;')
nav_layout.addWidget(questions_button)

# Add the navigation bar and the widgets to the window layout
window_layout.addLayout(nav_layout)

for widget in question_widgets:
    window_layout.addWidget(widget)
window.setLayout(window_layout)

# Apply the hover effect to the submit button
submit_button_style = '''
    QPushButton:hover {
        background-color: #0099FF;
    }
'''
submit_button = window.findChild
# Show the window and start the application event loop
window.show()
sys.exit(app.exec_())