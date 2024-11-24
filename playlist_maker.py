import tkinter as tk
from tkinter import ttk
from tkinter import *
import os

class PlaylistMaker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spotify alla better")
        self.state("zoomed")
        self.configure(bg = "black")

        #Setup start labels and entry 
        self.setup_labels()
        self.setup_entry()
        self.error_label = None

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
        self.question_label.config(text = "Enter the paths to your playlists by separating them with comma:")
        self.question_label.place(x = 400, y = 400)
        #Paths entry
        self.pathentry = Entry(width = 30)
        self.pathentry.place(x = 400, y = 430)
        #Names label
        self.name_label = Label(text = "Enter the names of your playlists separated by coma", bd = 0, bg = "black",
                                fg = "gray", font = ("Arial", 13), height = 1, highlightthickness = 0, relief = "flat")
        self.name_label.place(x = 400, y = 450)
        #Names entry
        self.nameentry = Entry(width = 30)
        self.nameentry.place(x = 400, y = 480)
        #When enter is pressed enter paths and names
        self.pathentry.bind("<Return>", self.get_path)
        self.nameentry.bind("<Return>", self.get_name)        

    #Function to check the input of the entry is it is a number
    def is_input_number(self, char):
        return char.isdigit() or char == ""
    
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
    
    #Function that stores the paths in self
    def get_path(self, event = None):
        path = self.pathentry.get()
        if not path:
            print("Empty string inserted")
        else: 
            self.path = path
    
    #Function that sotres the names of the playlists in self
    def get_name(self, event = None):
        name = self.nameentry.get()
        if not name:
            print("Empty string inserted")
        else: 
            self.name = name
            self.add_paths(self.path, self.name, self.user_input)
    
    #Function to add the paths and call the playlist select ui 
    def add_paths(self, path, name, user_input):
        match int(user_input):
            case 1:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        print("success")
                    else:
                        print("There is no directory in this path")
                else:
                    print("This is not a valid path")
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case _:
                print("There was an error")