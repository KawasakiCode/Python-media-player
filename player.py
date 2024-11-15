import pygame

pygame.mixer.init()

class MusicPlayer:
    def __init__(self):
        self.is_playing = False
        self.current_song = None
        self.song_list = []
        self.current_position = 0
        self.is_paused = True
        self.song_length = 0
    
    def load_song(self, song_paths):
        if not song_paths:
            print("Error: No songs found")
            return
        self.song_list = song_paths
        self.current_song = song_paths[0]
        self.set_song_length()
    
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
        current_index = self.song_list.index(self.current_song)
        next_index = (current_index + 1) % len(self.song_list)
        self.current_song = self.song_list[next_index]
        self.is_playing = False
        self.play_song()
    
    def previous_song(self):
        current_index = self.song_list.index(self.current_song)
        if(current_index == 0):
            prev_index = len(self.song_list) - 1
        else:
            prev_index = (current_index - 1) % len(self.song_list)
        self.current_song = self.song_list[prev_index]
        self.is_playing = False
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