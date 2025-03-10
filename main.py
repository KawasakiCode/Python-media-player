from PySide6.QtWidgets import QApplication
from first_time_ui import FirstTimeUi
from playlist_select_ui import PlaylistSelectUi
import os
import json

data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
data_file = os.path.join(data_dir, "user_data.json")

def ensure_data_directory():
    try:
        return os.path.exists(data_file)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON.")


if __name__ == "__main__":
    app = QApplication([])
    if ensure_data_directory():
        with open(data_file, "r") as file:
            file_dir = json.load(file)
        window = PlaylistSelectUi(file_dir)
    else:
        window = FirstTimeUi()
    window.show()
    app.exec()