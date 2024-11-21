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
        self.shuffle_list = []
        self.current_position = 0
        self.is_paused = True
        self.song_length = 0
        self.first_go = True
        self.last_played_index = None

    def load_song(self, song_paths):
        #if no songs are found print error
        if not song_paths:
            print("Error: No songs found")
            return
        #song list = the paths that got passed in the load
        self.song_list = song_paths
        #select a random index of the song list to pick a song
        index = random.randint(0, len(self.song_list) - 1)
        self.current_song = song_paths[index]
        #get song length for time labels in ui.py
        self.set_song_length()
        #fill the shuffle_list with as many 0 as the songs_list to handle the shuffle
        for i in range(len(self.song_list)):
            self.shuffle_list.append(0)
        self.shuffle_list[index] = 1
    
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
        #pick a random index for the shuffle list
        next_index = random.randint(0, len(self.song_list) - 1)
        while(True):
            #if the shuffle_list[index] is 0 load the song and play it
            if self.shuffle_list[next_index] == 0:
                self.current_song = self.song_list[next_index]
                self.is_playing = False
                self.shuffle_list[next_index] = max(self.shuffle_list) + 1
                self.play_song()
                break
            else:
                #if it is not 0 then check if all shuffle list nodes are not zero meaning that all songs have been played
                if all(node != 0 for node in self.shuffle_list):
                    #if all songs have been played make shuffle list nodes all 0 again
                    for i in range(len(self.shuffle_list)):
                        self.shuffle_list[i] = 0
                #if the first random index was a song that has been played pick another one
                next_index = random.randint(0, len(self.song_list) - 1)
    
    def previous_song(self):
        #if the max value of the shufflelist is 0 then no other song has been played 
        if(max(self.shuffle_list) == 0):
            #pick a random previous song if the button is pressed with no other song played before
            prev_index = random.randint(0, len(self.shuffle_list) - 1)
            self.current_song = self.song_list[prev_index]
            self.is_playing = False
            self.last_played_index = prev_index
            self.play_song()
        #if the max is 1 and it is the first time the previous button if pressed then the loaded song will have a value of 1
        #but you still need to pick a random song because nothing has played
        elif(self.first_go and max(self.shuffle_list) == 1):
            #pick a random index
            prev_index = random.randint(0, len(self.shuffle_list) - 1)
            #make the song that had 1 as value in the shufflelist to a 0
            self.shuffle_list[self.shuffle_list.index(max(self.shuffle_list))] = 0
            #tell the function that the first time has passed and the same senario cannot happen again since it could only occur
            #when the class first loads
            self.first_go = False
            self.current_song = self.song_list[prev_index]
            self.is_playing = False
            #keep the last song that was playing in case you need it later
            self.last_played_index = prev_index
            self.play_song()
        #if the max is not zero and it is not the first time
        else:
            #if max is 1
            if(max(self.shuffle_list) == 1):
                #set the max to 0
                self.shuffle_list[self.shuffle_list.index(max(self.shuffle_list))] = 0
                #if the last index has a value then play that song else print error
                #this only happens when all shuffle list nodes are 0 and then press next which makes a node 1
                #If you press previous again it shouldnt play a random song but the previous which is held in the last played
                if(self.last_played_index is not None):
                    prev_index = self.last_played_index
                    self.current_song = self.song_list[prev_index]
                    self.is_playing = False
                    self.play_song()
                else:
                    print("Problem last played index is None")
            #if the max is more than 1 then there is a queue of at least 2 songs
            else:
                #zero the current max which is the song that plays and play the new max
                self.shuffle_list[self.shuffle_list.index(max(self.shuffle_list))] = 0
                prev_index = self.shuffle_list.index(max(self.shuffle_list))
                self.current_song = self.song_list[prev_index]
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