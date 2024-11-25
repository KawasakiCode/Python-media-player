import tkinter as tk
from tkinter import *
from player import MusicPlayer
import os
from ui import GUI
from playlist_manager import PlaylistManager

#inherit from tk.Tk because it is the parent window
class PlaylistSelectUI(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        #Initialize music player here\
        self.playlistmanager = PlaylistManager()
        self.title("Spotify alla better")
        self.state("zoomed")
        self.configure(bg = "black")
        self.setup_buttons()
        self.protocol("WM_DELETE_WINDOW", self.close_all)

    #TODO pass name string and the user input then separate them correctly
    #and make the playlists
    #set up button with lambda function to pass argument to load directory
    def setup_buttons(self):
        playlist1_button = Button(self, text = "Playlist 1", background = "black", activebackground = "black", 
                                  font = ("Arial", 13), highlightthickness = 0, bd = 0, fg = "white",
                                  command = lambda: self.load_gui("playlist1"))
        playlist1_button.place(x = 800, y = 700)

        playlist2_button = Button(self, text = "Playlist 2", background = "black", activebackground = "black", 
                                  font = ("Arial", 13), highlightthickness = 0, bd = 0, fg = "white", 
                                  command = lambda: self.load_gui("playlist2"))
        playlist2_button.place(x = 880, y = 700)

        playlist3_button = Button(self, text = "Playlist 3", background = "black", activebackground = "black", 
                                  font = ("Arial", 13), highlightthickness = 0, bd = 0, fg = "white", 
                                  command = lambda: self.load_gui("playlist3"))
        playlist3_button.place(x = 960, y = 700)

    def load_gui(self, playlist):
        #hide this window and instantiate the gui class window
        self.music_player = self.playlistmanager.load_directory(playlist)
        self.withdraw()
        GUI(self, self.music_player)
    
    def close_all(self):
        self.destroy()
        self.quit()

