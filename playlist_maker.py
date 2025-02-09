import tkinter as tk
from tkinter import *
import os
from playlist_manager import PlaylistManager
from playlistselectui import PlaylistSelectUI
import re

class PlaylistMaker(tk.Tk):
    def __init__(self, caller):
        super().__init__()

        self.title("Spotify alla better")
        self.state("zoomed")
        self.configure(bg = "black")
        self.caller = caller
        self.name = ""
        self.path = ""
        self.user_input = ""

        #Setup start labels and entry 
        if self.caller == "file=false":
            self.setup_labels()
            self.setup_entry()
            self.error_label = None
        elif self.caller == "file=true":
            self.add_paths(self.path, self.name)

    #Setup labels
    def setup_labels(self):
        self.question_label = Label(text = "How many playlists you want to load (1 - 5)?", font = ("Arial", 13), height = 1, bd = 0, 
                               background = "black", fg = "gray", relief = "flat", anchor = "center", highlightthickness = 0)
        self.question_label.place(x = 400, y = 400)
    
    #Setup entry
    def setup_entry(self):
        #Value that is used to check is the entry input is a number between 1, 5
        vcmd = self.register(self.is_input_number)
        self.entry = Entry(validate = "key", validatecommand = (vcmd, "%S"), width = 30)
        self.entry.place(x = 400, y = 430)
        self.entry.bind("<Return>", self.process_input)

    #Function that sets the second part of the ui by asking the user to input the names and paths of the playlists
    def get_playlist_paths(self):
        #Hide the labels and entry of the previous part of the ui
        self.question_label.place_forget()
        self.entry.place_forget()
        if self.error_label is not None:
            self.error_label.place_forget()
        #Show new labels and entries
        self.question_label.config(text = "Enter the paths to your playlists separated by comma:")
        self.question_label.place(x = 400, y = 400)
        #Paths entry
        self.pathentry = Entry(width = 30)
        self.pathentry.place(x = 400, y = 425)
        #Names label
        self.name_label = Label(text = "Enter the names of your playlists separated by comma:", bd = 0, bg = "black",
                                fg = "gray", font = ("Arial", 13), height = 1, highlightthickness = 0, relief = "flat")
        self.name_label.place(x = 400, y = 450)
        #Names entry
        self.nameentry = Entry(width = 30)
        self.nameentry.place(x = 400, y = 475) 
        #Button to handle the entries inputs
        self.reput = Label(text = "", height = 1, bd = 0, bg = "black", fg = "gray", font = ("Arial", 10))
        self.patherror = Label(text = "", height = 1, bd = 0, bg = "black", fg = "gray", font = ("Arial", 10))
        entry_button = Button(text = "Enter paths and names", bd = 0, background = "gray", fg = "white",
                              highlightthickness = 0, relief = "flat", font = ("Arial", 10), command = lambda: self.process_entries_input(self.reput, self.patherror))
        entry_button.place(x = 400, y = 550)
        go_back_button = Button(text = "Go back?", bd = 0, background = "gray", fg = "white",
                              highlightthickness = 0, relief = "flat", font = ("Arial", 10), command = self.returnagain)      
        go_back_button.place(x = 400, y = 580)

    #Function that gets called when enter is pressed for entry
    def process_input(self, event = None):
        self.user_input = self.entry.get()
        #If correct input
        if 1 <= int(self.user_input) <= 5:
            #Empty the entry
            self.entry.delete(0, tk.END)
            #Call the second page of the ui
            self.get_playlist_paths()
        else:
            #If incorrect input make a label to repeat the correct input range and wait for input again
            self.error_label = Label(self, text = "Please enter a number between 1 - 5", fg = "gray", bg = "black", bd = 0, 
                                highlightthickness = 0, relief = "flat", font = ("Arial", 11))
            self.error_label.place(x = 400, y = 480)
            self.entry.delete(0, tk.END)
    
    #Function that stores the paths and names in self
    def process_entries_input(self, reput, patherror):
        self.name = self.nameentry.get()
        self.path = self.pathentry.get()
        
        reput.update_idletasks()
        patherror.update_idletasks()
        if not self.name and not self.path:
            reput.config(text = "Dont' submit empty fields")
        elif(not self.name):
            reput.config(text = "Don't submit with empty name field")
        elif(not self.path):
            reput.config(text = "Don't submit with empty path field")
        else:
            self.path = re.sub(r'\s*, \s*', ',', self.path)
            self.name = re.sub(r'\s*, \s*', ',', self.name)
            self.paths = self.path.split(",")
            self.names = self.name.split(",")
            for i in self.paths:
                if(os.path.exists(i)):
                    if(os.path.isdir(i)):
                        if(int(self.user_input) == len(self.paths) and int(self.user_input) == len(self.names)):
                            self.add_paths(self.path, self.name)
                            break
                        elif(int(self.user_input) != len(self.paths) and int(self.user_input) == len(self.names)):
                            patherror.config(text = f"You inserted {len(self.paths)} paths while trying to create {self.user_input} playlists")
                        elif(int(self.user_input) == len(self.paths) and int(self.user_input) != len(self.names)):
                            patherror.config(text = f"You inserted {len(self.names)} names while trying to create {self.user_input} playlists")
                        else:
                            patherror.config(text = f"You inserted {len(self.paths)} paths and {len(self.names)} names while trying to create {self.user_input} playlists")
                    else:
                        patherror.config(text = f"Path no {self.paths.index(i)} is not a directory")
                else:
                        patherror.config(text = f"Path no {self.paths.index(i)} is not a valid path")
        patherror.place(x = 400, y = 520)
        reput.place(x = 400, y = 520)

    #Function to add the paths and call the playlist select ui 
    def add_paths(self, path, name):
        #Instantiate Playlist manager to check the paths and connect them to the correct names
        self.playlistmanager = PlaylistManager(path, name, self.user_input)
        self.withdraw()
        #Call the playlist select gui
        PlaylistSelectUI(self, self.user_input, self.name, self.playlistmanager)
    
    #Function to check the input of the entry is it is a number
    def is_input_number(self, char):
        return char.isdigit() or char == ""

    def returnagain(self):
        self.destroy()
        PlaylistMaker()
