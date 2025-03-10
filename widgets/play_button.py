from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPolygon, QColor
from PySide6.QtCore import Qt, QPoint, Signal

class PlayButton(QPushButton):
    clicked_play = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(36, 36)  # Set base size to 36x36
        self.setStyleSheet(self.default_stylesheet())
        self.pressed_offset_x = 0
        self.pressed_offset_y = 0
        self.setCursor(Qt.CursorShape.PointingHandCursor)
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

        # Draw black triangle in the center with offset if pressed
        triangle = QPolygon([
            QPoint(11 + self.pressed_offset_x, 7 + self.pressed_offset_y),
            QPoint(11 + self.pressed_offset_x, 29 + self.pressed_offset_y),
            QPoint(28 + self.pressed_offset_x, 18 + self.pressed_offset_y)
        ])
        painter.setBrush(QColor("black"))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(triangle)
    
    def mousePressEvent(self, event):
        self.pressed_offset_x = 1  # Shift triangle slightly to the right
        self.pressed_offset_y = 1  # Shift triangle slightly downwards
        self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.pressed_offset_x = 0  # Reset position after release
        self.pressed_offset_y = 0
        self.update()
        super().mouseReleaseEvent(event)
    
    def emit_signal(self):
        self.clicked_play.emit()
