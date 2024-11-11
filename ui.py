import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from player import MusicPlayer
import os

music_player = MusicPlayer()

DIRECTORY = r"D:\Pantelis\playlist"
SONGS_LIST = [os.path.join(DIRECTORY, file) for file in os.listdir(DIRECTORY)]
music_player.load_song(SONGS_LIST)

root = Tk()
root.title("Spotify alla better")
root.state("zoomed")
root.configure(bg = "black")

original_pause = Image.open("Assets/Pause_button.png")

target_width_pause = 40
aspect_ratio_pause = original_pause.width / original_pause.height

new_width = target_width_pause
new_height = int(new_width / aspect_ratio_pause)
resized_image = original_pause.resize((new_width, new_height), Image.LANCZOS)

PAUSE_IMAGE = ImageTk.PhotoImage(resized_image)
pause = tk.Button(root, bd = 0, cursor = "hand2", 
                  image = PAUSE_IMAGE, borderwidth = 0, 
                  highlightthickness = 0, relief = "flat", activebackground= "black", command = music_player.pause_song)
pause.place(x = 940, y = 850)

original_next = Image.open("Assets/Next_song_button.png")

target_width_next = 30
aspect_ratio_next = original_next.width / original_next.height

new_next_width = target_width_next
new_next_height = int(new_next_width / aspect_ratio_next)
resized_next = original_next.resize((new_next_width, new_next_height), Image.LANCZOS)

NEXT_IMAGE = ImageTk.PhotoImage(resized_next)
next = tk.Button(root, bd = 0, cursor = "hand2", image = NEXT_IMAGE, borderwidth = 0,
    highlightthickness = 0,  relief="flat", activebackground= "black", command = music_player.next_song)
next.place(x = 1010, y = 920)

original_previous = Image.open("Assets/Previous_song_button.png")

new_previous_width = target_width_next
new_previous_height = int(new_previous_width / aspect_ratio_next)
resized_previous = original_previous.resize((new_previous_width, new_previous_height), Image.LANCZOS)

PREVIOUS_IMAGE = ImageTk.PhotoImage(resized_previous)
previous = tk.Button(root, bd = 0, cursor = "hand2", image = PREVIOUS_IMAGE, borderwidth = 0, 
    highlightthickness = 0,  relief="flat", activebackground= "black", command = music_player.previous_song)
previous.place(x = 880, y = 920)

original_play = Image.open("Assets/play_button.png")

aspect_ratio_play = original_play.width / original_play.height

target_width_play = 50

new_play_width = target_width_play
new_play_height = int(new_play_width / aspect_ratio_play)
resized_play = original_play.resize((new_play_width, new_play_height), Image.LANCZOS)

PLAY_IMAGE = ImageTk.PhotoImage(resized_play)
play = tk.Button(root, bd = 0, cursor = "hand2", image = PLAY_IMAGE, borderwidth = 0, highlightthickness = 0,
                 relief = "flat", activebackground = "black", command = music_player.play_song)
play.place(x = 935, y = 910)

def update_time():
    if music_player.is_playing:
        current_time = music_player.get_song_position()
        end_time = music_player.get_length()

        time_label.config(text = current_time)
        end_time_label.config(text = end_time)
        
    root.after(1000, update_time)

time_label = Label(root, text = "0:00", background = "black", height = 10, width = 25, 
                    bd = 0, font = ("Arial", 10), relief = "flat", fg="gray")
time_label.place(x = 510, y = 910)

end_time = music_player.get_length()
end_time_label = Label(root, text = "0:00", background = "black", height = 10, width = 25,
                        bd = 0, font = ("Arial", 10), relief = "flat", fg = "gray")
end_time_label.place(x = 1210, y = 910)

length_slider = ttk.Scale(root, from_=0, to=120, orient = "horizontal", length = 655)
length_slider.place(x = 635, y = 977)

update_time()

root.mainloop()