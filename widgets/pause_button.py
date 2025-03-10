from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, Signal

class PauseButton(QPushButton):
    clicked_paused = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(36, 36)  # Set base size to 36x36
        self.setStyleSheet(self.default_stylesheet())
        self.pressed_offset_x = 0  # Offset for pressed effect (rightwards)
        self.pressed_offset_y = 0  # Offset for pressed effect (downwards)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hide()
        self.clicked.connect(self.emit_signal)

    def default_stylesheet(self):
        return """
        QPushButton {
            border-radius: 18px;  /* Make it circular */
            background-color: white;
        }
        QPushButton:hover {
            background-color: rgb(230, 230, 230);
        }
        """
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw pause bars with offset if pressed
        painter.setBrush(QColor("black"))
        painter.setPen(Qt.NoPen)

        # Adjusted pause bars for 36x36 size
        painter.drawRect(11 + self.pressed_offset_x, 7 + self.pressed_offset_y, 5, 22)  # Left bar
        painter.drawRect(20 + self.pressed_offset_x, 7 + self.pressed_offset_y, 5, 22)

    def mousePressEvent(self, event):
        self.pressed_offset_x = 1  # Shift bars slightly to the right
        self.pressed_offset_y = 1  # Shift bars slightly downwards
        self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.pressed_offset_x = 0  # Reset position after release
        self.pressed_offset_y = 0
        self.update()
        super().mouseReleaseEvent(event)
    
    def emit_signal(self):
        self.clicked_paused.emit()