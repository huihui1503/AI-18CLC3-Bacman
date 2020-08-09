import os
import pygame
import numpy
import time

clock = pygame.time.Clock()
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
        self.action_level2 = {}
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

        # level 2

    def path_return(self, parent, start, goal):
        path = []
        while goal != start:
            path.append(goal)
            goal = parent[goal]

        path.append(start)
        path.reverse()
        return path

    def breadth_first_search(self, graph, start, goal):
        explored = []
        frontier = [start]
        parent = {start: None}
        found = False
        if start == goal:
            return [goal], [goal], True
        while len(frontier) and not found:
            node = frontier.pop(0)
            if node not in explored:
                explored.append(node)
                neighbours = graph[node]
                for neighbour in neighbours:
                    if neighbour not in explored:
                        frontier.append(neighbour)
                        parent[neighbour] = node
                        if neighbour == goal:
                            found = True
                            break
        if found:
            path = self.path_return(parent, start, goal)
            return path, explored + [goal], True
        else:
            return "There is no path between {} and {}".format(start, goal), explored, False

    def check_frontier(self, node, frontier):
        for i in range(0, len(frontier)):
            current = frontier[i]
            if node == current[0]:
                return i, True

        return -1, False

    def check_cost(self, node, frontier, cost):
        for i in range(0, len(frontier)):
            current = frontier[i]
            if node == current[0] and cost < current[1]:
                return True
        return False

    def sort_UCS_Astar(self, a, n):
        # sort by cost
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if a[i][1] > a[j][1]:
                    index1 = a.index(a[i])
                    index2 = a.index(a[j])
                    a[index1], a[index2] = a[index2], a[index1]
        # if the cost of some nodes is equal then sort by the order of node
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if (a[i][1] == a[j][1]) and (a[i][0] > a[j][0]):
                    index1 = a.index(a[i])
                    index2 = a.index(a[j])
                    a[index1], a[index2] = a[index2], a[index1]

    def uniform_cost_search(self, graph, start, goal):
        explored = []
        frontier = [(start, 0)]
        found = False
        parent = {start: None}
        current_cost = {start: 0}
        if start == goal:
            return [goal], [goal], True
        while len(frontier) and not found:
            current = frontier.pop(0)
            node = current[0]
            explored.append(node)
            if node == goal:
                found = True
                break
            neighbours = graph[node]
            for neighbour in neighbours:
                cost_node = 1
                cost = current_cost[node] + cost_node
                if neighbour not in explored:
                    pos, check = self.check_frontier(neighbour, frontier)
                    if not check:
                        frontier.append((neighbour, cost))
                        current_cost[neighbour] = cost
                        parent[neighbour] = node
                    elif check and self.check_cost(neighbour, frontier, cost):
                        frontier.pop(pos)
                        frontier.append((neighbour, cost))
                        current_cost[neighbour] = cost
                        parent[neighbour] = node

                    self.sort_UCS_Astar(frontier, len(frontier))

        if found:
            path = self.path_return(parent, start, goal)
            return path, explored, True
        else:
            return "There is no path between {} and {}".format(start, goal), explored, False

    def heuristic(self, node, goal):
        pos = self.action_level2[node]
        pos_goal = self.action_level2[goal]
        a = pos[0] + pos[1]
        b = pos_goal[0] + pos_goal[1]
        return abs(a - b)

    def sortHeuristic(self, a, n, goal):
        # sort by heuristic number
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                c = self.heuristic(a[i], goal)
                d = self.heuristic(a[j], goal)
                if c < d:
                    index1 = a.index(a[i])
                    index2 = a.index(a[j])
                    a[index1], a[index2] = a[index2], a[index1]
        # sort by node
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if (self.heuristic(a[i], goal) == self.heuristic(a[j], goal)) and (a[i] < a[j]):
                    index1 = a.index(a[i])
                    index2 = a.index(a[j])
                    a[index1], a[index2] = a[index2], a[index1]

    def greedy_best_first_search(self, graph, start, goal):
        explored = []
        frontier = [start]
        parent = {start: None}
        found = False
        if start == goal:
            return [goal], [goal], True
        while len(frontier) and not found:
            node = frontier.pop(0)
            if node not in explored:
                explored.append(node)
                neighbours = graph[node]
                self.sortHeuristic(neighbours, len(neighbours), goal)
                for neighbour in neighbours:
                    if neighbour not in explored:
                        frontier.insert(0, neighbour)
                        parent[neighbour] = node
                        if neighbour == goal:
                            found = True
                            break
        if found:
            path = self.path_return(parent, start, goal)
            return path, explored + [goal], True
        else:
            return "There is no path between {} and {}".format(start, goal), explored, False

    def astar_search(self, graph, start, goal):
        explored = []
        frontier = [(start, 0)]
        found = False
        parent = {start: None}
        current_cost = {start: 0}
        if start == goal:
            return [goal], [goal], True
        while len(frontier) and not found:
            current = frontier.pop(0)
            node = current[0]
            explored.append(node)
            if node == goal:
                found = True
                break
            neighbours = graph[node]
            for neighbour in neighbours:
                cost_node = 1
                cost = current_cost[node] + cost_node - self.heuristic(node, goal) + self.heuristic(neighbour, goal)
                if neighbour not in explored:
                    pos, check = self.check_frontier(neighbour, frontier)
                    if not check:
                        frontier.append((neighbour, cost))
                        current_cost[neighbour] = cost
                        parent[neighbour] = node
                    elif check and self.check_cost(neighbour, frontier, cost):
                        frontier.pop(pos)
                        frontier.append((neighbour, cost))
                        current_cost[neighbour] = cost
                        parent[neighbour] = node

                    self.sort_UCS_Astar(frontier, len(frontier))

        if found:
            path = self.path_return(parent, start, goal)
            return path, explored, True
        else:
            return "There is no path between {} and {}".format(start, goal), explored, False

    def make_graph(self, maze_temp):
        neighbours = []
        graph_neighbour_level2 = {}
        for i in range(self.col):
            for j in range(self.row):
                current = maze_temp[j][i]
                if current[0] == 0 or current[0] == 4 or current[0] == 2:
                    if i == 0:  # column = 0
                        right = maze_temp[j][i + 1]
                        if right[0] == 0 or right[0] == 2 or right[0] == 4:
                            neighbours.append(right[1])
                        if j == 0:
                            bottom = maze_temp[j + 1][i]
                            if bottom[0] == 0 or bottom[0] == 2 or bottom[0] == 4:
                                neighbours.append(bottom[1])
                        elif j == self.row - 1:
                            top = maze_temp[j - 1][i]
                            if top[0] == 0 or top[0] == 2 or top[0] == 4:
                                neighbours.append(top[1])
                        else:
                            bottom = maze_temp[j + 1][i]
                            top = maze_temp[j - 1][i]
                            if bottom[0] == 0 or bottom[0] == 2 or bottom[0] == 4:
                                neighbours.append(bottom[1])
                            if top[0] == 0 or top[0] == 2 or top[0] == 4:
                                neighbours.append(top[1])

                    elif j == 0:  # row = 0
                        bottom = maze_temp[j + 1][i]
                        if bottom[0] == 0 or bottom[0] == 2 or bottom[0] == 4:
                            neighbours.append(bottom[1])
                        if i == self.col - 1:
                            left = maze_temp[j][i - 1]
                            if left[0] == 0 or left[0] == 2 or left[0] == 4:
                                neighbours.append(left[1])
                        else:
                            left = maze_temp[j][i - 1]
                            right = maze_temp[j][i + 1]
                            if left[0] == 0 or left[0] == 2 or left[0] == 4:
                                neighbours.append(left[1])
                            if right[0] == 0 or right[0] == 2 or right[0] == 4:
                                neighbours.append(right[1])

                    elif i == self.col - 1:  # column = col - 1
                        left = maze_temp[j][i - 1]
                        if left[0] == 0 or left[0] == 2 or left[0] == 4:
                            neighbours.append(left[1])
                        if j == self.row - 1:
                            top = maze_temp[j - 1][i]
                            if top[0] == 0 or top[0] == 2 or top[0] == 4:
                                neighbours.append(top[1])
                        else:
                            top = maze_temp[j - 1][i]
                            bottom = maze_temp[j + 1][i]
                            if top[0] == 0 or top[0] == 2 or top[0] == 4:
                                neighbours.append(top[1])
                            if bottom[0] == 0 or bottom[0] == 2 or bottom[0] == 4:
                                neighbours.append(bottom[1])

                    elif j == self.row - 1:  # row
                        top = maze_temp[j - 1][i]
                        if top[0] == 0 or top[0] == 2 or top[0] == 4:
                            neighbours.append(top[1])
                        left = maze_temp[j][i - 1]
                        right = maze_temp[j][i + 1]
                        if left[0] == 0 or left[0] == 2 or left[0] == 4:
                            neighbours.append(left[1])
                        if right[0] == 0 or right[0] == 2 or right[0] == 4:
                            neighbours.append(right[1])

                    else:
                        top = maze_temp[j - 1][i]
                        bottom = maze_temp[j + 1][i]
                        left = maze_temp[j][i - 1]
                        right = maze_temp[j][i + 1]
                        if top[0] == 0 or top[0] == 2 or top[0] == 4:
                            neighbours.append(top[1])
                        if bottom[0] == 0 or bottom[0] == 2 or bottom[0] == 4:
                            neighbours.append(bottom[1])
                        if left[0] == 0 or left[0] == 2 or left[0] == 4:
                            neighbours.append(left[1])
                        if right[0] == 0 or right[0] == 2 or right[0] == 4:
                            neighbours.append(right[1])
                neighbours.sort(reverse=False)
                graph_neighbour_level2[current[1]] = neighbours
                neighbours = []

        return graph_neighbour_level2

    def run_level2(self):
        temp_map = []
        maze_temp = []
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                temp_map.append(0)

            maze_temp.append(temp_map)
            temp_map = []
        temp = 0
        pacman = 0
        food = 0
        for i in range(self.col):
            for j in range(self.row):
                if self.map[j][i] == 4:
                    pacman = temp
                if self.map[j][i] == 2:
                    food = temp
                maze_temp[j][i] = [self.map[j][i], temp]
                self.action_level2[temp] = [j, i]
                temp += 1

        graph = self.make_graph(maze_temp)

        print("1. BFS")
        print("2. UCS")
        print("3. Greedy")
        print("4. A star")
        al = input("Choose algorithm: ")
        if al == 1:
            path, explore, c = self.breadth_first_search(graph, pacman, food)
        elif al == 2:
            path, explore, c = self.uniform_cost_search(graph, pacman, food)
        elif al == 2:
            path, explore, c = self.greedy_best_first_search(graph, pacman, food)
        else:
            path, explore, c = self.astar_search(graph, pacman, food)

        # print("path: ", path)
        # print("explore: ", explore)

        if c:
            print("Time to finished: ", len(path))
            print("The length of the discovered paths: ", len(explore))
            print("Point: ", 20 - len(path))
            move = []
            for i in range(len(path)):
                move.append(self.action_level2[path[i]])
                i += 1
            check = True
            self.draw_map()
            pygame.display.update()
            while check:
                for i in range(len(move)):
                    if i != 0:
                        clock.tick(5)
                        re = move[i - 1]
                        pos = move[i]
                        self.map[re[0]][re[1]] = 0
                        self.map[pos[0]][pos[1]] = 4
                        self.draw_map()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                        pygame.display.update()
                check = False

            clock.tick(5)
            self.draw_map()
            pygame.display.update()
        else:
            print("Can not find food")
            print("Point: 0")
            self.draw_map()
            pygame.display.update()

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
    def  run_level1(self):
        print("1. Breath - First Search")
        print("2. Uniform Cost Search")
        print("3. A* ")
        print("4. Greedy Breath First Seach")
        choice=input("Choose Algorithm: ")
        if int(choice) == 1:
            self.BFS_ship(self.pacman,self.food[0])
        elif int(choice) == 2:
            self.UCS_ship(self.pacman,self.food[0])
        elif int(choice) == 3:
            pass
        elif int(choice) == 4 :
            pass
    
    def BFS_ship(self,ship,food):
        #assum that ship = [x,y]
        food_found = False
        list_child = list()# [father,child] with father = [x,y], child = [x,y]
        founded_path = list()
        frontier = list()
        explore = list()
        list_child = list()
        init_node = ship
        frontier.append(ship)
        if (ship[0]==food[0] and ship[1]==food[1]):
            return
        while food_found==False:
            if not frontier:
                print("Food not found")
                return
            temp_list = list()
            pop_node = frontier.pop(0)
            explore.append(pop_node)
            #finding surround templist = [child1, child2,child3,child4] with child = [x,y]
            if (pop_node[1]-1>=0 and pop_node[1]-1<self.col):#up
                if self.map[pop_node[0]][pop_node[1]-1]!=1:
                    cur_node = [pop_node[0],pop_node[1]-1]
                    temp_list.append(cur_node)
            if (pop_node[0]+1>=0 and pop_node[0]+1<self.row):   #right     
                if self.map[pop_node[0]+1][pop_node[1]]!=1:
                    cur_node = [pop_node[0]+1,pop_node[1]]
                    temp_list.append(cur_node)
            if (pop_node[1]+1>=0 and pop_node[1]+1<self.col):#down
                if self.map[pop_node[0]][pop_node[1]+1]!=1:
                    cur_node = [pop_node[0],pop_node[1]+1]
                    temp_list.append(cur_node)
            if (pop_node[0]-1>=0 and pop_node[0]-1<self.row):#left
                if self.map[pop_node[0]-1][pop_node[1]]!=1:
                    cur_node = [pop_node[0]-1,pop_node[1]]
                    temp_list.append(cur_node) 
            for i in temp_list:
                flag_frontier = False
                flag_explore = False
                if i[0]==food[0] and i[1]==food[1]:
                    list_child.append([pop_node,i])
                    food_found = True
                    break
                for j in frontier:
                    if i[0]==j[0] and j[1]==i[1]:
                        flag_frontier=True
                for z in explore:
                    if i[0] == z[0] and i[1]==z[1]:
                        flag_explore=True
                if flag_explore==False and flag_frontier == False:
                    frontier.append(i)     
                    list_child.append([pop_node,i])
    #finding path
        founded_path.append(food)
        cur = food
        while True:
            for i in list_child:
                if i[1][0] == cur[0] and i[1][1]==cur[1]:
                    cur = i[0]
                    founded_path.append(cur)
            if cur[0]==ship[0] and cur[1]==ship[1]:
                break
        founded_path.reverse()
    #VE= 
        if True == True:
            print("Time to finished: ", len(founded_path))
            print("The length of the discovered paths: ", len(explore))
            print("Point: ", 20 - len(founded_path))
            check = False
            self.draw_map()
            pygame.display.update()
            pos = 0
            cur = founded_path[pos]
            while check == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if cur[0]==food[0] and cur[1]==food[1]:
                    check = True
                clock.tick(5)
                re = cur
                pos+=1
                if pos == len(founded_path):
                    break
                cur = founded_path[pos]
                self.map[re[0]][re[1]] = 0
                self.map[cur[0]][cur[1]] = 4
                clock.tick(5)
                self.draw_map()
                pygame.display.update()
        else:
            print("Can not find food")
            print("Point: 0")
            self.draw_map()
            pygame.display.update()
    def UCS_ship(self,ship,food):
        #assum that ship = [x,y]
        food_found = False
        list_child = list()# [father,child] with father = [x,y], child = [x,y]
        founded_path = list()
        frontier = list()# frontier = [*[[x,y],1]*,*[[x,y],2]*]
        explore = list()
        list_child = list()
        init_node = [ship,0] #init_node = [ship= [x,y],cost= int]
        frontier.append(init_node)
        if (ship[0]==food[0] and ship[1]==food[1]):
            return
        while food_found==False:
            if not frontier:
                print("Food not found")
                return
            temp_list = list()
            #sort UCS
            pop_node = frontier.pop(0)#[[x,y],cost]
            explore.append(pop_node)
            #finding surround templist = [child1, child2,child3,child4] with child = [x,y]
            if (pop_node[0][1]-1>=0 and pop_node[0][1]-1<self.col):#up
                if self.map[pop_node[0][0]][pop_node[0][1]-1]!=1:
                    cur_node = [[pop_node[0][0],pop_node[0][1]-1],pop_node[1]+1]
                    temp_list.append(cur_node)
            if (pop_node[0][0]+1>=0 and pop_node[0][0]+1<self.row):   #right     
                if self.map[pop_node[0][0]+1][pop_node[0][1]]!=1:
                    cur_node = [[pop_node[0][0]+1,pop_node[0][1]],pop_node[1]+1]
                    temp_list.append(cur_node)
            if (pop_node[0][1]+1>=0 and pop_node[0][1]+1<self.col):#down
                if self.map[pop_node[0][0]][pop_node[0][1]+1]!=1:
                    cur_node = [[pop_node[0][0],pop_node[0][1]+1],pop_node[1]+1]
                    temp_list.append(cur_node)
            if (pop_node[0][0]-1>=0 and pop_node[0][0]-1<self.row):#left
                if self.map[pop_node[0][0]-1][pop_node[0][1]]!=1:
                    cur_node = [[pop_node[0][0]-1,pop_node[0][1]],pop_node[1]+1]
                    temp_list.append(cur_node) 
            for i in temp_list:#temp_list = [[node,cost],[node],cost]
                flag_frontier = False
                flag_explore = False
                check = i
                if i[0][0]==food[0] and i[0][1]==food[1]:
                    list_child.append([pop_node[0],i[0]])
                    food_found = True
                    break
                for j in frontier:
                    if i[0][0]==j[0][0] and j[0][1]==i[0][1]:
                        if check[1] < j[1]:
                            for find in frontier:
                                if check[0][0] == find[0][0] and check[0][1]== find[0][1]:
                                    frontier.pop(find)
                                    frontier.append(check)
                                    for x in list_child:
                                        if j[0]==x[0]:
                                            list_child.pop(x)
                                            list_child.append(pop_node[0],check[0])
                                            break
                        flag_frontier=True
                for z in explore:
                    if i[0][0] == z[0][0] and i[0][1]==z[0][1]:
                        flag_explore=True
                if flag_explore==False and flag_frontier == False:
                    frontier.append(i)    
                    list_child.append([pop_node[0],i[0]])
    #finding path
        founded_path.append(food)
        cur = food
        while True:
            for i in list_child:
                if i[1][0] == cur[0] and i[1][1]==cur[1]:
                    cur = i[0]
                    founded_path.append(cur)
            if cur[0]==ship[0] and cur[1]==ship[1]:
                break
        founded_path.reverse()
    #VE= 
        if True == True:
            print("Time to finished: ", len(founded_path))
            print("The length of the discovered paths: ", len(explore))
            print("Point: ", 20 - len(founded_path))
            check = False
            self.draw_map()
            pygame.display.update()
            pos = 0
            cur = founded_path[pos]
            while check == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if cur[0]==food[0] and cur[1]==food[1]:
                    check = True
                clock.tick(5)
                re = cur
                pos+=1
                if pos == len(founded_path):
                    break
                cur = founded_path[pos]
                self.map[re[0]][re[1]] = 0
                self.map[cur[0]][cur[1]] = 4
                clock.tick(5)
                self.draw_map()
                pygame.display.update()
        else:
            print("Can not find food")
            print("Point: 0")
            self.draw_map()
            pygame.display.update()