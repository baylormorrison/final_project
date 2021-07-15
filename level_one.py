import random
import pygame
from player import Player
from sounds import EndSound1, JumpSound, Level1Music
import scenery
import collidables

from pygame import (
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT
)


def main():
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700

    gameLost = False
    gameWon = False
    powerSchaffer = False
    soundCounter = 0

    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Charles Shaffer's Pro Skater")
    screen.fill((135, 206, 250))
    clock = pygame.time.Clock()

    # Custom events
    ADD_CLOUD = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_CLOUD, 4500)
    add_obstacle = pygame.USEREVENT + 2
    add_bird = pygame.USEREVENT + 3
    pygame.time.set_timer(add_bird, 4000, True)
    add_power = pygame.USEREVENT + 4
    pygame.time.set_timer(add_power, 12000)
    lose_power = pygame.USEREVENT + 5
    won_game = pygame.USEREVENT + 6

    # Initialize background, road, and player
    background = scenery.Background(SCREEN_WIDTH, SCREEN_HEIGHT, "images/two_neighborhood_tiles.jpg", False)
    road = scenery.Road()
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    barrel = collidables.Obstacle(player, SCREEN_WIDTH)

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    collision_order = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    barrels = pygame.sprite.Group()
    birds = pygame.sprite.Group()
    end_level = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    halos = pygame.sprite.Group()

    # Add background, road and player to environment group
    collision_order.add(background, road, player, barrel)
    barrels.add(barrel)

    # Obstacle spawn control
    # test spawns
    # spawns = [400, 400, 400]
    spawns = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 600]
    i = 0
    last_barrel = barrel

    # Start Soundtrack
    # Level1Music()

    running = True
    while running:
        for event in pygame.event.get():
            # Quit Conditions
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                # Set player state to jumping
                if event.key == K_SPACE:
                    if player.isJump == False:
                        player.isJump = True
                        player.toggleJumpSprite()
                        if gameWon:
                            running = False
            # Cloud generated
            elif event.type == ADD_CLOUD:
                new_cloud = scenery.Cloud(SCREEN_WIDTH, SCREEN_HEIGHT)
                clouds.add(new_cloud)
            # Bird generator
            elif event.type == add_bird:
                new_bird = collidables.Bird(SCREEN_WIDTH, SCREEN_HEIGHT)
                collision_order.add(new_bird)
                birds.add(new_bird)
                pygame.time.set_timer(add_bird, random.randint(0, 8000), True)
            # End level barrel stack
            elif event.type == add_obstacle:
                new_obstacle = collidables.Obstacle(player, SCREEN_WIDTH)
                end_level.add(new_obstacle)
                collision_order.add(new_obstacle)
            elif event.type == add_power:
                new_power = collidables.PowerUp(SCREEN_WIDTH, SCREEN_HEIGHT)
                collision_order.add(new_power)
                power_ups.add(new_power)
            elif event.type == lose_power:
                for halo in halos:
                    halo.kill()
                screen.fill((135, 206, 250))
                powerSchaffer = False
            elif event.type == won_game:
                EndSound1()

        if i < len(spawns) and last_barrel.rect.centerx <= spawns[i]:
            new_obstacle = collidables.Obstacle(player, SCREEN_WIDTH)
            barrels.add(new_obstacle)
            collision_order.add(new_obstacle)
            last_barrel = new_obstacle
            i += 1
        elif i == len(spawns):
            finishLine = collidables.Finish(SCREEN_WIDTH, SCREEN_HEIGHT)
            collision_order.add(finishLine)
            end_level.add(finishLine)

            i += 1

        # Determine player jump
        if player.isJump == True:
            player.jump()

        # Control halo
        if powerSchaffer:
            for halo in halos:
                halo.update(player)

        # Lose condition
        if pygame.sprite.spritecollideany(player, barrels) or pygame.sprite.spritecollideany(player, birds):
            if not powerSchaffer:
                gameLost = True
            elif powerSchaffer:
                if pygame.sprite.spritecollideany(player, birds):
                    pygame.sprite.spritecollideany(player, birds).kill()
        # Win condition
        if pygame.sprite.spritecollideany(player, end_level):
            gameWon = True
            soundCounter += 1

        if soundCounter == 1:
            pygame.time.set_timer(won_game, 1, True)

        if pygame.sprite.spritecollideany(player, power_ups):
            pygame.sprite.spritecollideany(player, power_ups).kill()
            powerSchaffer = True
            halo = scenery.Halo(player)
            halos.add(halo)
            collision_order.add(halo)
            pygame.time.set_timer(lose_power, 10000)
            JumpSound()

        # Move clouds, background, and road
        if (gameWon == False and gameLost == False):
            clouds.update()
            background.update()
            road.update()
            barrels.update()
            end_level.update()
            birds.update()
            power_ups.update()
        elif gameWon:
            win = scenery.WinText(SCREEN_WIDTH, SCREEN_HEIGHT)
            all_sprites.add(win)
        elif gameLost:
            gameOver = scenery.GameOver(SCREEN_WIDTH, SCREEN_HEIGHT)
            all_sprites.add(gameOver)

        # Get and process key presses
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        screen.fill((135, 206, 250))

        all_sprites.add(clouds)
        all_sprites.add(collision_order)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        pygame.display.flip()

        clock.tick(30)

    if gameWon:
        return True
    else:
        return False
