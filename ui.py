import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from player import MusicPlayer
import os
import io

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.music_player = MusicPlayer()
        self.DIRECTORY = r"D:\Pantelis\playlist"
        self.SONGS_LIST = [os.path.join(self.DIRECTORY, file) for file in os.listdir(self.DIRECTORY)]
        self.music_player.load_song(self.SONGS_LIST)

        self.title("Spotify alla better")
        self.state("zoomed")
        self.configure(bg = "black")

        self.setup_buttons()
        self.setup_labels()
        self.setup_slider()

        self.show_metadata()
        self.update_time()
        self.update_scale()
        self.autoplay_next()

    def setup_buttons(self):
        #Load pause button
        original_pause = Image.open("Assets/Pause_button.png")
        self.setup_button_image(original_pause, 40, 915, "pause", self.music_player.pause_song)

        #Load next button
        original_next = Image.open("Assets/Next_song_button.png")
        self.setup_button_image(original_next, 30, 920, "next", self.music_player.next_song)

        #Load previous button
        original_previous = Image.open("Assets/Previous_song_button.png")
        self.setup_button_image(original_previous, 30, 920, "previous", self.music_player.previous_song)

        #Load play button
        original_play = Image.open("Assets/play_button.png")
        self.setup_button_image(original_play, 50, 908, "play", self.music_player.play_song)


    def setup_button_image(self, original_image, target_width, y_pos, button_name, command):
        #Load and resize the button images
        aspect_ratio = original_image.width / original_image.height
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        button_image = ImageTk.PhotoImage(resized_image)

        button = tk.Button(self, bd=0, cursor="hand2", image=button_image, borderwidth=0, highlightthickness=0,
                        relief="flat", activebackground="black", command=command)
        button.image = button_image
        if button_name == "pause":
            button.place(x=1007, y=y_pos)
        elif button_name == "next":
            button.place(x=1070, y=y_pos)
        elif button_name == "previous":
            button.place(x=880, y=y_pos)
        elif button_name == "play":
            button.place(x=935, y=y_pos)

    def setup_labels(self):
        # Label to show the song time
        self.time_label = Label(self, text="0:00", background="black", height=10, width=25, bd=0,
                                font=("Arial", 10), relief="flat", fg="gray")
        self.time_label.place(x=510, y=910)

        # Label to show the end time of the song
        self.end_time_label = Label(self, text="0:00", background="black", height=10, width=25, bd=0,
                                    font=("Arial", 10), relief="flat", fg="gray")
        self.end_time_label.place(x=1210, y=910)

        #Labels to show metadata
        self.title_label = Label(self, text = "Title", background = "black", font = ("Arial", 15), fg = "white", relief = "flat",
                                 height = 10, width = 50, bd = 0, anchor = "nw")
        self.title_label.place(x = 60, y = 890, height = 30, width = 300)

        self.artist_label = Label(self, text = "Artist", background = "black", font = ("Arial", 12), fg = "gray", relief = "flat",
                                 height = 10, width = 50, bd = 0, anchor = "nw")
        self.artist_label.place(x = 60, y = 923, height = 30, width = 300)
        
        self.album_label = Label(self, text = "Album", background = "black", font = ("Arial", 12), fg = "gray", relief = "flat",
                                 height = 10, width = 50, bd = 0, anchor = "nw")
        self.album_label.place(x = 60, y = 950, height = 30, width = 300)

        self.cover_label = Label(self, image = None, background = "black", fg = "gray", relief = "flat",
                                 height = 50, width = 50, bd = 0, anchor = "nw")
        self.cover_label.place(x = 400, y = 300, height = 100, width = 100)


    def setup_slider(self):
        # Slider to control song position
        START = 0
        end = self.music_player.get_length_in_sec()
        self.length_slider = ttk.Scale(self, from_=START, to=end, orient="horizontal", length=655)
        self.length_slider.place(x=635, y=977)

    def update_time(self):
        #Update the time of the song every second
        if self.music_player.is_playing:
            current_time = self.music_player.get_song_position()
            self.time_label.config(text=current_time)

        end_time = self.music_player.get_length()
        self.end_time_label.config(text=end_time)

        # Recall update_time every second
        self.after(1000, self.update_time)

    def update_scale(self):
        #Update the slider position every second
        if self.music_player.is_playing:
            self.length_slider.set(self.music_player.get_song_position_sec())
            self.length_slider.config(to=self.music_player.get_length_in_sec())

        self.after(1000, self.update_scale)

    def autoplay_next(self):
        #Autoplay next song 
        current_time = self.music_player.get_song_position_sec()
        end_time = self.music_player.get_length_in_sec()
        if current_time == end_time:
            self.music_player.next_song()

        self.after(1000, self.autoplay_next)
    
    def show_metadata(self):
        #Show the data of each song 
        metadata = self.music_player.get_metadata()
        self.title_label.config(text = metadata["Title"])
        formatted_artist = metadata["Artist"].replace("/", ",")
        self.artist_label.config(text = formatted_artist)
        self.album_label.config(text = metadata["Album"])

        '''image_data = metadata["Album_cover"].image_data
        img = Image.open(io.BytesIO(image_data))
        img = img.resize((100, 100))
        image = ImageTk.PhotoImage(img)
        self.cover_label.config(image = image)
        '''
        self.after(1000, self.show_metadata)