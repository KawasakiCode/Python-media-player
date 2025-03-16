from PySide6.QtWidgets import QApplication
from first_time_ui import FirstTimeUi
from playlist_select_ui import PlaylistSelectUi
from PySide6.QtGui import QIcon, QGuiApplication
import os
import json
import sys

data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
data_file = os.path.join(data_dir, "user_data.json")

def ensure_data_directory():
    return os.path.exists(data_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QGuiApplication.setWindowIcon(QIcon("Assets/icon.ico"))
    if ensure_data_directory() and not os.path.getsize(data_file) == 0:
        print("here")
        with open(data_file, "r") as file:
            file_dir = json.load(file)
        window = PlaylistSelectUi(file_dir)
    else:
        window = FirstTimeUi()
    window.show()
    app.exec()