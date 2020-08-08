import pygame
import os
import Maze
pygame.init()
filename = os.getcwd()
print(filename)
# create screen
HEIGHT = 750
WEIGHT = 1300
screen = pygame.display.set_mode((WEIGHT, HEIGHT))

#title and icon
pygame.display.set_caption("Pac-man")
# background
background = pygame.image.load(filename + "/PICTURE/background1.jpg")
# player
running = True
level_running = False
main = Maze.Maze(screen)
while running:
    level = 0
    maze_map = 0
    while not(level_running):  # check enter level and maze
        level = int(input("Enter level (1-4): "))
        maze_map = int(input("Enter map (1-5): "))
        if level > 0 and level < 5 and maze_map > 0 and maze_map < 6:
            level_running = True
            main.add_level(level, maze_map)
            main.read_data("map" + str(maze_map) + ".txt")
    main.draw_map()
    if level == 1:
        pass
    if level == 2:
        pass
    if level == 3:
        pass
    if level == 4:
        # main.run_level4()
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
