import os
from player import MusicPlayer

class PlaylistManager:
    def __init__(self):
        self.music_player = MusicPlayer()

    def select_playlist(self, directory):
        self.songslist = [os.path.join(directory, file) for file in os.listdir(directory)]
        self.music_player.load_song(self.songslist)

