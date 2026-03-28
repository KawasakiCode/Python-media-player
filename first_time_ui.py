from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QIcon
from playlist_select_ui import PlaylistSelectUi
import os
import json
import sys

class FirstTimeUi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spotify alla better")
        self.setStyleSheet("background: black;")
        self.setWindowIcon(QIcon(self.resource_path("Assets/icon.ico")))

        self.data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
        self.data_file = os.path.join(self.data_dir, "user_data.json")

        self.bglabel = QLabel("", self)
        self.textlabel = QLabel("Let's create your first playlist", self)
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Enter the path of your playlist")
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter the name of your playlist")
        self.name_input.setFocus()
        self.textlabel2 = QLabel("Don't worry, you 'll be able to make more later", self)

        self.pathempty = QLabel("Don't hit enter with empty path", self)
        self.patherror = QLabel("The path doesn't exist or it's not a directory", self)
        self.nameempty = QLabel("Don't hit enter with empty name", self)
        self.empty = QLabel("Don't hit enter with empty fields", self)

        self.pathempty.hide()
        self.patherror.hide()
        self.nameempty.hide()
        self.empty.hide()

        self.textlabel.setStyleSheet("""
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: gray;
                padding: 5px;
                border: none;
        """)
        self.textlabel2.setStyleSheet("""
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: gray;
                padding: 5px;
                border: none;
        """)
        self.path_input.setStyleSheet("""
            QLineEdit {
                background-color: #1E1E1E;
                border-radius: 20px;
                padding: 10px 15px;
                font-size: 16px;
                color: white;
                border: none;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
        """)
        self.name_input.setStyleSheet("""
                QLineEdit {
                        background-color: #1E1E1E;
                        border-radius: 20px;
                        padding: 10px 15px;
                        font-size: 16px;
                        color: white;
                        border: none;
                }
                QLineEdit:focus {
                        border: 1px solid #4A90E2;
                }
        """)
        self.pathempty.setStyleSheet("""
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: gray;
                padding: 5px;
                border: none;
        """)
        self.patherror.setStyleSheet("""
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: gray;
                padding: 5px;
                border: none;
        """)
        self.nameempty.setStyleSheet("""
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: gray;
                padding: 5px;
                border: none;
        """)
        self.empty.setStyleSheet("""
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: gray;
                padding: 5px;
                border: none;
        """)
        self.bglabel.setStyleSheet("background: gray; border-radius: 25px;")

        self.name_input.returnPressed.connect(self.process_input)
        self.path_input.returnPressed.connect(self.process_input)

        self.textlabel.setFixedSize(400, 30)
        self.textlabel2.setFixedSize(400, 30)
        self.path_input.setFixedSize(400, 45)
        self.name_input.setFixedSize(400, 45)
        self.patherror.setFixedSize(400, 30)
        self.pathempty.setFixedSize(400, 30)
        self.nameempty.setFixedSize(400, 30)
        self.empty.setFixedSize(400, 30)
        self.bglabel.setFixedSize(500, 300)

        self.bglabel.move(710, 250)
        self.textlabel.move(760, 300)
        self.textlabel2.move(760, 330)
        self.path_input.move(760, 450)
        self.name_input.move(760, 400)
        self.pathempty.move(760, 360)
        self.patherror.move(760, 360)
        self.nameempty.move(760, 360)
        self.empty.move(760, 360)

        self.showMaximized()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

    def process_input(self):
        self.pathempty.hide()
        self.patherror.hide()
        self.nameempty.hide()
        self.empty.hide()
        if not self.path_input.text() and not self.name_input.text():
            self.empty.show()
        elif not self.path_input.text():
            self.pathempty.show()
        elif not self.name_input.text():
            self.nameempty.show()
        elif not os.path.isdir(self.path_input.text()):
            self.patherror.show()
        else:
            playlist_dict = self.create_playlist(self.path_input.text(), self.name_input.text())
            self.add_data_to_file(playlist_dict)
            self.path_input.clear()
            self.name_input.clear()
            self.close()
            self.playlist_select_ui = PlaylistSelectUi(playlist_dict)
            self.playlist_select_ui.show()
    
    def create_playlist(self, path, name):
        playlist_dict = {}
        playlist_dict.update({name : path})
        return playlist_dict

    def add_data_to_file(self, data_dict):
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)
        with open(self.data_file, "w") as file:
            json.dump(data_dict, file, indent = 4)