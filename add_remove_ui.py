from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit
from PySide6.QtGui import QIcon
from widgets.back_button import BackButton
import os
import json
import sys

class AddRemoveUi(QMainWindow):
    def __init__(self, playlist_select_ui, caller):
        super().__init__()
        self.playlist_select_ui = playlist_select_ui
        self.caller = caller

        self.setWindowTitle("Spotify alla better")
        self.setStyleSheet("background: black;")
        self.setWindowIcon(QIcon(self.resource_path("Assets/icon.ico")))

        self.data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
        self.data_file = os.path.join(self.data_dir, "user_data.json")
        self.image_data_file = os.path.join(self.data_dir, "image_data.json")

        self.bglabel = QLabel("", self)
        if self.caller == "add":
            self.textlabel = QLabel("Add playlist", self)
            self.path_input = QLineEdit(self)
            self.path_input.setPlaceholderText("Enter the path of your new playlist")
            self.path_input.setFixedSize(400, 45)
            self.path_input.move(760, 420)
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
            self.path_input.returnPressed.connect(self.process_input)
        else:
            self.textlabel = QLabel("Remove playlist", self) 

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter the name of your new playlist")
        self.name_input.setFocus()

        self.back_button = BackButton(self)

        self.errorlabel = QLabel("", self)
        self.errorlabel.hide()

        self.textlabel.setStyleSheet("""
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
                font-weight: bold;
                color: white;
                background-color: gray;
                padding: 5px;
                border: none;
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
        self.errorlabel.setStyleSheet("""
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

        self.textlabel.setFixedSize(400, 30)
        self.name_input.setFixedSize(400, 45)
        self.errorlabel.setFixedSize(400, 30)
        if(self.caller == "add"):
            self.bglabel.setFixedSize(500, 250)
        else:
            self.bglabel.setFixedSize(500, 200)     

        self.bglabel.move(710, 250)
        self.textlabel.move(760, 300)
        self.name_input.move(760, 370)
        self.errorlabel.move(760, 330)
        self.back_button.move(50, 60)

        self.back_button.clicked.connect(self.go_back)

        self.showMaximized()
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

    def process_input(self):
        self.errorlabel.hide()
        if self.caller == "add":
            if not self.path_input.text() and not self.name_input.text():
                self.errorlabel.setText("Don't hit enter with empty fields")
                self.errorlabel.show()
            elif not self.path_input.text():
                self.errorlabel.setText("Don't hit enter with empty path")
                self.errorlabel.show()
            elif not self.name_input.text():
                self.errorlabel.setText("Don't hit enter with empty name")
                self.errorlabel.show()
            elif not os.path.isdir(self.path_input.text()):
                self.errorlabel.setText("The path doesn't exist or it's not a directory")
                self.errorlabel.show()
            elif len(self.name_input.text()) > 15:
                self.errorlabel.setText("Names can be up to 15 characters long")
                self.errorlabel.show()
            else:
                bool = self.create_playlist(self.path_input.text(), self.name_input.text())
                if bool:
                    self.path_input.clear()
                    self.name_input.clear()
                    self.close()
                    self.playlist_select_ui.refresh_playlists()
                    self.playlist_select_ui.show()
                    
        else:
            if not self.name_input.text():
                self.errorlabel.setText("Don't hit enter with empty name")
                self.errorlabel.show()
            else:
                bool = self.remove_playlist(self.name_input.text())
                if bool:
                    
                    self.name_input.clear()
                    self.close()
                    self.playlist_select_ui.refresh_playlists()
                    self.playlist_select_ui.show()
        
    def create_playlist(self, path, name):
        if self.is_audio_directory(path):
            try:
                if not os.path.getsize(self.data_file) == 0:
                    with open(self.data_file, "r") as file:
                        data = json.load(file)
                else:
                    data = {}
            except FileNotFoundError:
                data = {}
            if len(data) == 10:
                self.errorlabel.setText("You can make only up to 10 playlists as of now")
                self.errorlabel.show()
                return False
            else:
                if name in data:
                    self.errorlabel.setText("There is already a playlist with the same name")
                    self.errorlabel.show()
                    return False
                elif path in data.values():
                    self.errorlabel.setText("There is already a playlist with the same path")
                    self.errorlabel.show()
                    return False            
                else:
                    data[name] = path
                    with open(self.data_file, "w") as file:
                        json.dump(data, file, indent = 4)
                    return True
        else:
            self.errorlabel.setText("Select a directory with only audio files")
            self.errorlabel.show()
            return False
    
    def remove_playlist(self, name):
        try:
            if not os.path.getsize(self.data_file) == 0:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
            else:
                data = {}
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        self.iteration = 0
        if len(data) == 1:
            self.errorlabel.setText("You can't delete all playlists")
            self.errorlabel.show()
            return False
        elif len(data) == 0:
            self.errorlabel.setText("There was a file error")
            self.errorlabel.show()
            return False
        for i, (key, value) in enumerate(data.items()):
            if key == name:
                self.iteration = i
        
        if not os.path.getsize(self.image_data_file) == 0:
            with open(self.image_data_file, "r") as file:
                image_data = json.load(file)
        else:
            image_data = {}
        if str(self.iteration) in image_data:
            del image_data[str(self.iteration)]
            with open(self.image_data_file, "w") as file:
                json.dump(image_data, file, indent = 4)

        if name in data:
            del data[name]
            with open(self.data_file, "w") as file:
                json.dump(data, file, indent = 4)
            return True
        else:
            self.errorlabel.setText("There is no playlist with this name")
            self.errorlabel.show()
            return False
    
    def go_back(self):
        self.close()
        self.playlist_select_ui.show()
    
    def is_audio_directory(self, directory):
        audio_extensions = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"}
        
        try:
            files = os.listdir(directory)
            if not files:
                return False  

            return all(file.lower().endswith(tuple(audio_extensions)) for file in files if os.path.isfile(os.path.join(directory, file)))

        except FileNotFoundError:
            return False
        except PermissionError:
            return False

            
                

