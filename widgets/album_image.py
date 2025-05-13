from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
import os
import sys

class AlbumImage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)

        pixmap = QPixmap(self.resource_path("Assets/default.jpg"))

        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        layout.addWidget(self.image_label)
        self.setLayout(layout)
        self.setFixedSize(350, 350)
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
