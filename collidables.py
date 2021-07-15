import pygame
import random
from helper_methods import scaleSurf, imageStack


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player, screenWidth):
        super(Obstacle, self).__init__()
        self.surf = scaleSurf("images/barrel.png", 8)
        self.rect = self.surf.get_rect(centerx=screenWidth, bottom=(player.ground))

    def update(self):
        self.rect.move_ip(-4, 0)
        if self.rect.right < 0:
            self.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super(Bird, self).__init__()
        self.images = imageStack("images/bird/bird_", 7, 8)
        self.current_image = 0
        self.surf = self.images[self.current_image]
        self.rect = self.surf.get_rect(center=(screenWidth, screenHeight / 8))

        # Bounds
        self.lower = screenHeight * (6 / 8)
        self.upper = screenHeight / 8
        self.speed = 8

    def update(self):
        # Animation
        self.current_image += 1
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.surf = self.images[self.current_image]

        # Movement
        self.rect.move_ip(-6, self.speed)
        if self.rect.centery >= self.lower or self.rect.centery <= self.upper:
            self.speed *= -1
        if self.rect.right < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super(PowerUp, self).__init__()
        self.images = imageStack("images/power_up/power up_", 8, 8)
        self.current_image = 0
        self.surf = self.images[self.current_image]
        self.rect = self.surf.get_rect(center=(random.randint(0, screenWidth), 0))

        # Bounds
        self.floor = screenHeight - 10

    def update(self):
        # Animation
        self.current_image += 1
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.surf = self.images[self.current_image]

        # Movement
        self.rect.move_ip(0, 2)
        if self.rect.bottom >= self.floor:
            self.kill()


class Finish(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super(Finish, self).__init__()
        self.surf = scaleSurf("images/finish.png", 3)
        self.rect = self.surf.get_rect(left=screenWidth, bottom=screenHeight - 10)

    def update(self):
        self.rect.move_ip(-4, 0)
        if self.rect.right < 0:
            self.kill()