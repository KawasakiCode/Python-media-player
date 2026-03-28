from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QApplication
from PySide6.QtCore import Qt

class AddRemovePlaylist(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.add_playlist = QPushButton(self)
        self.remove_playlist = QPushButton(self)
        self.setFixedSize(200, 100)
        self.add_playlist.setFixedSize(140, 40)
        self.remove_playlist.setFixedSize(140, 40)
        self.add_playlist.setText("Add Playlist")
        self.remove_playlist.setText("Remove Playlist")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.add_playlist.setStyleSheet("""
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
        """)
        self.remove_playlist.setStyleSheet("""
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
        """)

        self.add_playlist.original_pos = self.add_playlist.pos()
        self.remove_playlist.original_pos = self.add_playlist.pos()

        self.add_playlist.pressed.connect(self.mousePressEventAdd)
        self.add_playlist.released.connect(self.mouseReleaseEventAdd)
        self.remove_playlist.pressed.connect(self.mousePressEventRemove)
        self.remove_playlist.released.connect(self.mouseReleaseEventRemove)

        layout.addWidget(self.add_playlist)
        layout.addSpacing(5)
        layout.addWidget(self.remove_playlist)
        self.setLayout(layout)

    def mousePressEventAdd(self):
        self.add_playlist.move(self.add_playlist.x() + 1, self.add_playlist.y() + 1)

    def mouseReleaseEventAdd(self):
        self.add_playlist.move(self.add_playlist.x() - 1, self.add_playlist.y() - 1)
    
    def mousePressEventRemove(self):
        self.remove_playlist.move(self.remove_playlist.x() + 1, self.remove_playlist.y() + 1)

    def mouseReleaseEventRemove(self):
        self.remove_playlist.move(self.remove_playlist.x() - 1, self.remove_playlist.y() - 1)