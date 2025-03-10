from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class TitleArtistLabels(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(450, 80)
        text = "Title"
        text2 = "Artists"
        text3 = "Album"
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Title label
        self.title_label = QLabel(text, self)
        self.title_label.setFixedWidth(450)
        self.title_label.setStyleSheet("""
            font-size: 18px;
            font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
            color: white;
            background-color: black;
            border: none;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Artist label
        self.artist_label = QLabel(text2, self)
        self.artist_label.setFixedHeight(25)
        self.artist_label.setStyleSheet("""
            font-size: 15px;
            font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
            color: #777;
            background-color: black;
            border: none;
        """)
        self.artist_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Album name label
        self.album_name = QLabel(text3, self)
        self.album_name.setFixedHeight(25)
        self.album_name.setStyleSheet("""
            font-size: 15px;
            font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
            color: #777;
            background-color: black;
            border: none;
        """)
        self.album_name.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.title_label)
        layout.addWidget(self.artist_label)
        layout.addWidget(self.album_name)
        self.setLayout(layout)
