import pygame
import level_one
import level_two
levelOneFinish = False

running = True
while running:
    if level_one.main():
        print("You did it")
        level_two.main()
    running = False

