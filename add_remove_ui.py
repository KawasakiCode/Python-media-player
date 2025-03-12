from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit
import os
import json

class AddRemoveUi(QMainWindow):
    def __init__(self, playlist_select_ui, caller):
        super().__init__()
        self.playlist_select_ui = playlist_select_ui
        self.caller = caller
        self.setWindowTitle("Spotify alla better")
        self.setStyleSheet("background: black;")
        self.data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
        self.data_file = os.path.join(self.data_dir, "user_data.json")

        self.bglabel = QLabel("", self)
        if self.caller == "add":
            self.textlabel = QLabel("Add playlist", self)
        else:
            self.textlabel = QLabel("Remove playlist", self)
        if self.caller == "add":
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
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter the name of your new playlist")
        self.name_input.setFocus()

        self.pathempty = QLabel("Don't hit enter with empty path", self)
        self.patherror = QLabel("The path doesn't exist or it's not a directory", self)
        self.nameempty = QLabel("Don't hit enter with empty name", self)
        self.empty = QLabel("Don't hit enter with empty fields", self)
        self.more_chars = QLabel("Names can be up to 15 characters long", self)

        self.pathempty.hide()
        self.patherror.hide()
        self.nameempty.hide()
        self.empty.hide()
        self.more_chars.hide()

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
        self.more_chars.setStyleSheet("""
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
        self.patherror.setFixedSize(400, 30)
        self.pathempty.setFixedSize(400, 30)
        self.nameempty.setFixedSize(400, 30)
        self.empty.setFixedSize(400, 30)
        self.more_chars.setFixedSize(400, 30)
        if(self.caller == "add"):
            self.bglabel.setFixedSize(500, 250)
        else: 
            self.bglabel.setFixedSize(500, 200)

        self.bglabel.move(710, 250)
        self.textlabel.move(760, 300)
        self.name_input.move(760, 370)
        self.pathempty.move(760, 330)
        self.patherror.move(760, 330)
        self.nameempty.move(760, 330)
        self.more_chars.move(760, 330)
        self.empty.move(760, 330)

        self.showMaximized()
    
    def process_input(self):
        self.pathempty.hide()
        self.patherror.hide()
        self.nameempty.hide()
        self.more_chars.hide()
        self.empty.hide()
        if self.caller == "add":
            if not self.path_input.text() and not self.name_input.text():
                self.empty.show()
            elif not self.path_input.text():
                self.pathempty.show()
            elif not self.name_input.text():
                self.nameempty.show()
            elif not os.path.isdir(self.path_input.text()):
                self.patherror.show()
            elif len(self.name_input.text()) > 15:
                self.more_chars.show()
            else:
                self.create_playlist(self.path_input.text(), self.name_input.text())
                self.path_input.clear()
                self.name_input.clear()
                self.close()
                self.playlist_select_ui.refresh_playlists()
                self.playlist_select_ui.show()
        else:
            if not self.name_input.text():
                self.nameempty.show()
            elif len(self.name_input.text()) > 15:
                self.more_chars.show()
            else:
                self.remove_playlist(self.name_input.text())
                self.name_input.clear()
                self.close()
                self.playlist_select_ui.refresh_playlists()
                self.playlist_select_ui.show()
        
    def create_playlist(self, path, name):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        
        data[name] = path
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent = 4)
    
    def remove_playlist(self, name):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                print(data)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if name in data:
            del data[name]
            with open(self.data_file, "w") as file:
                json.dump(data, file, indent = 4)
        else:
            print("Incorrect name")

            
                

