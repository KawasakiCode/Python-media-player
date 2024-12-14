import tkinter as tk
from tkinter import *
from ui import GUI
import eyed3
from PIL import Image, ImageTk
import io
import os

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
        self.setup_buttons_and_images()
        self.protocol("WM_DELETE_WINDOW", self.close_all)

    #set up button with lambda function to pass argument to load directory
    def setup_buttons_and_images(self):
        #Make as many buttons as the playlists the user made
        if(self.name):
            self.names = self.name.split(",")
            for _ in range(5 - len(self.names)):
                self.names.append("none")
        else:
            print("There was an error loading tha paths and names")
        X = 200
        #Create buttons with different names and lambda functions to call a different playlist each time
        self.final_images = []
        self.path_list = self.playlistmanager.return_paths()
        for i in range(int(self.user_input)):
            button = Button(self, text = self.names[i], background = "black", activebackground = "black", 
                                  font = ("Arial", 15), highlightthickness = 0, bd = 0, fg = "white",
                                  command = lambda i = i: self.load_gui(self.names[i]), anchor = "center")
                                  #in the lambda have argument i = i or else all lambdas will use the last i as the argument
            button.place(x = 340 + i * 350, y = 500)
            self.images = []
            for j in range(4):
                files = os.listdir(self.path_list[i])
                first_four_files = files[:4]
                audio_file = eyed3.load(os.path.join(self.path_list[i], first_four_files[j])) #no song list but from each path needs change
                if audio_file.tag.images:
                    image = audio_file.tag.images[0]
                    image_data = image.image_data
                    img = Image.open(io.BytesIO(image_data))
                    img = img.resize((150, 150))
                    self.images.append(img)
            
            self.combined_image = Image.new("RGB", (300, 300))
            
            self.combined_image.paste(self.images[0], (0, 0))
            self.combined_image.paste(self.images[1], (150, 0))
            self.combined_image.paste(self.images[2], (0, 150))
            self.combined_image.paste(self.images[3], (150, 150))
            
            self.combined_photo = ImageTk.PhotoImage(self.combined_image)
            self.final_images.append(self.combined_photo)

            self.image_label = Label(self, image = self.final_images[i], bg = "black", activebackground = "black", 
                                    relief = "flat", highlightthickness = 0, bd = 0)
            self.image_label.place(x = X + i * 350, y = 150)   

    def load_gui(self, playlist):
        #hide this window and instantiate the gui class window
        self.music_player = self.playlistmanager.load_directory(playlist)
        self.withdraw()
        GUI(self, self.music_player)
    
    def close_all(self):
        self.destroy()
        self.quit()

