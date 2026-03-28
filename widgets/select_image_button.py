from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

class SelectImageButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(255, 250)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgba(255, 255, 255, 0);
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                font-size: 18px;
            }
        """)
        self.setText("Change Image")
        self.setVisible(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)