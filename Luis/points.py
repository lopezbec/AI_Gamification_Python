import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class SoloLearnXP(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('XP')

        # Create a label for the XP system
        self.xp_label = QLabel('XP', self)
        self.xp_label.move(150, 20)

        # Create a label for the current XP
        self.current_xp_label = QLabel('Current XP: 0', self)
        self.current_xp_label.move(150, 60)

        # Create a button to earn XP
        self.earn_xp_button = QPushButton('Earn XP', self)
        self.earn_xp_button.move(150, 100)
        self.earn_xp_button.clicked.connect(self.earnXP)

        # Create a vertical layout to hold the labels and button
        xp_layout = QVBoxLayout()
        xp_layout.addWidget(self.xp_label)
        xp_layout.addWidget(self.current_xp_label)
        xp_layout.addWidget(self.earn_xp_button)

        # Create a widget to hold the XP layout
        widget = QWidget()
        widget.setLayout(xp_layout)
        self.setCentralWidget(widget)

        self.show()

    def earnXP(self):
        # Increment the current XP and update the label
        current_xp = int(self.current_xp_label.text().split(': ')[1])
        current_xp += 10
        self.current_xp_label.setText('Current XP: {}'.format(current_xp))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    solo_learn_xp = SoloLearnXP()
    sys.exit(app.exec())