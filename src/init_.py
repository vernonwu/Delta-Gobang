'''加载背景、图片、音效
'''
import pygame
import os
pygame.init()
# define absolute path
def resource_path(relative): 
    absolute_path = os.path.join(relative)
    return absolute_path
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
background = (201, 202, 187)
checkerboard = (80, 80, 80)
button = (52, 53, 44)
background_jpg = pygame.image.load(resource_path('image\\Background.jpg'))
black_chessman = pygame.image.load(resource_path('image\\Black_chess.png'))
white_chessman = pygame.image.load(resource_path('image\\White_chess.png'))
# 音乐
play_chess_sound = pygame.mixer.Sound(resource_path("music\\play_chess.wav"))
play_chess_sound.set_volume(0.2)
button_sound = pygame.mixer.Sound(resource_path("music\\button.wav"))
button_sound.set_volume(0.2)
victor_sound = pygame.mixer.Sound(resource_path("music\\victory.wav"))
victor_sound.set_volume(1)
background_music = pygame.mixer.Sound(resource_path("music\\Bgm.wav"))
background_music.set_volume(0.3)

# 定义极限
pinf = float('inf')
ninf = float('-inf')