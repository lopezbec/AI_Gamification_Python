import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QRadioButton, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class SoloLearnXP(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_xp = 0
        self.current_quiz = 0
        self.questions = ['Python is an interpreted, high-level and general-purpose programming language.',
                          'Guido van Rossum is the creator of Python.']
        self.options = [['Python is a snake.',
                         'Python is an interpreted, high-level and general-purpose programming language.',
                         'Python is a type of food.'],
                        ['Guido van Rossum is a film actor.',
                         'Guido van Rossum is a football player.',
                         'Guido van Rossum is the creator of Python.']]
        self.correct_options = [1, 2]

        # Llama al método para inicializar la interfaz de usuario.
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('XP')

        self.xp_label = QLabel('XP', self)
        self.xp_label.move(150, 20)

        self.current_xp_label = QLabel('Current XP: 0', self)
        self.current_xp_label.move(150, 60)

        self.lesson_label = QLabel(self.questions[self.current_quiz], self)
        self.lesson_label.setWordWrap(True)
        self.lesson_label.adjustSize()

        self.option1 = QRadioButton(self.options[self.current_quiz][0], self)
        self.option2 = QRadioButton(self.options[self.current_quiz][1], self)
        self.option3 = QRadioButton(self.options[self.current_quiz][2], self)
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.checkAnswer)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.xp_label)
        self.layout.addWidget(self.current_xp_label)
        self.layout.addWidget(self.lesson_label)
        self.layout.addWidget(self.option1)
        self.layout.addWidget(self.option2)
        self.layout.addWidget(self.option3)
        self.layout.addWidget(self.submit_button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.show()

    def checkAnswer(self):
        if ((self.option1.isChecked() and self.correct_options[self.current_quiz] == 0) or
            (self.option2.isChecked() and self.correct_options[self.current_quiz] == 1) or
            (self.option3.isChecked() and self.correct_options[self.current_quiz] == 2)):
            self.current_xp += 1
            self.current_xp_label.setText('Current XP: {}'.format(self.current_xp))
            QMessageBox.information(self, 'Correct!', 'Your answer is correct. You earned 1 XP.')
            self.nextQuiz()
        else:
            QMessageBox.warning(self, 'Incorrect!', 'Your answer is incorrect. Try again.')

    def nextQuiz(self):
        if self.current_quiz + 1 < len(self.questions):
            self.current_quiz += 1
            self.lesson_label.setText(self.questions[self.current_quiz])
            self.option1.setText(self.options[self.current_quiz][0])
            self.option2.setText(self.options[self.current_quiz][1])
            self.option3.setText(self.options[self.current_quiz][2])
            self.option1.setChecked(False)
            self.option2.setChecked(False)
            self.option3.setChecked(False)
        else:
            QMessageBox.information(self, 'Congratulations!', 'You have completed all quizzes.')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    solo_learn_xp = SoloLearnXP()
    sys.exit(app.exec())
