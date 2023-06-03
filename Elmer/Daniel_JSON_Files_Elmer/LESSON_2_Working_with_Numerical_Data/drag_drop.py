from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag,  QPixmap, QPainter
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout


def create_pixmap_from_label(label):
    pixmap = QPixmap(label.size())
    label.render(pixmap)
    return pixmap


class DraggableLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAcceptDrops(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mime_data = QMimeData()
            mime_data.setText(self.text())

            drag = QDrag(self)
            drag.setMimeData(mime_data)

            pixmap = create_pixmap_from_label(self)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            drag.exec(Qt.DropAction.MoveAction)


class DropLabel(QWidget):
    def __init__(self, text, styles, question_type=None, multiple=False):
        super().__init__()
        self.question_type = question_type
        self.setAcceptDrops(True)
        self.dropped_texts = []
        self.dropped_text = None
        self.styles = styles
        self.multiple = multiple

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if multiple:
            self.base_text_parts = text.split("___")
            self.drop_area3 = QLabel(self.get_current_text())
            self.drop_area3.setStyleSheet(f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
            self.layout.addWidget(self.drop_area3)
        else:
            self.base_text = text
            self.drop_area = QLabel(text)
            self.drop_area.setStyleSheet(f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
            self.layout.addWidget(self.drop_area)

    def get_current_text(self):
        text = ""
        for i in range(len(self.base_text_parts)):
            text += self.base_text_parts[i]
            if i < len(self.dropped_texts):
                text += self.dropped_texts[i]
        return text

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        new_dropped_text = event.mimeData().text()
        if self.multiple:
            if len(self.dropped_texts) < len(self.base_text_parts) - 1:
                self.dropped_texts.append(new_dropped_text)
                self.drop_area3.setText(self.get_current_text())
        else:
            if self.dropped_text is not None:
                current_text = self.drop_area.text().replace(self.dropped_text, "____" if "____" in self.base_text else "_", 1)
                self.drop_area.setText(current_text)
                self.base_text = current_text

            self.dropped_text = new_dropped_text

            if "____" in self.base_text:
                self.drop_area.setText(self.base_text.replace("____", new_dropped_text, 1))
                self.base_text = self.drop_area.text()
            elif "_" in self.base_text:
                self.drop_area.setText(self.base_text.replace("_", new_dropped_text, 1))
                self.base_text = self.drop_area.text()
        event.acceptProposedAction()


