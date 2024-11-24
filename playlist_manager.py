import os
from player import MusicPlayer

class PlaylistManager:
    def __init__(self):
        self.music_player = MusicPlayer()

    def load_directory(self, playlist):
        #check which playlist to load 
        if(playlist == "playlist1"):
            directory = r"D:\Pantelis\playlist"
        elif(playlist == "playlist2"):
            directory = r"D:\Pantelis\playlist2"
        elif(playlist == "playlist3"):
            directory = r"D:\Pantelis\playlist3"
        #load the songs of the playlist to the music player
        self.SONGS_LIST = [os.path.join(directory, file) for file in os.listdir(directory)]
        self.music_player.load_song(self.SONGS_LIST)
        
        return self.music_player

