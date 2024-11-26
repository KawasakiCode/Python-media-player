import tkinter as tk
from tkinter import *
from ui import GUI

#inherit from tk.Tk because it is the parent window
class PlaylistSelectUI(tk.Toplevel):
    def __init__(self, parent, user_input, name, playlistmanager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlistmanager = playlistmanager
        self.parent = parent
        self.user_input = user_input
        self.name = name

        #Initialize window here
        self.title("Spotify alla better")
        self.state("zoomed")
        self.configure(bg = "black")
        self.setup_buttons()
        self.protocol("WM_DELETE_WINDOW", self.close_all)

    #set up button with lambda function to pass argument to load directory
    def setup_buttons(self):
        #Make as many buttons as the playlists the user made
        if(self.name):
            self.names = self.name.split(",")
            for _ in range(5 - len(self.names)):
                self.names.append("none")
        else:
            print("There was an error loading tha paths and names")
        X = 400
        #Create buttons with different names and lambda functions to call a different playlist each time
        for i in range(int(self.user_input)):
            button = Button(self, text = self.names[i], background = "black", activebackground = "black", 
                                  font = ("Arial", 13), highlightthickness = 0, bd = 0, fg = "white",
                                  command = lambda i = i: self.load_gui(self.names[i]))
                                  #in the lambda have argument i = i or else all lambdas will use the last i as the argument
            button.place(x = X + i * 50, y = 500)

    def load_gui(self, playlist):
        #hide this window and instantiate the gui class window
        self.music_player = self.playlistmanager.load_directory(playlist)
        self.withdraw()
        GUI(self, self.music_player)
    
    def close_all(self):
        self.destroy()
        self.quit()

