import pygame
import math
import random
from helper_methods import imageStack
from helper_methods import scaleSurf

from pygame import (
    RLEACCEL,
)


class Cloud(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screenWidth + 10, screenWidth + 20),
                random.randint(0, math.floor(screenHeight / 3)),
            )
        )

    def update(self):
        self.rect.move_ip(-2, 0)
        if self.rect.right < 0:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, file, alpha):
        super(Background, self).__init__()
        self.surf = pygame.image.load(file).convert()
        self.screenWidth = screenWidth
        if alpha:
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        else:
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(left=0, bottom=(screenHeight - 125))

    def update(self):
        self.rect.move_ip(-3, 0)
        if self.rect.left == -(900 + self.screenWidth):
            self.rect.left = 0


class Road(pygame.sprite.Sprite):
    def __init__(self):
        super(Road, self).__init__()
        self.surf = pygame.image.load("images/road.jpg").convert()
        self.size = self.surf.get_size()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.bigger = pygame.transform.scale(self.surf, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.rect = self.bigger.get_rect(center=(2136, 657))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.left <= -712:
            self.rect.left = 0


class WinText(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super(WinText, self).__init__()
        self.surf = pygame.image.load("images/you win.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                screenWidth / 2,
                screenHeight / 4,
            )
        )


class GameOver(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super(GameOver, self).__init__()
        self.surf = pygame.image.load("images/game over.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                screenWidth / 2,
                screenHeight / 4,
            )
        )


class Halo(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Halo, self).__init__()
        self.images = imageStack("images/power_up/power up_", 6, 8)
        self.current_image = 0
        self.surf = self.images[self.current_image]
        self.rect = self.surf.get_rect(center=player.rect.center)

    def update(self, player):
        # Animation
        self.current_image += 1
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.surf = self.images[self.current_image]

        self.rect.center = player.rect.center
