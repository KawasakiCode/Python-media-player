import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Spotify alla better")

HEIGHT = root.winfo_screenheight()
WIDTH = root.winfo_screenwidth()
root.geometry(f'{WIDTH}x{HEIGHT}')

original_pause = Image.open("Assets/Pause_button.png")

target_width = 40
aspect_ratio = original_pause.width / original_pause.height

new_width = target_width
new_height = int(new_width / aspect_ratio)
resized_image = original_pause.resize((new_width, new_height), Image.LANCZOS)

PAUSE_IMAGE = ImageTk.PhotoImage(resized_image)
pause = tk.Button(root, bd = 1, cursor = "hand2", 
                  image = PAUSE_IMAGE, borderwidth = 0, highlightthickness = 0)
pause.place(x = 940, y = 930)

original_next = Image.open("Assets/Next_song_button.png")

target_width_next = 30
aspect_ratio_next = original_next.width / original_next.height

new_next_width = target_width_next
new_next_height = int(new_next_width / aspect_ratio_next)
resized_next = original_next.resize((new_next_width, new_next_height), Image.LANCZOS)

NEXT_IMAGE = ImageTk.PhotoImage(resized_next)
next = tk.Button(root, bd = 1, cursor = "hand2", image = NEXT_IMAGE, borderwidth = 0,
    highlightthickness = 0)
next.place(x = 1010, y = 935)

original_previous = Image.open("Assets/Previous_song_button.png")

new_previous_width = target_width_next
new_previous_height = int(new_previous_width / aspect_ratio_next)
resized_previous = original_previous.resize((new_previous_width, new_previous_height), Image.LANCZOS)

PREVIOUS_IMAGE = ImageTk.PhotoImage(resized_previous)
previous = tk.Button(root, bd = 1, cursor = "hand2", image = PREVIOUS_IMAGE, borderwidth = 0, 
    highlightthickness = 0)
previous.place(x = 880, y = 935)

root.mainloop()