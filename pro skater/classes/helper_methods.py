import pygame

from pygame import (
    RLEACCEL,
)


def scaleSurf(file, divisor=1):
    img = pygame.image.load("classes/images/riding.png").convert_alpha()
    img.set_colorkey((255, 255, 255), RLEACCEL)
    size = img.get_size()
    return pygame.transform.scale(pygame.image.load(file).convert_alpha(), (int(size[0] / divisor), int(size[1] / divisor)))


def imageStack(fileStyle, length, divisor=1):
    stack = []
    for i in range(1, length + 1):
        file = f"{fileStyle}{i}.png"
        stack.append(scaleSurf(f"{fileStyle}{i}.png", divisor))
    return stack
