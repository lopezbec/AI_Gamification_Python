import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget

class Leaderboard(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Leaderboard')

        # Create labels for the leaderboard entries
        self.player1 = QLabel('Player 1 - 100', self)
        self.player2 = QLabel('Player 2 - 90', self)
        self.player3 = QLabel('Player 3 - 80', self)
        self.player4 = QLabel('Player 4 - 70', self)
        self.player5 = QLabel('Player 5 - 60', self)

        # Create a vertical layout to hold the leaderboard labels
        leaderboard_layout = QVBoxLayout()
        leaderboard_layout.addWidget(self.player1)
        leaderboard_layout.addWidget(self.player2)
        leaderboard_layout.addWidget(self.player3)
        leaderboard_layout.addWidget(self.player4)
        leaderboard_layout.addWidget(self.player5)

        # Create a horizontal layout to hold the leaderboard title and the vertical layout
        main_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(leaderboard_layout)
        main_layout.addStretch()

        # Create a widget to hold the main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    leaderboard = Leaderboard()
    sys.exit(app.exec())