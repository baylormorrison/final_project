import pygame

from pygame import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super(Player, self).__init__()

        # Render variables
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.file = pygame.image.load("classes/images/riding.png").convert_alpha()
        self.file.set_colorkey((255, 255, 255), RLEACCEL)
        self.size = self.file.get_size()
        self.surf = pygame.transform.scale(self.file, (int(self.size[0] / 4), int(self.size[1] / 4)))
        self.rect = self.surf.get_rect(center=(0, int(self.screenHeight - ((self.surf.get_size()[1] / 2) + 50))))

        # Jumping variables
        self.ground = self.rect.bottom
        self.isJump = False
        self.velocity = 10
        self.mass = 1

        # Speed
        self.speed = 14

    # Move the sprite based on user key presses
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screenWidth:
            self.rect.right = self.screenWidth

    def toggleJumpSprite(self):
        if self.isJump:
            self.surf = pygame.transform.scale(pygame.image.load("classes/images/jumping.png").convert_alpha(), (int(self.size[0] / 4), int(self.size[1] / 4)))
        else:
            self.surf = pygame.transform.scale(pygame.image.load("classes/images/riding.png").convert_alpha(),
                                               (int(self.size[0] / 4), int(self.size[1] / 4)))

    def jump(self):
        force = .5 * self.mass * (self.velocity ** 2)
        # self.rect.bottom -= force
        self.velocity = self.velocity - 1
        if self.velocity >= 0:
            self.rect.bottom -= force
        else:
            self.rect.bottom += force
        if self.velocity <= -11:
            self.isJump = False
            self.toggleJumpSprite()
            self.rect.bottom = self.ground
            self.mass = 1
            self.velocity = 10
