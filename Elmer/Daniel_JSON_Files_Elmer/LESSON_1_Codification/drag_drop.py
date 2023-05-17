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
    def __init__(self, text, styles, question_type=None):
        super().__init__()
        self.question_type = question_type
        self.setAcceptDrops(True)
        self.dropped_text = None

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.base_text = text
        self.drop_area = QLabel(text)
        self.drop_area.setStyleSheet(f"border: {styles['syntax_border_width']}px solid {styles['syntax_border_color']}; background-color: {styles['syntax_background_color']}; font-size: {styles['font_size_normal']}px")
        self.layout.addWidget(self.drop_area)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        new_dropped_text = event.mimeData().text()
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


