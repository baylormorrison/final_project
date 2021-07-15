from scene_manager.classes import level_two, level_one

levelOneFinish = False

running = True
while running:
    if level_one.main():
        print("You did it")
        level_two.main()
    running = False

