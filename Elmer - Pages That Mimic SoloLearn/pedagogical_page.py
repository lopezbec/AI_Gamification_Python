import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel


class PedagogicalWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        # Create a layout for the widget
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Add the title to the layout
        title_label = QLabel(data['title'])
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #00BFFF;')
        layout.addWidget(title_label)

        for block in data['blocks']:
            block_label = QLabel(block['text'])
            block_label.setStyleSheet('font-size: 18px; color: #555555;')
            block_type = block['type']

            # Set the style of the block based on its type
            if block_type == 'info':
                block_label.setStyleSheet('background-color: #ECF8FF; border: 1px solid #B5E2FF; padding: 10px; font-size: 18px; color: #555555;')
            elif block_type == 'syntax':
                block_label.setStyleSheet('background-color: #F9F9F9; border: 1px solid #EDEDED; padding: 10px; font-size: 18px; color: #555555;')
            elif block_type == 'hint':
                block_label.setStyleSheet('background-color: #FFF6F6; border: 1px solid #FFC9C9; padding: 10px; font-size: 18px; color: #555555;')

            layout.addWidget(block_label)

        # Set the layout for the widget
        self.setLayout(layout)

# Create the QApplication instance
app = QApplication(sys.argv)

# Load the data from the JSON file
with open('pedagogical.json', 'r') as file:
    data = json.load(file)

# Create a list of PedagogicalWidget instances based on the data
pedagogical_widgets = [PedagogicalWidget(page_data) for page_data in data['pages']]

# Create the main window and set its properties
window = QWidget()
window.setWindowTitle('My SoloLearn Course')
window.setGeometry(100, 100, 800, 600)

# Create a vertical layout for the window and add the widgets to it
window_layout = QVBoxLayout()
for widget in pedagogical_widgets:
    window_layout.addWidget(widget)
window.setLayout(window_layout)

# Show the window and start the application event loop
window.show()
sys.exit(app.exec_())
