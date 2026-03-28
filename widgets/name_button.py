from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class NameButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(140, 40)
        self.setStyleSheet(self.default_stylesheet())
        self.pressed_offset_x = 0
        self.pressed_offset_y = 0
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make background transparent
        self.setFlat(True)  # Remove button border
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def default_stylesheet(self):
        return  """
            QPushButton{
                font-size: 14px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: #333;
                border-radius: 20px;
                padding: 5px 10px;
                border: none;
            }
            
            QPushButton:hover {
                background-color: #555;
            }
        """
    
    def mousePressEvent(self, event):
        self.move(self.x() + 1, self.y() + 1)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.move(self.x() - 1, self.y() - 1)
        super().mouseReleaseEvent(event)