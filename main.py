import pygame
import os
import Maze
pygame.init()
filename = os.getcwd()

# player
running = True
level_running = False
while running:
    level = 0
    maze_map = 0
    main = Maze.Maze()
    while not(level_running):  # check enter level and maze
        level = int(input("Enter level (1-4): "))
        maze_map = int(input("Enter map (1-5): "))
        if level > 0 and level < 5 and maze_map > 0 and maze_map < 6:
            level_running = True
            main.add_level(level, maze_map)
            main.read_data("map" + str(maze_map) + ".txt")
        # Enter -1 to get out of loop
        if level == -1 or maze_map == -1:
            level_running = True
            running = False
    if level == 1:
        main.run_level1()
        level_running = False
    if level == 2:
        main.run_level2()
        level_running = False
    if level == 3:
        main.run_level3()
        level_running = False
    if level == 4:
        main.run_level4()
        level_running = False
