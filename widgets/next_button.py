from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPolygon, QColor
from PySide6.QtCore import Qt, QPoint

class NextButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(30, 30)  # Set base size to 30x30
        self.setStyleSheet(self.default_stylesheet())
        self.pressed_offset_x = 0
        self.pressed_offset_y = 0
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make background transparent
        self.setFlat(True)  # Remove button border
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def default_stylesheet(self):
        return """
        QPushButton {
            border-radius: 15px;  /* Keep circular shape */
            background-color: black;
        }
        """
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw white forward icon with offset if pressed
        painter.setBrush(QColor("white"))
        painter.setPen(Qt.NoPen)

        # Adjusted forward triangle for 30x30 size (mirrored rewind)
        triangle = QPolygon([
            QPoint(21 - self.pressed_offset_x, 15 + self.pressed_offset_y),
            QPoint(8 - self.pressed_offset_x, 6 + self.pressed_offset_y),
            QPoint(8 - self.pressed_offset_x, 24 + self.pressed_offset_y)
        ])
        painter.drawPolygon(triangle)

        # Adjusted right bar (mirrored from left)
        painter.drawRect(21 - self.pressed_offset_x, 6 + self.pressed_offset_y, 3, 18)
    
    def mousePressEvent(self, event):
        self.pressed_offset_x = 1  # Shift icon slightly to the right
        self.pressed_offset_y = 1  # Shift icon slightly downwards
        self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.pressed_offset_x = 0  # Reset position after release
        self.pressed_offset_y = 0
        self.update()
        super().mouseReleaseEvent(event)

