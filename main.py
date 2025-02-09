from playlist_maker import PlaylistMaker
import os

data_dir = os.path.join(os.path.expanduser("~"), ".spotify_alla_better")

#Function to ensure data file exists or not
def ensure_data_directory():
    return not os.path.exists(data_dir)

if __name__ == "__main__":
    if(ensure_data_directory()):
        playlistmaker = PlaylistMaker("file=false")
        playlistmaker.mainloop()
    else:
        playlistmaker = PlaylistMaker("file=true")
        playlistmaker.mainloop()