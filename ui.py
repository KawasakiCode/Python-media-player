import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import io
import os

#inherit from tk.Toplevel because this will always be a child window
class GUI(tk.Toplevel):
    def __init__(self, parent, music_player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        #get the music player instance of the playlistselectui
        self.music_player = music_player
        self.protocol("WM_DELETE_WINDOW", self.close_all)

        self.title("Spotify alla better")
        self.state("zoomed")
        self.configure(bg = "black")

        #setup widgets
        self.setup_buttons()
        self.setup_labels()
        self.setup_slider()

        self.volume_slider.set(50)
        #run functions that handle time lables, metadata, the scale widget and the play next song automatically
        self.show_metadata()
        self.update_time()
        self.update_scale()
        self.autoplay_next()
        self.update_volume()
        self.setup_searchbars()

    def setup_buttons(self):
        #Load pause button
        original_pause = Image.open("Assets/pause.png")
        self.setup_button_image(original_pause, 36, 36, 925, "pause", self.toggle_play)

        #Load next button
        original_next = Image.open("Assets/next.png")
        self.setup_button_image(original_next, 30, 30, 928, "next", self.music_player.next_song)

        #Load previous button
        original_previous = Image.open("Assets/previous.png")
        self.setup_button_image(original_previous, 30, 30, 928, "previous", self.music_player.previous_song)

        #Load play button
        original_play = Image.open("Assets/play.png")
        self.setup_button_image(original_play, 36, 36, 925, "play", self.toggle_pause)

        select_playlist_button = tk.Button(self, text = "Change Playlist?", bd = 0, cursor = "hand2", borderwidth = 0,
                                           highlightthickness = 0, relief = "flat", background = "black", fg = "white", 
                                           font = ("Arial", 11), activebackground = "black", command = self.go_back_to_playlist)
        select_playlist_button.place(x = 1750, y = 950)

    def setup_searchbars(self):
        #song searchbar
        self.select_label = Label(self, text = "Search for a song", font = ("Arial", 11), bg = "black", fg = "white", 
                             relief = "flat", highlightthickness = 0, bd = 0, width = 25, anchor = "nw")
        self.select_label.place(x = 100, y = 60)
        self.select_song = Entry(self, font = ("Arial", 12))
        self.select_song.place(x = 100, y = 80)
        self.select_song_listbox = Listbox(self, font = ("Arial", 11), height = 5)
        self.select_song.bind("<KeyRelease>", self.on_keypress)
        self.select_song_listbox.bind("<Double-1>", self.play_song)

        #custom queue searchbar
        self.queue_label = Label(self, text = "Add to queue", font = ("Arial", 11), bg = "black", fg = "white", 
                             relief = "flat", highlightthickness = 0, bd = 0, width = 25, anchor = "nw")
        self.queue_label.place(x = 1550, y = 60)
        self.queue_song = Entry(self, font = ("Arial", 12))
        self.queue_song.place(x = 1550, y = 80)
        self.queue_song_listbox = Listbox(self, font = ("Arial", 11), height = 5)
        self.queue_song.bind("<KeyRelease>", self.on_keypress_queue)
        self.queue_song_listbox.bind("<Double-1>", self.create_custom_queue)

    def setup_button_image(self, original_image, width, height, y_pos, button_name, command):
        resized_image = original_image.resize((width, height), Image.LANCZOS)
        button_image = ImageTk.PhotoImage(resized_image)

        if button_name == "play":
            self.play_button = tk.Button(self, bd=0, cursor="hand2", image=button_image, borderwidth=0, highlightthickness=0,
                        relief="flat", activebackground="black", bg = "black", command=command)
            #keep the image as an attribute so python garbage collector won't delete it
            self.play_button.image = button_image
            self.play_button.place(x=945, y=y_pos)
        elif button_name == "pause":
            self.pause_button = tk.Button(self, bd=0, cursor="hand2", image=button_image, borderwidth=0, highlightthickness=0,
                        relief="flat", activebackground="black", bg = "black", command=command)
            self.pause_button.image = button_image
        elif button_name == "previous":
            self.previous_button = tk.Button(self, bd=0, cursor="hand2", image=button_image, borderwidth=0, highlightthickness=0,
                        relief="flat", activebackground="black", bg = "black", command=command)
            self.previous_button.image = button_image
            self.previous_button.place(x=892, y=y_pos)  
        elif button_name == "next":
            self.next_button = tk.Button(self, bd=0, cursor="hand2", image=button_image, borderwidth=0, highlightthickness=0,
                        relief="flat", activebackground="black", bg = "black", command=command)
            self.next_button.image = button_image
            self.next_button.place(x=1004, y=y_pos)
               
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
        self.title_label.place(x = 60, y = 890, height = 30, width = 650)

        self.artist_label = Label(self, text = "Artist", background = "black", font = ("Arial", 10), fg = "gray", relief = "flat",
                                 height = 10, width = 50, bd = 0, anchor = "nw")
        self.artist_label.place(x = 60, y = 923, height = 30, width = 650)
        
        self.album_label = Label(self, text = "Album", background = "black", font = ("Arial", 10), fg = "gray", relief = "flat",
                                 height = 10, width = 50, bd = 0, anchor = "nw")
        self.album_label.place(x = 60, y = 950, height = 30, width = 650)

        self.cover_label = Label(self, image = None, background = "black", fg = "gray", relief = "flat",
                                 height = 50, width = 50, bd = 0, anchor = "nw")
        self.cover_label.place(x = 810, y = 300, height = 300, width = 300)

        #Volume label
        original_image = Image.open("Assets/volume.png")
        aspect_ratio = original_image.width / original_image.height
        new_width = 30
        new_height = int(new_width / aspect_ratio)
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        self.volume_image = ImageTk.PhotoImage(resized_image)

        self.volume_label = Label(self, image = self.volume_image, relief = "flat", bd = 0, background = "black")
        self.volume_label.place(x = 1400, y = 976)

    def setup_slider(self):
        # Slider to control song position
        START = 0
        end = self.music_player.get_length_in_sec()
        self.length_slider = ttk.Scale(self, from_=START, to=end, orient="horizontal", length=656)
        self.length_slider.place(x=635, y=977)

        self.volume_slider = ttk.Scale(self, from_ = 0, to = 100, orient = "horizontal", length = 200)
        self.volume_slider.place(x = 1450, y = 977)

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

    def update_volume(self):
        volume = self.volume_slider.get()
        volume = volume / 100.0
        self.music_player.change_volume(volume)

        self.after(500, self.update_volume)

    def autoplay_next(self):
        #Autoplay next song 
        current_time = self.music_player.get_song_position_sec()
        end_time = self.music_player.get_length_in_sec()
        if end_time - current_time <= 1:
            self.music_player.next_song()

        self.after(500, self.autoplay_next)
    
    def show_metadata(self):
        #Show the data of each song 
        metadata = self.music_player.get_metadata()
        self.title_label.config(text = metadata["Title"])
        formatted_artist = metadata["Artist"].replace("/", ",")
        self.artist_label.config(text = formatted_artist)
        self.album_label.config(text = metadata["Album"])

        #get the image data convert it to an image object and open it
        image_data = metadata["Album_cover"]
        img = Image.open(io.BytesIO(image_data))
        img = img.resize((300, 300))
        self.image = ImageTk.PhotoImage(img)
        self.cover_label.config(image = self.image)
        

        self.after(1000, self.show_metadata)
    
    def go_back_to_playlist(self):
        #if the button change playlist is pressed destroy the window and show the parent window again
        self.destroy()
        self.parent.state("zoomed")
        self.music_player.pause_song()
        self.music_player.is_playing = False
        self.parent.deiconify()

    def on_keypress(self, event):
        #Function that triggers when a character is inserted into the search entry
        #Get the string from the entry
        search = self.select_song.get().strip()
        #Clear the listbox from previous searches
        self.select_song_listbox.delete(0, tk.END)
        #Take only the names of the songs not the whole path then search if the name matches 
        #with the base of a path in the songs lists
        matches = [os.path.basename(path) for path in self.music_player.song_list if search in os.path.basename(path)]
        #If matches show insert them into the listbox
        if matches:
            self.select_song_listbox.place(x = 100, y = 100)
            for song in matches:
                self.select_song_listbox.insert(tk.END, song)
        else:
            self.select_song_listbox.place_forget()

    def on_keypress_queue(self, event):
        #Get the string from the entry
        search = self.queue_song.get().strip()
        #Clear the listbox from previous searches
        self.queue_song_listbox.delete(0, tk.END)
        #Take only the names of the songs not the whole path then search if the name matches 
        #with the base of a path in the songs lists
        matches = [os.path.basename(path) for path in self.music_player.song_list if search in os.path.basename(path)]
        #If matches show insert them into the listbox
        if matches:
            self.queue_song_listbox.place(x = 1550, y = 100)
            for song in matches:
                self.queue_song_listbox.insert(tk.END, song)
        else:
            self.queue_song_listbox.place_forget()
  
    def play_song(self, event):
        #Function that triggers when double click happens on a song in the listbox
        #Save the directory of the song without its name
        directory = os.path.dirname(self.music_player.song_list[0])
        #Get the selection  from the listbox from where the cursor is
        selected_song = self.select_song_listbox.get(self.select_song_listbox.curselection())
        #Join the selected songs name with the directory from before to create its full path again
        selected_song_full_path = os.path.join(directory, selected_song)
        #Make the song play and hide the listbox
        self.music_player.is_playing = False
        self.music_player.current_song = selected_song_full_path
        #Add the song to the played queue
        #self.music_player.played_queue.append(selected_song_full_path)
        self.music_player.play_song()
        self.select_song_listbox.place_forget()
        self.select_song.delete(0, tk.END)

    def create_custom_queue(self, event):
        #Save the directory of the song without its name
        directory = os.path.dirname(self.music_player.song_list[0])
        #Get the selection  from the listbox from where the cursor is
        selected_song = self.queue_song_listbox.get(self.queue_song_listbox.curselection())
        #Join the selected songs name with the directory from before to create its full path again
        selected_song_full_path = os.path.join(directory, selected_song)
        #Add the song to the custom queue list and remove the listbox
        self.music_player.custom_queue_list.append(selected_song_full_path)
        self.queue_song_listbox.place_forget()
        self.queue_song.delete(0, tk.END)

    def close_all(self):
        self.destroy()
        self.quit()

    def toggle_pause(self):
        #when play is pressed
        self.play_button.place_forget()
        self.pause_button.place(x = 945, y = 925)
        self.music_player.play_song()
    
    def toggle_play(self):
        #when paused is pressed
        self.pause_button.place_forget()
        self.play_button.place(x = 945, y = 925)
        self.music_player.pause_song()