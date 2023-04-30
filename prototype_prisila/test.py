import json
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget


class Test(QMainWindow):
    def __init__(self) -> None:
        super(Test, self).__init__()

        welcome_data = open(r"./json/welcome_info.json", "r")
        data = json.loads(welcome_data.read())
        #title
        title = QLabel(self)
        title.setText(data["title_text"])
        title.adjustSize()
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(data["title_font_size"])
        font_title.setFamily(data["title_font_family"])
        title.setFont(font_title)
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        title.setMargin(data["title_margin"])

        content = QLabel(self)
        
        content.setText(data["content_text"])

        font_content = QFont()
        font_content.setPointSize(data["content_font_size"])
        font_content.setFamily("Lato")
        content.setFont(font_content)
        content.adjustSize()
        content.setWordWrap(True)
        content.setAlignment(data["title_alignment"])
        content.setMargin(10)



        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        v_layout.addWidget(title)

        h_layout.addWidget(content)
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(-1,-1,-1,-1)
        v_layout.addLayout(h_layout)
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(-1,-1,-1,-1)
        
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

  
def main():
    app = QApplication(sys.argv)
    window = Test()
    window.showMaximized()
    window.show()

    try:
        app.exec()
    except KeyboardInterrupt:
        print("shuting down...")

if __name__ == "__main__":
    main()

