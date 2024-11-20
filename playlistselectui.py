import tkinter as tk
from tkinter import *
from player import MusicPlayer
import os
from ui import GUI

#inherit from tk.Tk because it is the parent window
class PlaylistSelectUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #Initialize music player here
        self.music_player = MusicPlayer()
        self.title("Spotify alla better")
        self.state("zoomed")
        self.configure(bg = "black")
        self.setup_buttons()

    #set up button with lambda function to pass argument to load directory
    def setup_buttons(self):
        playlist1_button = Button(self, text = "Playlist 1", background = "black", activebackground = "black", 
                                  font = ("Arial", 13), highlightthickness = 0, bd = 0, fg = "white",
                                  command = lambda: self.load_directory("playlist1"))
        playlist1_button.place(x = 800, y = 700)

        playlist2_button = Button(self, text = "Playlist 2", background = "black", activebackground = "black", 
                                  font = ("Arial", 13), highlightthickness = 0, bd = 0, fg = "white", 
                                  command = lambda: self.load_directory("playlist2"))
        playlist2_button.place(x = 880, y = 700)

        playlist3_button = Button(self, text = "Playlist 3", background = "black", activebackground = "black", 
                                  font = ("Arial", 13), highlightthickness = 0, bd = 0, fg = "white", 
                                  command = lambda: self.load_directory("playlist3"))
        playlist3_button.place(x = 960, y = 700)
    
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
        #hide this window and instantiate the gui class window
        self.withdraw()
        second_gui = GUI(self, self.music_player)

