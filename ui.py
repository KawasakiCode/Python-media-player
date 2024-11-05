import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Spotify alla better")

HEIGHT = root.winfo_screenheight()
WIDTH = root.winfo_screenwidth()
root.geometry(f'{WIDTH}x{HEIGHT}')

original_image = Image.open("Assets/Pause_button.png")

target_width = 30
aspect_ratio = original_image.width / original_image.height

new_width = target_width
new_height = int(new_width / aspect_ratio)

resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

PAUSE_IMAGE = ImageTk.PhotoImage(resized_image)
pause = tk.Button(root, bd = 1, cursor = "hand2", 
                  image = PAUSE_IMAGE, borderwidth = 0, highlightthickness = 0)
pause.pack(pady=50)


root.mainloop()