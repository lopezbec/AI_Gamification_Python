import csv
import json
import random
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QMainWindow, QPushButton, QRadioButton, QVBoxLayout, \
    QWidget
from finish_window import FinishWindow
import os


class QuestionWindow(QMainWindow):
    def __init__(self) -> None:
        self.read_csv()
        global responses
        self.counter = 0
        responses = []
        self.username = "placeholder"
        self.radio_buttons = ["radio_1", "radio_2", "radio_3", "radio_4",
                              "radio_5", "radio_6", "radio_7"]
        super(QuestionWindow, self).__init__()

        # Obtiene la ruta del directorio donde se encuentra el script actual
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al archivo JSON usando os.path.join
        json_path = os.path.join(current_script_path, 'json', 'question_info.json')
        with open(json_path, encoding='UTF-8') as question_info:
            data = json.load(question_info)

        # window title
        self.setWindowTitle(data["window_title"])
        # title
        self.title = QLabel(self)
        question_number = self.get_number_question()
        self.title.setText(data["title_text"] + str(question_number))
        self.title.adjustSize()
        font_title = QFont()
        # font_title.setBold(data["title_bold"])
        font_title.setPointSize(data["title_font_size"])
        # font_title.setFamily(data["title_font_family"])
        self.title.setFont(font_title)
        self.title.setWordWrap(data["title_word_wrap"])
        self.title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.title.setMargin(data["title_margin"])

        self.content = QLabel(self)
        question = self.pick_question()
        self.content.setText(question)

        font_content = QFont()
        font_content.setPointSize(data["content_font_size"])
        # font_content.setFamily(data["content_font_family"])
        self.content.setFont(font_content)
        self.content.adjustSize()
        self.content.setWordWrap(data["content_word_wrap"])
        self.content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.content.setMargin(data["content_margin"])

        # For the variables name in radio button I rather to choose the point in the scale
        # than the name itself for shortest but logical names here the scale

        # 1 - Strongly Disagree
        # 2 - Disagree
        # 3 - Somewhat Disagree
        # 4 - Neutral
        # 5 - Somewhat Neutral
        # 6 - Agree
        # 7 - Strongly Agree
        # soo radio_1 is the radio button for strongly disagre
        # because is their rate in the scale

        self.radio_1 = QRadioButton()
        self.radio_1.setText(data["radio_text"]["radio_1"])
        self.radio_1.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.radio_1.toggled.connect(lambda: self.pick_value(self.radio_1))

        self.radio_2 = QRadioButton()
        self.radio_2.setText(data["radio_text"]["radio_2"])
        self.radio_2.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.radio_2.toggled.connect(lambda: self.pick_value(self.radio_2))

        self.radio_3 = QRadioButton()
        self.radio_3.setText(data["radio_text"]["radio_3"])
        self.radio_3.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.radio_3.toggled.connect(lambda: self.pick_value(self.radio_3))

        self.radio_4 = QRadioButton()
        self.radio_4.setText(data["radio_text"]["radio_4"])
        self.radio_4.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.radio_4.toggled.connect(lambda: self.pick_value(self.radio_4))

        self.radio_5 = QRadioButton()
        self.radio_5.setText(data["radio_text"]["radio_5"])
        self.radio_5.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.radio_5.toggled.connect(lambda: self.pick_value(self.radio_5))

        self.radio_6 = QRadioButton()
        self.radio_6.setText(data["radio_text"]["radio_6"])
        self.radio_6.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.radio_6.toggled.connect(lambda: self.pick_value(self.radio_6))

        self.radio_7 = QRadioButton()
        self.radio_7.setText(data["radio_text"]["radio_7"])
        self.radio_7.setStyleSheet(f"font-size:{data['content_font_size']}px")
        self.radio_7.toggled.connect(lambda: self.pick_value(self.radio_7))

        self.next_button = QPushButton(self)
        self.next_button.setText(data["next_button_text"])
        # self.next_button.setFixedSize(data["next_button_width"], data["next_button_height"])
        self.next_button.setStyleSheet(
            f"background-color: {data['Default_ConsentUser_button_color']};color: white;font-size:{data['font_size_buttons']}px")
        self.next_button.setEnabled(data["next_button_enabled"])
        self.next_button.clicked.connect(self.next_question)

        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        grid_layout = QGridLayout()

        grid_layout.addWidget(self.radio_1)
        grid_layout.addWidget(self.radio_2)
        grid_layout.addWidget(self.radio_3)
        grid_layout.addWidget(self.radio_4)
        grid_layout.addWidget(self.radio_5)
        grid_layout.addWidget(self.radio_6)
        grid_layout.addWidget(self.radio_7)

        v_layout.addWidget(self.title)

        h_layout.addWidget(self.content)
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(-1, -1, -1, -1)
        v_layout.addLayout(h_layout)
        v_layout.addLayout(grid_layout)
        v_layout.addWidget(self.next_button)
        v_layout.setSpacing(10)
        v_layout.setContentsMargins(-1, -1, -1, -1)

        widget = QWidget()
        widget.setLayout(v_layout)
        self.showMaximized()
        self.setCentralWidget(widget)

    def read_csv(self):
        global question_index, question_value, question_dict
        question_index = []  # store the index
        question_value = []  # store the questions itself

        current_script_path = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al archivo JSON usando os.path.join
        json_path = os.path.join(current_script_path, 'Survey.csv')
        with open(json_path, encoding='UTF-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
            line = 0
            for row in csv_reader:
                if line == 0:
                    line += 1
                    continue
                question_index.append(row[0])
                question_value.append(row[1])
                line += 1

            # create dictionary with  index list (P1, P2, etc) and the question list
            question_dict = dict(zip(question_index, question_value))

    def pick_question(self):
        global random_index  # index from the survey P1, P2, P3 and so on.
        random_index = random.choice(question_index)
        random_question = question_dict[random_index]
        return random_question

    def get_number_question(self):
        self.counter += 1
        return self.counter

    # assing value to the radio button
    def pick_value(self, radio):
        global score
        options = ["Totalmente en desacuerdo", "En desacuerdo", "Ligeramente en desacuerdo",
                   "Neutral", "Ligeramente de acuerdo", "De acuerdo", "Totalmente de acuerdo"]
        value = [1, 2, 3, 4, 5, 6, 7]
        values_dict = dict(zip(options, value))

        if radio.isChecked() and radio.text() in options:
            score = values_dict.get(radio.text())
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(
                f"background-color: #00BFFF;color: white;font-size:18px")
        else:
            self.next_button.setEnabled(False)
            self.next_button.setStyleSheet(
                f"background-color: #9B9B9B;color: white;font-size:18px")

    def next_question(self):
        index_in_list = question_index.index(random_index)
        question_index.pop(index_in_list)
        self.next_button.setEnabled(False)

        for radio in self.radio_buttons:
            getattr(self, radio).setAutoExclusive(False)
            getattr(self, radio).setChecked(False)

        if len(question_index) < 1:
            self.save_question()
            self.write_csv()
            self.finish = FinishWindow()
            self.finish.show()
            self.hide()
        else:
            self.save_question()
            self.title.setText("Pregunta #" + str(self.get_number_question()))
            self.content.setText(self.pick_question())

        if len(question_index) == 1:
            self.next_button.setText("Finalizar")
            # self.next_button.clicked.connect( self.show_pages)
            # Sself.hide()

        if len(question_index) == 0:
            self.next_button.setText("Finalizar")

        for radio in self.radio_buttons:
            getattr(self, radio).setAutoExclusive(True)

    def save_question(self):
        question = random_index
        value = score
        responses.append(dict({"question_index": question, "score": value}))

    def write_csv(self):
        try:
            csv_columns = ['question_index', 'score']
            final_responses = responses  # Asegúrate de que 'responses' esté definido correctamente

            # Crear la carpeta si no existe
            folder_path = 'Usuarios_respuestas_entrevista'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Ruta del archivo CSV dentro de la carpeta
            csv_file_path = os.path.join(folder_path, 'user_{}.csv'.format(self.username))
        except Exception as e:
            print(f"Error carpeta: {e}")

        try:
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns, delimiter=',', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                writer.writeheader()
                for data in final_responses:
                    writer.writerow(data)
        except IOError:
            print("I/O error")