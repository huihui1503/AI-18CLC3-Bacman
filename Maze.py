import os
import pygame
import numpy
import time

filename = os.getcwd()
wall = pygame.image.load(filename + "/PICTURE/wall.png")
image_food = pygame.image.load(filename + "/PICTURE/venus.png")
image_monster = pygame.image.load(filename + "/PICTURE/monsters.png")
image_pacman = pygame.image.load(filename + "/PICTURE/ufo.png")
image_background = pygame.image.load(filename + "/PICTURE/background1.jpg")
HEIGHT = 750
WEIGHT = 1300


class Maze():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WEIGHT, HEIGHT))

        #title and icon
        pygame.display.set_caption("Pac-man")
        self.map = []  # wall == 1 , food == 2 , monster == 3 , bac-man == 4
        self.pacman = ()
        self.monster = []  # list of monster
        self.food = []  # list [[y,x],[y,x]]
        self.row = 0  # size of row
        self.col = 0  # size of collum
        self.frontier = []
        self.expanded = []
        self.point = 0
        self.time = 0
        self.level = 0  # level of game
        self.maze_map = 0  # level of map

    def test(self):
        i = 1
        while True:
            self.map[0][i - 1] = 0
            self.map[0][i] = 4
            self.draw_map()
            if i < 12:
                i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

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
        self.screen.fill(0)
        self.screen.blit(image_background, (0, 0))
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
                elif self.map[i][j] == 2:
                    self.screen.blit(image_food, (x, y))
                elif self.map[i][j] == 3:
                    self.screen.blit(image_monster, (x, y))
                elif self.map[i][j] == 4:
                    self.screen.blit(image_pacman, (x, y))
                x += 30
            y += 30

    def run_level4(self):
        #cost_path = [[100 for _ in range(self.row)]for _ in range(self.collum)]
        check_stop = True
        x = (WEIGHT - (self.col + 2) * 30) / 2 + 30
        y = (HEIGHT - (self.row + 2) * 30) / 2 + 30
        turn = True
        while check_stop:
            if turn:
                food, monster = self.detect_food_monster()
                position = []
                self.MAX_VALUE(self.pacman, food, monster,
                               0, position, -999999)
                self.map[self.pacman[0]][self.pacman[1]] = 0
                self.pacman = position
                self.map[self.pacman[0]][self.pacman[1]] = 4
                for i, a in enumerate(self.food):
                    if a[0] == self.pacman[0] and a[1] == self.pacman[1]:
                        self.food.pop(i)
                        break
                turn = False
            else:
                action = self.MONSTER_ACTION(self.pacman, self.monster)
                for i in self.monster:
                    self.map[i[0]][i[1]] = 0
                for i in self.food:
                    self.map[i[0]][i[1]] = 2
                self.monster = action
                for i in self.monster:
                    self.map[i[0]][i[1]] = 3
                turn = True
            self.draw_map()
            if self.check_stop():
                check_stop = False
            pygame.display.update()

    def movement(self):
        x = (WEIGHT - (self.col + 2) * 30) / 2 + 30
        y = (HEIGHT - (self.row + 2) * 30) / 2 + 30
        for i in self.food:
            self.screen.blit(image_food, (x + 30 * b[1], y + 30 * b[0]))
        for i in self.monster:
            self.screen.blit(image_monster, (x + 30 * b[1], y + 30 * b[0]))
        self.screen.blit(
            image_pacman, (x + 30 * self.pacman[1], y + 30 * self.pacman[0]))

    def check_stop(self):
        # check when all of food is eaten or monster collides with pacman
        # when monster collides with pacman, the position of bacman should be changed into (-1,-1)
        if len(self.food) == 0 or (self.pacman[0] == -1 and self.pacman[1] == -1):
            return True
        return False
 # min max algorithm

    def detect_food_monster(self):
        food = []
        monster = []
        for i in self.monster:
            if abs(i[0] - self.pacman[0]) + abs(i[1] - self.pacman[1]) <= 3:
                monster.append(i)
        for i in self.food:
            if abs(i[0] - self.pacman[0]) + abs(i[1] - self.pacman[1]) <= 3:
                food.append(i)
        return food, monster

    def MAX_VALUE(self, state, food, monster, step, position, a):
        check = self.TERMINAL_TEST(state, food, monster)
        if check:
            if check == 1:
                return self.point - step + 20
            if check == -1:
                return self.point - step - 2**(20 - step)
        v = -999999
        temp_act = self.ACTION(state, 4)
        for i in temp_act:
            temp_value = self.map[i[0]][i[1]]
            self.map[i[0]][i[1]] = 4
            temp = self.MIN_VALUE(i, food, monster, step + 1, position, a)
            self.map[i[0]][i[1]] = temp_value
            if temp > v:
                v = temp
                position = i
            a = max(a, v)
        return v

    def MIN_VALUE(self, state, food, monster, step, position, a):
        check = self.TERMINAL_TEST(state, food, monster)
        if check:
            if check == 1:
                temp_monster = self.monster.copy()
                self.monster = self.MONSTER_ACTION(state)
                check = self.TERMINAL_TEST(state)
                self.monster = temp_monster
                if check == -1:
                    return self.point - step + 20 - 2**(20 - step)
                else:
                    return self.point - step + 20
            if check == -1:
                return self.point - step - 2**(20 - step)
        if (self.point - step) < a:
            return self.point - step
        if step == 3:
            return self.point - step
        temp_monster = monster.copy()
        self.monster = self.MONSTER_ACTION(state, monster)
        v = self.MAX_VALUE(state, food, monster, step, position, a)
        monster = temp_monster
        return v

    def ACTION(self, state, value):
        # value to differentiate whether monster or pacman
        temp_act = []
        if state[0] - 1 > 0 and self.map[state[0] - 1][state[1]] != 1 and self.map[state[0] - 1][state[1]] != value:
            temp_act.append([state[0] - 1, state[1]])
        if state[0] + 1 < self.row and self.map[state[0] + 1][state[1]] != 1 and self.map[state[0] + 1][state[1]] != value:
            temp_act.append([state[0] + 1, state[1]])
        if state[1] - 1 > 0 and self.map[state[0]][state[1] - 1] != 1 and self.map[state[0]][state[1] - 1] != value:
            temp_act.append([state[0], state[1] - 1])
        if state[1] + 1 < self.col and self.map[state[0]][state[1] + 1] != 1 and self.map[state[0]][state[1] + 1] != value:
            temp_act.append([state[0], state[1] + 1])
        return temp_act

    def TERMINAL_TEST(self, state, food, monster):
        for i in food:
            if i[0] == state[0] and i[1] == state[1]:
                return 1
        for i in monster:
            if i[0] == state[0] and i[1] == state[1]:
                return -1
        return 0

    def MONSTER_ACTION(self, state, monster):
        action = []
        for i in monster:
            action.append(self.BFS(i, state))
        return action

    def BFS(self, monster, goal):
        return_value = []
        check_stop = True
        frontier_parent = []
        expanded_parent = []
        self.frontier.append(monster)
        frontier_parent.append(-1)
        while check_stop:
            self.expanded.append(self.frontier[0])
            self.frontier = self.frontier[1:]
            expanded_parent.append(frontier_parent[0])
            frontier_parent = frontier_parent[1:]
            adjacency_node = self.ACTION(
                self.expanded[len(self.expanded) - 1], 1)
            for i in adjacency_node:
                if not i in self.expanded:
                    if i[0] == goal[0] and i[1] == goal[1]:
                        parent_pos = len(self.expanded) - 1
                        while parent_pos != -1:
                            return_value.append(self.expanded[parent_pos])
                            parent_pos = expanded_parent[parent_pos]
                        check_stop = False
                    else:
                        if not i in self.frontier:
                            frontier_parent.append(len(self.expanded) - 1)
                            self.frontier.append(i)
        self.expanded.clear()
        self.frontier.clear()
        return return_value[1]
