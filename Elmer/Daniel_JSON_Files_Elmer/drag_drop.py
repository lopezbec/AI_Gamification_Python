from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap
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

        self.base_text_parts = text.split("___")
        self.drop_area = QLabel(self.get_current_text())
        self.drop_area.setStyleSheet(f"color: {self.styles['cmd_text_color']}; background-color: {self.styles['cmd_background_color']}; font-size: {self.styles['font_size_normal']}px")
        self.layout.addWidget(self.drop_area)

    def get_current_text(self):
        text = ""
        for i in range(len(self.base_text_parts)):
            text += self.base_text_parts[i]
            if i < len(self.dropped_texts):
                text += self.dropped_texts[i]
            elif i < len(self.base_text_parts) - 1:
                text += "<Espacio para respuesta>"
        return text

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        new_dropped_text = event.mimeData().text()
        if len(self.dropped_texts) < len(self.base_text_parts) - 1:
            self.dropped_texts.append(new_dropped_text)
            self.drop_area.setText(self.get_current_text())
        else:
            # Manejo para cuando solo se permite una respuesta
            if self.dropped_text is not None:
                current_text = self.drop_area.text().replace(self.dropped_text, "<Espacio para respuesta>", 1)
                self.drop_area.setText(current_text)

            self.dropped_text = new_dropped_text
            self.drop_area.setText(self.get_current_text())

        event.acceptProposedAction()
