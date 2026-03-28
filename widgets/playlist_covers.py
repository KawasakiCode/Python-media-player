from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QBrush
from PySide6.QtCore import Qt
import sys
import os

class PlaylistCover(QWidget):
    def __init__(self, parent, image_path):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(250, 250)
        self.image_path = image_path

        if image_path == "default":
            self.image_label.setPixmap(self.get_rounded_pixmap(self.resource_path("Assets/default.jpg"), 35))
        else:
            self.image_label.setPixmap(self.get_rounded_pixmap(image_path, 35))
        self.image_label.setScaledContents(True)

        layout.addWidget(self.image_label)
        self.setLayout(layout)
        self.setFixedSize(350, 350)

        # Add widgets to layout
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def get_rounded_pixmap(self, image_path, radius):
        pixmap = QPixmap(image_path).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        path = QPainterPath()
        path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(pixmap))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        painter.end()

        return rounded

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)