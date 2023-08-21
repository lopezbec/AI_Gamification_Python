import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCheckBox, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget
from name_window import NameWindow


class ConcentWindow(QMainWindow):
    def __init__(self) -> None:
        super(ConcentWindow, self).__init__()

        with open(r'./json/concent_info.json', "r", encoding='UTF-8') as f:
            data = json.load(f)
        
        #title
        title = QLabel(self)
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setBold(data["title_bold"])
        font_title.setPointSize(data["title_font_size"])
        font_title.setFamily(data["title_font_family"])
        title.setFont(font_title)
        title.setWordWrap(data["title_word_wrap"])
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop )
        title.setMargin(data["title_margin"])

        content = QLabel(self)
        
        content.setText(data["content_text"])

        font_content = QFont()
        font_content.setPointSize(data["content_font_size"])
        font_content.setFamily(data["content_font_family"])
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(data["content_word_wrap"])
        content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content.setMargin(data["content_margin"])

        self.accept_terms = QCheckBox(data["accept_checkbox_text"])
        self.accept_terms.stateChanged.connect(self.user_concent)

        self.button = QPushButton(data["button_text"])
        self.button.setMaximumSize(data["button_width"], data["button_height"]);
        self.button.setEnabled(data["button_enabled"])
        self.button.clicked.connect(self.agree_btn_is_clicked)
     
        v_layout = QVBoxLayout()

        v_layout.addWidget(title)
        v_layout.addWidget(content)
        v_layout.addWidget(self.accept_terms)
        v_layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)
        v_layout.setContentsMargins(5,10,5,10)
        
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.showMaximized()

    def user_concent(self):
        if  self.accept_terms.isChecked():
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)
            
    def agree_btn_is_clicked(self):
        if self.button.isEnabled():
            self.name_window = NameWindow()
            self.name_window.show()
            self.hide()
