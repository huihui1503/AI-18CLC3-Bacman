import os
import pygame
import numpy
filename = os.getcwd()
wall = pygame.image.load(filename + "/PICTURE/wall.png")
HEIGHT = 750
WEIGHT = 1300


class Maze():
    def __init__(self, screen):
        self.screen = screen
        self.map = []  # wall == 1 , food == 2 , monster == 3 , bac-man == 4
        self.pacman = ()
        self.monster = []  # list of monster
        self.food = []  #  list [[y,x],[y,x]]
        self.row = 0  # size of row
        self.col = 0  # size of collum
        self.frontier = []
        self.expanded = []
        self.point = 0
        self.time = 0
        self.level = 0  # level of game
        self.maze_map = 0  # level of map
    def add_level(self, level, maze_map):
        self.maze_map = maze_map
        self.level = level

    def read_data(self, path_file):
        file = open(filename + "/MAP/" + path_file, "r")
        line = file.readline().split(" ")
        self.row = int(line[0])
        self.col = int(line[1])
        for i in range(self.row):
            line = file.readline().split(" ")
            temp = [int(k) for k in line]
            self.map.append(temp)
        line = file.readline().split(" ")
        self.map[int(line[0])][int(line[1])] = 4
        self.pacman = [int(line[0]), int(line[1])]
        file.close()
        if self.level == 1:
            self.random_object(1, 0)
        elif self.level == 2:
            if self.maze_map == 1:
                self.random_object(1, 1)
            elif self.maze_map == 2:
                self.random_object(1, 2)
            elif self.maze_map == 3:
                self.random_object(1, 3)
            elif self.maze_map == 4:
                self.random_object(1, 4)
            elif self.maze_map == 5:
                self.random_object(1, 4)
        elif self.level == 3:
            if self.maze_map == 1:
                self.random_object(3, 1)
            elif self.maze_map == 2:
                self.random_object(4, 2)
            elif self.maze_map == 3:
                self.random_object(5, 3)
            elif self.maze_map == 4:
                self.random_object(6, 4)
            elif self.maze_map == 5:
                self.random_object(7, 4)
        elif self.level == 4:
            if self.maze_map == 1:
                self.random_object(3, 1)
            elif self.maze_map == 2:
                self.random_object(4, 2)
            elif self.maze_map == 3:
                self.random_object(5, 3)
            elif self.maze_map == 4:
                self.random_object(6, 4)
            elif self.maze_map == 5:
                self.random_object(7, 4)

    def random_object(self, food, monster):
        while food > 0:
            x = numpy.random.randint(self.col)
            y = numpy.random.randint(self.row)
            check = abs(x - self.pacman[1]) + abs(y - self.pacman[0])
            if self.map[y][x] == 0 and check > 5:
                self.map[y][x] = 2
                self.food.append([y, x])
                food -= 1
        while monster > 0:
            x = numpy.random.randint(self.col)
            y = numpy.random.randint(self.row)
            check = abs(x - self.pacman[1]) + abs(y - self.pacman[0])
            if self.map[y][x] == 0 and check > 5:
                self.map[y][x] = 3
                self.monster.append([y, x])
                monster -= 1

    def draw_map(self):
        x = (WEIGHT - (self.col + 2) * 30) / 2
        y = (HEIGHT - (self.row + 2) * 30) / 2
        for i in range(self.col + 2):
            self.screen.blit(wall, (x + i * 30, y))
        for i in range(self.col + 2):
            self.screen.blit(wall, (x + i * 30, y + (self.row + 1) * 30))
        for i in range(self.row):
            self.screen.blit(wall, (x, y + 30 + i * 30))
        for i in range(self.row):
            self.screen.blit(wall, (x + (self.col + 1) * 30, y + 30 + i * 30))
        y += 30
        for i in range(self.row):
            x = (WEIGHT - (self.col + 2) * 30) / 2 + 30
            for j in range(self.col):
                if self.map[i][j] == 1:
                    self.screen.blit(wall, (x, y))
                # elif self.map[i][j] == 2:
                    # self.screen.blit(food, (x, y))
                # elif self.map[i][j] == 3:
                    # self.screen.blit(monster, (x, y))
                # elif self.map[i][j] == 4:
                    # self.screen.blit(pacman, (x, y))
                x += 30
            y += 30

    def run_level4(self):
        cost_path=[[100 for _ in range(self.row)]for _ in range(self.collum)]
        check_stop = True
        pacman, img_food, img_monster = self.create_image_variable()
        x = (WEIGHT - (self.col + 2) * 30) / 2 + 30
        y = (HEIGHT - (self.row + 2) * 30) / 2 + 30
        while check_stop:
            for (a, b) in zip(img_food, self.food):
                self.screen.blit(a, (x + 30 * b[1], y + 30 * b[0]))
            for (a, b) in zip(img_monster, self.monster):
                self.screen.blit(a, (x + 30 * b[1], y + 30 * b[0]))
            self.screen.blit(
                pacman, (x + 30 * self.pacman[1], y + 30 * self.pacman[0]))
            if self.check_stop():
                check_stop = False
            pygame.display.update()

    def check_stop(self):
        # check when all of food is eaten or monster collides with pacman
        # when monster collides with pacman, the position of bacman should be changed into (-1,-1)
        if len(self.food) == 0 or (self.pacman[0] == -1 and self.pacman[1] == -1):
            return True
        return False

    def create_image_variable(self):
        # create variable contain image of object
        pacman = pygame.image.load(filename + "/PICTURE/ufo.png")
        img_monster = [pygame.image.load(filename + "/PICTURE/monsters.png") if i % 2 == 0 else pygame.image.load(
            filename + "/PICTURE/monsters.png") for i in range(len(self.monster))]
        img_food = []
        for i in range(len(self.food):
            if i % 2 == 0:
                img_food.append(pygame.image.load(
                    filename + "/PICTURE/venus.png"))
            elif i % 3 == 0:
                img_food.append(pygame.image.load(
                    filename + "/PICTURE/global.png"))
            else:
                img_food.append(pygame.image.load(
                    filename + "/PICTURE/planet.png"))
        return pacman, img_food, img_monster


    #find food and mosnter in the sight
    def
