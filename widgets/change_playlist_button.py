from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

class Change_playlist(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(120, 40)
        self.setText("Change Playlist?")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton{
                font-size: 12px;
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
        """)

        self.original_pos = self.pos() 

    def mousePressEvent(self, event):
        self.move(self.x() + 1, self.y() + 1)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.move(self.x() - 1, self.y() - 1)
        super().mouseReleaseEvent(event)