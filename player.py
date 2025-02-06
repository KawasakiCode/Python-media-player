import pygame
import random
import eyed3

pygame.mixer.init()
eyed3.log.setLevel("ERROR")

class MusicPlayer:
    def __init__(self):
        self.is_playing = False
        self.current_song = None
        self.song_list = []
        self.current_position = 0
        self.is_paused = True
        self.song_length = 0
        self.custom_queue_list = []


    def load_song(self, song_paths):
        #if no songs are found print error
        if not song_paths:
            print("Error: No songs found")
            return
        #song list = the paths that got passed in the load
        self.song_list = song_paths
        #select a random index of the song list to pick a song
        self.create_shuffled_list()
        #index = random.randint(0, len(self.song_list) - 1)
        self.current_song = self.shuffled_list[self.index]
        #self.next_pressed = True
        #get song length for time labels in ui.py
        self.set_song_length()
    
    def get_metadata(self):
        #Load the current song and read its metadata and add them in a dictionary
        if self.current_song is not None:
            audio_file = eyed3.load(self.current_song)
            metadata = {}
            metadata.update([("Title", audio_file.tag.title), ("Artist", audio_file.tag.artist), ("Album", audio_file.tag.album)])
            if audio_file.tag.images:
                image = audio_file.tag.images[0]
                metadata.update({"Album_cover": image.image_data})
            return metadata

    def play_song(self):
        #if song is not playing load the current song and play it whilst getting its length
        if not self.is_playing:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.set_song_length()
        #if the song is paused unpause it
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    
    def pause_song(self):
        #if the song is playing pause it
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
    
    def next_song(self):
        #if the index is at the end of the list which means the whole playlist has been played make a new shuffled queue again
        #and start the index from 0 again (loses the previous queue)
        if self.custom_queue_list: #list is NOT empty
            self.current_song = self.custom_queue_list.pop(0)
        elif self.index == len(self.shuffled_list) - 1: #if the custom queue is empty
            self.create_shuffled_list()
            self.current_song = self.shuffled_list[self.index]
        #if the index is not at the end just increment it and play the next song in the queue
        else:
            self.index += 1
            self.current_song = self.shuffled_list[self.index]
        self.is_playing = False
        self.play_song()
    
    def previous_song(self):
        #if the index is at 0 which means the user presses previous as the first button remake a new shuffled list and play
        #the first song (like it is a random one) (can play the same song again especially in small playlists)
        if self.index == 0:
            self.create_shuffled_list()
        #if the index is not at 0 just play the previous song from the queue
        else:
            self.index -= 1
        self.current_song = self.shuffled_list[self.index]
        self.is_playing = False
        self.play_song()

    def get_song_position(self):
        #get the current time of the song in string format
        milliseconds = pygame.mixer.music.get_pos()
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02}"
    
    def get_song_position_sec(self):
        #get the time of the song in seconds format
        milliseconds = pygame.mixer.music.get_pos()
        return milliseconds // 1000

    def set_position(self, position):
        #set the position of the song manually
        pygame.mixer.music.play(start = position)

    def get_length(self):
        #get the total length of the song in string format
        minutes = self.song_length // 60
        seconds = self.song_length % 60
        return f"{minutes}:{seconds:02}"
    
    def get_length_in_sec(self):
        #get the length of the song in seconds
        return self.song_length

    def set_song_length(self):
        #set the total length of the song in seconds 
        sound = pygame.mixer.Sound(self.current_song)
        self.song_length = int(sound.get_length())

    def change_volume(self, value):
        pygame.mixer.music.set_volume(value)

    def create_shuffled_list(self):
        #create a shuffled list of the song list and start the index at 0
        self.shuffled_list = random.sample(self.song_list, len(self.song_list))
        self.index = 0