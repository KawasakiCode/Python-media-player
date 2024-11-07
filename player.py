import pygame
import time

pygame.mixer.init()

class MusicPlayer:
    def __init__(self):
        self.is_playing = False
        self.current_song = None
        self.song_list = []
        self.current_position = 0
        self.is_paused = False
    
    def load_song(self, song_paths):
        self.song_list = song_paths
        self.current_song = song_paths[0]
    
    def play_song(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
        else: 
            pygame.mixer.music.unpause()
    
    def pause_song(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True
    
    def next_song(self):
        current_index = self.song_list.index(self.current_song)
        next_index = (current_index + 1) % len(self.song_list)
        self.current_song = self.song_list[next_index]
        self.play_song()
    
    def previous_song(self):
        current_index = self.song_list.index(self.current_song)
        prev_index = (current_index - 1) % len(self.song_list)
        self.current_song = self.song_list[prev_index]
        self.play_song()

    def get_current_position(self):
        return pygame.mixer.music.get_pos() / 1000 + self.current_position
    
    def set_position(self, position):
        pygame.mixer.music.play(start = position)