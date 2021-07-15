import pygame

def Level1Music():
    pygame.mixer.music.load('night.wav')
    pygame.mixer.music.play(-1)

def JumpSound():
    pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/alright.wav"))

def EndSound1():
    pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/accomplish.wav"))

def EndSound2():
    pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/python.wav"))
