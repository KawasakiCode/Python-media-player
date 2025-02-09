import os
from player import MusicPlayer
import json

class PlaylistManager:
    def __init__(self, path, name, user_input):
        self.music_player = MusicPlayer()
        self.path = path
        self.name = name
        self.user_input = user_input
        self.data_dict = {}
        self.data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")
        self.data_file = os.path.join(self.data_dir, "user_data.json")

        if not os.path.exists(self.data_dir):
            self.separate_paths_names()
            self.add_data_to_file()
        else:
            self.data_dict = self.load_data_from_file()
            self.names = list(self.data_dict.keys())
            self.paths = list(self.data_dict.values())

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

    def add_data_to_file(self):
        os.makedirs(self.data_dir)
        if(self.name and self.path):
            self.names = self.name.split(",")
            self.paths = self.path.split(",")
            #Load the list with none if user enters less than 5 playlists
            for _ in range(5 - len(self.names)):
                self.names.append(None)
                self.paths.append(None)
            for i in range(5):
                if self.names[i] is not None:
                    self.data_dict.update({self.names[i]: self.paths[i]})
        else:
            print("There was an error loading tha paths and namess")
        with open(self.data_file, "w") as file:
            json.dump(self.data_dict, file, indent = 4)

    def return_paths(self):
        return self.paths
    
    def load_data_from_file(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                return json.load(file)
        return None

