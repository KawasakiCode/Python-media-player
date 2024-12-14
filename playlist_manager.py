import os
from player import MusicPlayer

class PlaylistManager:
    def __init__(self, path, name, user_input):
        self.music_player = MusicPlayer()
        self.path = path
        self.name = name
        self.user_input = user_input

        self.separate_paths_names()

    #Correctly separate the paths and names 
    def separate_paths_names(self):
        if(self.name and self.path):
            self.names = self.name.split(",")
            self.paths = self.path.split(",")
            #Load the list with none if user enters less than 5 playlists
            for _ in range(5 - len(self.names)):
                self.names.append(None)
                self.paths.append(None)
        else:
            print("There was an error loading tha paths and names")

    def load_directory(self, playlist):
        #check which path to load 
        if(playlist == self.names[0]):
            directory = self.paths[0]
        elif(playlist == self.names[1]):
            directory = self.paths[1]
        elif(playlist == self.names[2]):
            directory = self.paths[2]
        elif(playlist == self.names[3]):
            directory = self.paths[3]
        elif(playlist == self.names[4]):
            directory = self.paths[4]
        
        #load the songs of the playlist to the music player
        self.SONGS_LIST = [os.path.join(directory, file) for file in os.listdir(directory)]
        self.music_player.load_song(self.SONGS_LIST)
        
        return self.music_player

    def return_paths(self):
        return self.paths

