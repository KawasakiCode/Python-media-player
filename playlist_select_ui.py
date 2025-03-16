from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtGui import QPixmap, QIcon
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
        self.setWindowIcon(QIcon("Assets/icon.ico"))

        self.playlist_covers = []
        self.name_buttons = []
        self.select_image_buttons = []
        
        self.data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
        self.data_file = os.path.join(self.data_dir, "user_data.json")
        self.image_data_file = os.path.join(self.data_dir, "image_data.json")
        
        if self.ensure_file_exists():
            with open(self.image_data_file, "r") as file:
                self.image_data_dict = json.load(file)          

        self.add_remove_buttons = AddRemovePlaylist(self)
        self.add_remove_buttons.move(1700, 850)
        self.add_remove_buttons.add_playlist.clicked.connect(self.add_playlist)
        self.add_remove_buttons.remove_playlist.clicked.connect(self.remove_playlist)

        x = 225
        y = 130
        for i in range(len(self.playlist_dict)):
            if self.ensure_file_exists() and (str(i) in self.image_data_dict):
                playlist_cover = PlaylistCover(self, self.image_data_dict[str(i)])
                self.playlist_covers.append(playlist_cover)
            else:
                playlist_cover = PlaylistCover(self, "default")
                self.playlist_covers.append(playlist_cover)
            playlist_cover.move(x, y)

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
        self.add_data_to_file(file_path, idx)
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
            if not os.path.getsize(self.data_file) == 0:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
            else:
                data = {}
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if self.ensure_file_exists() and not os.path.getsize(self.image_data_file) == 0:
            with open(self.image_data_file, "r") as file:
                self.image_data_dict = json.load(file)
        else:
            self.image_data_dict = {}

        self.playlist_dict = data

        for widget in self.playlist_covers + self.name_buttons + self.select_image_buttons:
            widget.deleteLater()

        self.playlist_covers = []
        self.name_buttons = []
        self.select_image_buttons = []

        x = 225
        y = 130
        for i in range(len(self.playlist_dict)):
            if self.ensure_file_exists() and (str(i) in self.image_data_dict):
                playlist_cover = PlaylistCover(self, self.image_data_dict[str(i)])
                self.playlist_covers.append(playlist_cover)
            else:
                playlist_cover = PlaylistCover(self, "default")
                self.playlist_covers.append(playlist_cover)
            playlist_cover.move(x, y)

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
    
    def add_data_to_file(self, data, index):
        if self.ensure_file_exists() and not os.path.getsize(self.image_data_file) == 0:
            with open(self.image_data_file, "r") as file:
                data_dict = json.load(file)
            data_dict[index] = data
            with open(self.image_data_file, "w") as file:
                json.dump(data_dict, file, indent = 4)
        else:
            data_dict = {}
            data_dict[index] = data
            with open(self.image_data_file, "w") as file:
                json.dump(data_dict, file, indent = 4)
    
    def ensure_file_exists(self):
        return os.path.exists(self.image_data_file)