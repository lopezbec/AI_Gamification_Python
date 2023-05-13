from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QLabel


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
            drag.exec(Qt.DropAction.MoveAction)


class DropLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.base_text = text
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        dropped_text = event.mimeData().text()
        self.setText(self.base_text.replace("....", dropped_text))
        event.acceptProposedAction()