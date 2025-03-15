from PySide6.QtWidgets import QMainWindow
from widgets.change_playlist_button import Change_playlist
from widgets.next_button import NextButton
from widgets.pause_button import PauseButton
from widgets.previous_button import RewindButton
from widgets.play_button import PlayButton
from widgets.spotify_slider import Widget
from widgets.volume_slider import VolumeSlider
from widgets.title_artist_labels import TitleArtistLabels
from widgets.search_song import SearchBar
from widgets.add_queue import QueueBar
from widgets.album_image import AlbumImage
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QBrush, QIcon
from PIL import Image
import os
import sys
import io

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from player import MusicPlayer

class MainUi(QMainWindow):
    def __init__(self, playlist_select_ui, playlist_name):
        super().__init__()
        self.setWindowTitle("Spotify alla batter")
        self.setStyleSheet("background: black;")
        self.setWindowIcon(QIcon("Assets/icon.ico"))

        self.playlist_select_ui = playlist_select_ui
        self.playlist_name = playlist_name
        self.playlist_path = self.playlist_select_ui.playlist_dict[self.playlist_name]
        self.music_player = MusicPlayer()
        self.songs_list = [os.path.join(self.playlist_path, file) for file in os.listdir(self.playlist_path)]
        self.music_player.load_song(self.songs_list)

        self.rewind_button = RewindButton(self)
        self.play_button = PlayButton(self)
        self.pause_button = PauseButton(self)
        self.next_button = NextButton(self)
        self.change_playlist_button = Change_playlist(self)
        self.volume_slider = VolumeSlider(self)
        self.progress_slider = Widget(self)
        self.title_labels = TitleArtistLabels(self)
        self.search_bar = SearchBar(self)
        self.queue_bar = QueueBar(self)
        self.album_image = AlbumImage(self)

        self.pause_button.clicked_paused.connect(self.toggle_buttons)
        self.play_button.clicked_play.connect(self.toggle_buttons)
        self.change_playlist_button.clicked.connect(self.back_to_selection)
        self.next_button.clicked.connect(self.music_player.next_song)
        self.rewind_button.clicked.connect(self.music_player.previous_song)
        self.volume_slider.slider.valueChanged.connect(self.update_volume)
        self.search_bar.search_input.textChanged.connect(self.update_results)
        self.search_bar.result_list.itemDoubleClicked.connect(self.select_result)
        self.queue_bar.search_input.textChanged.connect(self.update_results_queue)
        self.queue_bar.result_list.itemDoubleClicked.connect(self.create_custom_queue)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_metadata)
        self.timer.timeout.connect(self.autoplay)
        self.timer.start(500)

        self.slider_timer = QTimer(self)
        self.slider_timer.timeout.connect(self.update_slider)
        self.slider_timer.start(1000)



        self.showMaximized()
        
    def showEvent(self, event):
        super().showEvent(event)
        self.rewind_button.move(887, 941)
        self.play_button.move(940, 938)
        self.pause_button.move(940, 938)
        self.next_button.move(1000, 941)
        self.change_playlist_button.move(1770, 970)
        self.volume_slider.move(1550, 965)
        self.progress_slider.move(590, 965)
        self.title_labels.move(100, 925)
        self.search_bar.move(100, 75)
        self.queue_bar.move(1570, 75)
        self.album_image.move(790, 300)

    def toggle_buttons(self):
        if self.play_button.isVisible():
            self.music_player.play_song()
            self.play_button.hide()
            self.pause_button.show()
        else:
            self.music_player.pause_song()
            self.pause_button.hide()
            self.play_button.show()

    def back_to_selection(self):
        self.music_player.pause_song()
        self.close()
        self.playlist_select_ui.show()
    
    def show_metadata(self):
        #Show the data of each song 
        metadata = self.music_player.get_metadata()
        self.title_labels.title_label.setText(metadata["Title"])
        formatted_artist = metadata["Artist"].replace("/", ",")
        self.title_labels.artist_label.setText(formatted_artist)
        self.title_labels.album_name.setText(metadata["Album"])

        #get the image data convert it to an image object and open it
        image_data = metadata["Album_cover"]

        img = Image.open(io.BytesIO(image_data))
        img = img.resize((300, 300))
        img = img.convert("RGBA")
        qimage = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)

        pixmap = QPixmap.fromImage(qimage)
        pixmap = self.get_rounded_pixmap(pixmap, 20)

        self.album_image.image_label.setPixmap(pixmap)
    
    def get_rounded_pixmap(self, pixmap, radius):
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

    def update_slider(self):
        if self.music_player.is_playing:
            self.progress_slider.slider.setRange(0, self.music_player.get_length_in_sec())
            self.progress_slider.slider.setValue(self.music_player.get_song_position_sec())
            self.progress_slider.start_label.setText(self.music_player.get_song_position())
            self.progress_slider.end_label.setText(self.music_player.get_length())
        
    def autoplay(self):
        current_time = self.music_player.get_song_position_sec()
        end_time = self.music_player.get_length_in_sec()
        if end_time - current_time <= 1:
            self.music_player.next_song()
    
    def update_volume(self):
        volume = self.volume_slider.slider.value() / 100.0
        self.music_player.change_volume(volume)
    
    def update_results(self):
        query = self.search_bar.search_input.text().strip()
        self.search_bar.result_list.clear()

        if query:
            matches = [os.path.basename(path) for path in self.music_player.song_list if query in os.path.basename(path)]
            if matches:
                self.search_bar.result_list.addItems(matches)
                self.search_bar.result_list.show()  # Show list when there are results
            else:
                self.search_bar.result_list.hide()  # Hide list if no matches
        else:
            self.search_bar.result_list.hide()  # Hide list if query is empty
    
    def select_result(self, item):
        path = self.playlist_path
        selected_song_full_path = os.path.join(path, item.text())
        self.music_player.is_playing = False
        self.music_player.current_song = selected_song_full_path
        self.music_player.play_song()
        if self.play_button.isVisible():
            self.toggle_buttons()
        QTimer.singleShot(0, self.search_bar.result_list.hide)
        self.search_bar.search_input.clear()

    def update_results_queue(self):
        query = self.queue_bar.search_input.text().strip()
        self.queue_bar.result_list.clear()

        if query:
            matches = [os.path.basename(path) for path in self.music_player.song_list if query in os.path.basename(path)]
            if matches:
                self.queue_bar.result_list.addItems(matches)
                self.queue_bar.result_list.show()  # Show list when there are results
            else:
                self.queue_bar.result_list.hide()  # Hide list if no matches
        else:
            self.queue_bar.result_list.hide()  # Hide list if query is empty

    def create_custom_queue(self, item):
        path = self.playlist_path
        selected_song_full_path = os.path.join(path, item.text())
        self.music_player.custom_queue_list.append(selected_song_full_path)
        QTimer.singleShot(0, self.queue_bar.result_list.hide)
        self.queue_bar.search_input.clear()
