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
        self.played_queue = []
        self.counter = True


    def load_song(self, song_paths):
        #if no songs are found print error
        if not song_paths:
            print("Error: No songs found")
            return
        #song list = the paths that got passed in the load
        self.song_list = song_paths
        #select a random index of the song list to pick a song
        index = random.randint(0, len(self.song_list) - 1)
        self.current_song = self.song_list[index]
        self.played_queue.append(self.current_song)
        print(self.played_queue)
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
        #pick a random index from the song list
        next_index = random.randint(0, len(self.song_list) - 1)
        print("we are here")
        while(True):
            #if no songs are in played queue or the song that is picked is not in the queue play the new random song
            if self.played_queue:
                print("List is not empty")
            if  self.song_list[next_index] in self.played_queue:
                print("Song we picked is not in the queue")
            
            if not self.played_queue or not self.song_list[next_index] in self.played_queue:
                self.current_song = self.song_list[next_index]
                self.is_playing = False
                self.played_queue.append(self.song_list[next_index])
                print(self.played_queue)
                self.play_song()
                break
            #if the song that was picked is in the queue pick a new one
            else:
                next_index = random.randint(0, len(self.song_list) - 1)
    
    def previous_song(self):
        #if the played queue is empty pick a random song
        if not self.played_queue and self.counter:
            prev_index = random.randint(0, len(self.song_list) - 1)
            self.current_song = self.song_list[prev_index]
            self.is_playing = False
            self.play_song()
            self.counter = False
        #if the played queue is empty and it's not the first time
        elif not self.played_queue:
            prev_index = random.randint(0, len(self.song_list) - 1)
            self.current_song = self.song_list[prev_index]
            self.is_playing = False
            self.play_song()
        #if the played queue has songs
        else:
            self.played_queue.pop()
            self.current_song = self.played_queue.pop()
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