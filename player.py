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
        if not song_paths:
            print("Error: No songs found")
            return
        self.song_list = song_paths
        index = random.randint(0, len(self.song_list) - 1)
        self.current_song = song_paths[index]
        self.set_song_length()
        for i in range(len(self.song_list) - 1):
            self.shuffle_list.append(0)
        self.shuffle_list[index] = 1
    
    def get_metadata(self):
        if self.current_song is not None:
            audio_file = eyed3.load(self.current_song)
            metadata = {}
            metadata.update([("Title", audio_file.tag.title), ("Artist", audio_file.tag.artist), ("Album", audio_file.tag.album)])
            if audio_file.tag.images:
                image = audio_file.tag.images[0]
                with open("album_cover.jpg", "wb") as img_file:
                    img_file.write(image.image_data)
                    metadata.update({"Album_cover": image})
            return metadata

    def play_song(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.set_song_length()
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    
    def pause_song(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
    
    def next_song(self):
        next_index = random.randint(0, len(self.song_list) - 1)
        while(True):
            if self.shuffle_list[next_index] == 0:
                self.current_song = self.song_list[next_index]
                self.is_playing = False
                self.shuffle_list[next_index] = max(self.shuffle_list) + 1
                #print(f"Song that is playing {next_index}")
                self.play_song()
                break
            else:
                counter = 0
                for i in range(len(self.song_list) - 1):
                    if(self.shuffle_list != 0):
                        counter += 1
                    else: 
                        break
                if(counter == len(self.shuffle_list) - 1):
                    for i in range(len(self.song_list) - 1):
                        self.shuffle_list[i] = 0
                next_index = random.randint(0, len(self.song_list) - 1)
    
    def previous_song(self):
        if(max(self.shuffle_list) == 0):
            prev_index = random.randint(0, len(self.shuffle_list) - 1)
            self.current_song = self.song_list[prev_index]
            self.is_playing = False
            self.last_played_index = prev_index
            #print(f"All zero and prev index {prev_index}")
            self.play_song()
        elif(self.first_go and max(self.shuffle_list) == 1):
            prev_index = random.randint(0, len(self.shuffle_list) - 1)
            self.shuffle_list[self.shuffle_list.index(max(self.shuffle_list))] = 0
            self.first_go = False
            self.current_song = self.song_list[prev_index]
            self.is_playing = False
            #print(f"First time loading so max is 1 {prev_index}")
            self.last_played_index = prev_index
            self.play_song()
        else:
            if(max(self.shuffle_list) == 1):
                #print("Max is one")
                self.shuffle_list[self.shuffle_list.index(max(self.shuffle_list))] = 0
                #print("Max is zero again")
                #print(self.last_played_index)
                if(self.last_played_index is not None):
                    prev_index = self.last_played_index
                    self.current_song = self.song_list[prev_index]
                    self.is_playing = False
                    self.play_song()
                else:
                    print("Problem last played index is None")
            else:
                self.shuffle_list[self.shuffle_list.index(max(self.shuffle_list))] = 0
                prev_index = self.shuffle_list.index(max(self.shuffle_list))
                self.current_song = self.song_list[prev_index]
                self.is_playing = False
                #print(f"Not first time and max not zero or 1 and prev index {prev_index}")
                self.play_song()
    

    def get_song_position(self):
        milliseconds = pygame.mixer.music.get_pos()
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02}"
    
    def get_song_position_sec(self):
        milliseconds = pygame.mixer.music.get_pos()
        return milliseconds // 1000

    def set_position(self, position):
        pygame.mixer.music.play(start = position)

    def get_length(self):
        minutes = self.song_length // 60
        seconds = self.song_length % 60
        return f"{minutes}:{seconds:02}"
    
    def get_length_in_sec(self):
        return self.song_length

    def set_song_length(self):
        sound = pygame.mixer.Sound(self.current_song)
        self.song_length = int(sound.get_length())