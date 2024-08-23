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
        self.drop_area.setStyleSheet(f"color: {self.styles.get('cmd_text_color', '#000000')}; background-color: {self.styles.get('cmd_background_color', '#FFFFFF')}; font-size: {self.styles.get('font_size_normal', 12)}px")
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
        print(f"Texto arrastrado: {new_dropped_text}")  # Agregar print para verificar el texto arrastrado
        if len(self.dropped_texts) < len(self.base_text_parts) - 1:
            self.dropped_texts.append(new_dropped_text)
        else:
            if self.dropped_text is not None:
                current_text = self.drop_area.text().replace(self.dropped_text, "<Espacio para respuesta>", 1)
                self.drop_area.setText(current_text)
            self.dropped_text = new_dropped_text
            self.dropped_texts = [self.dropped_text]  # Reemplaza el texto anterior

        self.drop_area.setText(self.get_current_text())
        print(f"Estado actual de dropped_texts: {self.dropped_texts}")  # Agregar print para verificar dropped_texts
        event.acceptProposedAction()
