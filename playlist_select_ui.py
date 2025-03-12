from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QBrush
from widgets.playlist_covers import PlaylistCover
from widgets.name_button import NameButton
from widgets.select_image_button import SelectImageButton
from widgets.add_remove_playlist import AddRemovePlaylist
from main_ui import MainUi
from add_remove_ui import AddRemoveUi
import json
import os

class PlaylistSelectUi(QMainWindow):
    def __init__(self, playlist_dict):
        super().__init__()
        self.playlist_dict = playlist_dict
        self.setWindowTitle("Spotify alla better")
        self.setStyleSheet("background: black;")
        self.playlist_covers = []
        self.name_buttons = []
        self.select_image_buttons = []
        self.data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
        self.data_file = os.path.join(self.data_dir, "user_data.json")

        self.add_remove_buttons = AddRemovePlaylist(self)
        self.add_remove_buttons.move(1700, 850)
        self.add_remove_buttons.add_playlist.clicked.connect(self.add_playlist)
        self.add_remove_buttons.remove_playlist.clicked.connect(self.remove_playlist)

        x = 225
        y = 130
        for i in range(len(self.playlist_dict)):
            playlist_cover = PlaylistCover(self)
            playlist_cover.move(x, y)
            self.playlist_covers.append(playlist_cover)

            for index, (key, value) in enumerate(self.playlist_dict.items()):
                if index == i:
                    self.key = key
                    break

            select_image_button = SelectImageButton(self)
            self.select_image_buttons.append(select_image_button)
            select_image_button.clicked.connect(lambda checked, idx=i: self.open_file_dialog(idx))
            select_image_button.move(x + 8, y + 50)

            name_button = NameButton(self)
            name_button.setText(f"{self.key}")
            name_button.move(x + 60, y + 320)
            self.name_buttons.append(name_button)
            x += 300
            if i == 4:
                x = 225
                y += 400
            name_button.clicked.connect(lambda checked, name = self.key: self.open_main_ui(name))
        self.showMaximized()
    
    def open_main_ui(self, name):
        self.hide()
        self.main_ui = MainUi(self, name)
        self.main_ui.show()
    
    def open_file_dialog(self, idx):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        if file_path:
            pixmap = self.get_rounded_pixmap(file_path, 35)
            self.playlist_covers[idx].image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    
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

    def add_playlist(self):
        self.hide()
        self.addremoveui = AddRemoveUi(self, "add")

    def remove_playlist(self):
        self.hide()
        self.addremoveui = AddRemoveUi(self, "remove")
    
    def refresh_playlists(self):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        self.playlist_dict = data  # Update the playlist dictionary

        # Clear the existing buttons and covers
        for widget in self.playlist_covers + self.name_buttons + self.select_image_buttons:
            widget.deleteLater()

        # Re-create UI elements with the updated playlist dictionary
        self.playlist_covers = []
        self.name_buttons = []
        self.select_image_buttons = []

        x = 225
        y = 130
        for i in range(len(self.playlist_dict)):
            playlist_cover = PlaylistCover(self)
            playlist_cover.move(x, y)
            self.playlist_covers.append(playlist_cover)

            for index, (key, value) in enumerate(self.playlist_dict.items()):
                if index == i:
                    self.key = key
                    break

            select_image_button = SelectImageButton(self)
            self.select_image_buttons.append(select_image_button)
            select_image_button.clicked.connect(lambda checked, idx=i: self.open_file_dialog(idx))
            select_image_button.move(x + 8, y + 50)

            name_button = NameButton(self)
            name_button.setText(f"{self.key}")
            name_button.move(x + 60, y + 320)
            self.name_buttons.append(name_button)
            x += 300
            if i == 4:
                x = 225
                y += 400
            name_button.clicked.connect(lambda checked, name=self.key: self.open_main_ui(name))