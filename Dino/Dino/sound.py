import os

import pygame


def load_sound(sound_name: str):
    path = os.path.join(os.path.dirname(__file__), "audio", sound_name)
    sound = pygame.mixer.Sound(path)
    return sound
