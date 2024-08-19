from PyQt6.QtCore import QEvent

class CompleteLessonEvent(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self):
        super().__init__(self.EVENT_TYPE)
