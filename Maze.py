import os
import pygame
import numpy
import time
import random
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
        self.pacman = []
        self.monster = []  # list of monster
        self.food = []  # list [[y,x],[y,x]]
        self.row = 0  # size of row
        self.col = 0  # size of collum
        self.frontier = []
        self.expanded = []
        self.discovered_path = []
        self.point = 20
        self.time = 0
        self.level = 0  # level of game
        self.maze_map = 0  # level of map
        self.action_level2 = {}

    def test(self):
        i = 1
        while i < 12:
            self.map[0][i - 1] = 0
            self.map[0][i] = 4
            self.draw_map()
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
                self.random_object(1, 1)
            elif self.maze_map == 3:
                self.random_object(1, 2)
            elif self.maze_map == 4:
                self.random_object(1, 2)
            elif self.maze_map == 5:
                self.random_object(1, 3)
        elif self.level == 3:
            if self.maze_map == 1:
                self.random_object(10, 1)
            elif self.maze_map == 2:
                self.random_object(15, 1)
            elif self.maze_map == 3:
                self.random_object(15, 2)
            elif self.maze_map == 4:
                self.random_object(30, 2)
            elif self.maze_map == 5:
                self.random_object(30, 3)
        elif self.level == 4:
            if self.maze_map == 1:
                self.random_object(10, 1)
            elif self.maze_map == 2:
                self.random_object(15, 1)
            elif self.maze_map == 3:
                self.random_object(15, 2)
            elif self.maze_map == 4:
                self.random_object(30, 2)
            elif self.maze_map == 5:
                self.random_object(30, 3)

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
        return abs(pos_goal[0] - pos[0]) + abs(pos_goal[1] - pos[1])

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
                cost = current_cost[node] + cost_node - \
                    self.heuristic(node, goal) + \
                    self.heuristic(neighbour, goal)
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
        elif al == 3:
            path, explore, c = self.greedy_best_first_search(
                graph, pacman, food)
        else:
            path, explore, c = self.astar_search(graph, pacman, food)

        # print("path: ", path)
        # print("explore: ", explore)

        if c:
            start = time.time()
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
                                pygame.quit()
                                exit()
                        pygame.display.update()
                end = time.time()
                print("Time to finished: ", end - start)
                print("The length of the discovered paths: ", len(path))
                print("Point: ", 20 - len(path))
                check = False

            clock.tick(5)
            self.draw_map()
            pygame.display.update()
        else:
            print("Can not find food")
            print("Point: 0")
            self.draw_map()
            pygame.display.update()
#------------------------------------------ LV3
    def BFS_lv3(self, goal):
        check_stop = True
        frontier_parent = []
        expanded_parent = []
        path = []
        self.frontier.append(self.pacman)
        frontier_parent.append(-1)
        while check_stop:
            if len(self.frontier) == 0:
                path.append(self.pacman)
                path.append(self.pacman)
                break
            self.expanded.append(self.frontier[0])
            self.frontier = self.frontier[1:]
            expanded_parent.append(frontier_parent[0])
            frontier_parent = frontier_parent[1:]
            adjacency_node = self.ACTION(
                self.expanded[len(self.expanded) - 1], 1)
            for i in adjacency_node:
                if not i in self.expanded:
                    if i[0] == goal[0] and i[1] == goal[1]:
                        expanded_parent.append(len(self.expanded) - 1)
                        self.expanded.append(i)
                        parent_pos = len(self.expanded) - 1
                        while parent_pos != -1:
                            path.append(self.expanded[parent_pos])
                            parent_pos = expanded_parent[parent_pos]
                        path.reverse()
                        check_stop = False
                    else:
                        if not i in self.frontier:
                            frontier_parent.append(len(self.expanded) - 1)
                            self.frontier.append(i)
        self.expanded.clear()
        self.frontier.clear()
        return path[1]

    def child_not_in(self, child, List):
        for items in List:
            if items[1][0] == child[0] and items[1][1] == child[1]:
                return False
        return True

    def mahattan(self, pacman, goal):
        return abs(pacman[0] - goal[0]) + abs(pacman[1] + goal[1])
    def Greedy_lv3(self, goal):
        check_stop = True
        path = []
        self.frontier.append( (self.pacman, self.pacman, 0) ) #(parent, child, manhattan)

        while check_stop:
            if len(self.frontier) == 0:
                path.append(self.pacman)
                path.append(self.pacman)
                break
            self.frontier.sort(key=lambda tup: tup[2])
            node = self.frontier.pop(0)
            self.expanded.append(node)
            if node[1][0] == goal[0] and node[1][1] == goal[1]:
                break
            adjacency_node = self.ACTION(node[1], 1)

            for child in adjacency_node:
                h = self.mahattan(child, goal)
                if self.child_not_in(child, self.expanded) and self.child_not_in(child, self.frontier):
                    self.frontier.append( (node[1], child, h) )


        path.append(self.expanded[-1][1])
        current_parent = self.expanded[-1][0]
        while True:
            if current_parent[0] == self.pacman[0] and current_parent[1] == self.pacman[1]:
                path.append(current_parent)
                break
            for i in self.expanded:
                if i[1][0] == current_parent[0] and i[1][1] == current_parent[1]:
                    path.append(i[1])
                    current_parent = i[0]
                    break
        path.reverse()
        self.expanded.clear()
        self.frontier.clear()
        return path[1]
    def monster_move_random(self, current, initial):
       rowc = current[0]
       rowi = initial[0]
       colc = current[1]
       coli = initial[1]
       move = []

       if colc == coli - 1:
           if rowc == rowi + 1:
               move.append( [rowc - 1, colc] ) #up
           elif rowc == rowi - 1:
               move.append ( [rowc + 1, colc] ) #down
           else:
               move.append( [rowc - 1, colc] )
               move.append ( [rowc + 1, colc] )
           move.append( [rowc, colc + 1] )
       elif colc == coli + 1:
           if rowc == rowi + 1:
               move.append( [rowc - 1, colc] ) #up
           elif rowc == rowi - 1:
               move.append ( [rowc + 1, colc] ) #down
           else:
               move.append( [rowc - 1, colc] ) #left
               move.append ( [rowc + 1, colc] ) #right
           move.append( [rowc, colc - 1] )
       else:
           if rowc == rowi + 1:
               move.append( [rowc - 1, colc] ) #up
           elif rowc == rowi - 1:
               move.append ( [rowc + 1, colc] ) #down
           else:
               move.append( [rowc - 1, colc] )
               move.append ( [rowc + 1, colc] )
           move.append( [rowc, colc - 1] ) #left
           move.append( [rowc, colc + 1] ) #right

       move_real = []
       for i in range(len(move)):
           if move[i][0] >= 0 and move[i][0] <= self.row - 1 and move[i][1] >= 0 and move[i][1] <= self.col - 1 and self.map[move[i][0]][move[i][1]] != 1 and self.map[move[i][0]][move[i][1]] != 3:
               move_real.append( [move[i][0], move[i][1]] )
       return move_real[random.randint(0, len(move_real)- 1)]

    def choose_path_lv3(self, cost_path):
        temp_act = self.ACTION(self.pacman, 4)
        point_path=[]
        for i in temp_act:
            point_path.append(cost_path[i[0]][i[1]])
        max_value=max(point_path)
        position=[]
        for a,b in zip(point_path,temp_act):
            if a == max_value:
                position.append(b)

        if len(position) > 1:
            temp=numpy.random.randint(0,len(position)-1)
            cost_path[position[temp][0]][position[temp][1]]-=1
            position= position[temp]
        else:
            cost_path[position[0][0]][position[0][1]]-=1
            position = position[0]
        return position

    def run_level3(self):
        print("1. Breath - First Search")
        print("2. Greedy - Best First Search")
        choice=input("Choose Algorithm: ")

        start = time.time()
        initial_monster = self.monster.copy()
        cost_path = [[100 for _ in range(self.col)]for _ in range(self.row)]
        save = []
        check_stop = True
        turn = True
        self.discovered_path.append(self.pacman)
        for i in self.monster:
            save.append( [i[0], i[1], 0] )
        while check_stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            if turn == True:
                self.map[self.pacman[0]][self.pacman[1]] = 0
                foods, monsters = self.detect_food_monster()
                if len(foods) >= 1:
                      if int(choice) == 1:
                          self.pacman = self.BFS_lv3(foods[0])
                      else:
                          self.pacman = self.Greedy_lv3(foods[0])
                else:
                     self.pacman = self.choose_path_lv3(cost_path)

                self.map[self.pacman[0]][self.pacman[1]] = 4
                self.discovered_path.append(self.pacman)
                self.point = self.point - 1
                for i, a in enumerate(self.food):
                    if a[0] == self.pacman[0] and a[1] == self.pacman[1]:
                        self.point = self.point + 20
                        self.food.pop(i)
                        break
                turn = False
            else:
                for i in range(len(self.monster)):
                    refill = save.pop(0)
                    self.map[refill[0]][refill[1]] = refill[2]
                    new_pos = self.monster_move_random(self.monster[i], initial_monster[i])
                    if self.map[new_pos[0]][new_pos[1]] == 2:
                        save.append( [new_pos[0], new_pos[1], 2] )
                    elif self.map[new_pos[0]][new_pos[1]] == 0:
                        save.append( [new_pos[0], new_pos[1], 0] )
                    self.monster[i] = new_pos.copy()
                    self.map[new_pos[0]][new_pos[1]] = 3
                    turn= True

            if self.check_stop():
                check_stop = False
            clock.tick(5)
            self.draw_map()
            pygame.display.update()
        end = time.time()
        print("Len of discovered pạth: " + str(len(self.discovered_path)))
        print("Time: " + str(end - start))
        print("Point: " + str(self.point))
#-----------------------------------------------------------
    def run_level4(self):
        start = time.time()
        step=0
        cost_path = [[100 for _ in range(self.col)]for _ in range(self.row)]
        check_stop = True
        turn = True
        while check_stop:
            clock.tick(10)
            if turn:
                self.map[self.pacman[0]][self.pacman[1]] = 0
                self.pacman = self.choose_path(cost_path)
                self.map[self.pacman[0]][self.pacman[1]] = 4
                for i, a in enumerate(self.food):
                    if a[0] == self.pacman[0] and a[1] == self.pacman[1]:
                        self.food.pop(i)
                        self.point+=20
                        break
                self.point-=1
                step+=1
                turn = False
            else:
                #print("MONSTER")
                action = self.MONSTER_ACTION(self.pacman, self.monster)
                #print("action: ", end="")
                # print(action)
                for i in self.monster:
                    self.map[i[0]][i[1]] = 0
                for i in self.food:
                    self.map[i[0]][i[1]] = 2
                self.monster = action
                for i in self.monster:
                    self.map[i[0]][i[1]] = 3
                turn = True
            if self.check_stop():
                end=time.time()
                print("Time to finished: ", end - start)
                print("The length of the discovered paths: ", step)
                print("Point: ", self.point)
                check_stop = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.draw_map()
            pygame.display.update()

    def check_stop(self):
        # check when all of food is eaten or monster collides with pacman
        # when monster collides with pacman, the position of bacman should be changed into (-1,-1)
        if len(self.food) == 0:
            return True
        for i in self.monster:
            if i[0] == self.pacman[0] and i[1] == self.pacman[1]:
                self.map[i[0]][i[1]]=3
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

    def choose_path(self,cost_path):
        food, monster = self.detect_food_monster()
        temp_act = self.ACTION(self.pacman, 4)
        v = -999999
        a = -999999
        point_path=[]
        for i in temp_act:
            point_path.append(self.MIN_VALUE(self.pacman,i, food, monster, 1, a))
        max_value=max(point_path)
        position=[]
        for a,b in zip(point_path,temp_act):
            if a == max_value:
                position.append(b)
        #print(position)
        if len(position) > 1:
            temp_cost=[cost_path[i[0]][i[1]] for i in position]
            max_value=max(temp_cost)
            temp_array=[]
            for a,b in zip(temp_cost,position):
                if a == max_value:
                    temp_array.append(b)
            if len(temp_array) > 1:
                temp=numpy.random.randint(0,len(temp_array)-1)
                cost_path[temp_array[temp][0]][temp_array[temp][1]]-=1
                position=temp_array[temp]
            else:
                cost_path[temp_array[0][0]][temp_array[0][1]]-=1
                position = temp_array[0]
        else:
            position=position[0]
        return position

    def MAX_VALUE(self,parent,state, food, monster, step, a):
        check = self.TERMINAL_TEST(state, food, monster)
        if check:
            if check == 1:
                temp_monster = monster.copy()
                monster = self.MONSTER_ACTION(state, monster)
                check = self.TERMINAL_TEST(state, food, monster)
                monster = temp_monster
                if check == -1:
                    return self.point - step + 20 - 2**(20 - step)
                else:
                    return self.point - step + 20
            if check == -1:
                #if abs(state[0]-self.pacman[0]) + abs(state[1]-self.pacman[1])
                return self.point - step - 2**(20 - step)
        v = -999999
        temp_act = self.ACTION(state, 4,parent)
        #print(str(state)+" - "+str(temp_act))
        for i in temp_act:
            temp_value = self.map[i[0]][i[1]]
            self.map[i[0]][i[1]] = 4
            temp = self.MIN_VALUE(state,i, food, monster, step + 1, a)
            self.map[i[0]][i[1]] = temp_value
            if temp > v:
                v = temp

            a = max(a, v)
        return v

    def MIN_VALUE(self,parent,state, food, monster, step, a):
        check = self.TERMINAL_TEST(state, food, monster)
        if check:
            if check == 1:
                temp_monster = monster.copy()
                monster = self.MONSTER_ACTION(state, monster)
                check = self.TERMINAL_TEST(state, food, monster)
                monster = temp_monster
                if check == -1:
                    return self.point - step + 20 - 2**(20 - step)
                else:
                    return self.point - step + 20
            if check == -1:
                #if abs(state[0]-self.pacman[0]) + abs(state[1]-self.pacman[1])
                return self.point - step - 2**(20 - step)
        if (self.point - step) < a:
            return self.point - step
        if step == 3:
            return self.point - step
        temp_monster = monster.copy()
        monster = self.MONSTER_ACTION(state, monster)
        #print("monster: "+str(monster))
        v = self.MAX_VALUE(parent,state, food, monster, step, a)
        monster = temp_monster
        return v

    def ACTION(self, state, value,parent=[-1,-1]):
        # value to differentiate whether monster or pacman
        temp_act = []
        if state[0] - 1 >= 0 and self.map[state[0] - 1][state[1]] != 1 and self.map[state[0] - 1][state[1]] != value and ((state[0] - 1)!=parent[0] or state[1]!=parent[1]):
            temp_act.append([state[0] - 1, state[1]])
        if state[0] + 1 < self.row and self.map[state[0] + 1][state[1]] != 1 and self.map[state[0] + 1][state[1]] != value and ((state[0] + 1)!=parent[0] or state[1]!=parent[1]):
            temp_act.append([state[0] + 1, state[1]])
        if state[1] - 1 >= 0 and self.map[state[0]][state[1] - 1] != 1 and self.map[state[0]][state[1] - 1] != value and (state[0] !=parent[0] or state[1]-1!=parent[1]):
            temp_act.append([state[0], state[1] - 1])
        if state[1] + 1 < self.col and self.map[state[0]][state[1] + 1] != 1 and self.map[state[0]][state[1] + 1] != value and (state[0]!=parent[0] or state[1]+1!=parent[1]):
            temp_act.append([state[0], state[1] + 1])
        return temp_act

    def TERMINAL_TEST(self, state, food, monster):
        for i in monster:
            if i[0] == state[0] and i[1] == state[1]:
                return -1
        for i in food:
            if i[0] == state[0] and i[1] == state[1]:
                return 1
        return 0

    def MONSTER_ACTION(self, state, monster):
        action = []
        for i in monster:
            temp = self.BFS(i, state,action)
            action.append(temp)
            #print("action i: ", end="")
            # print(temp)
        return action

    def BFS(self, monster, goal,action=[]):
        return_value = []
        check_stop = True
        frontier_parent = []
        expanded_parent = []
        self.frontier.append(monster)
        frontier_parent.append(-1)
        while check_stop:
            if len(self.frontier) == 0:
                return_value.append(monster)
                return_value.append(monster)
                break
            self.expanded.append(self.frontier[0])
            self.frontier = self.frontier[1:]
            expanded_parent.append(frontier_parent[0])
            frontier_parent = frontier_parent[1:]
            adjacency_node = self.ACTION(
                self.expanded[len(self.expanded) - 1], 3)
            i=0
            for a in adjacency_node:
                for b in action:
                    if b[0]==a[0] and b[1]==a[1]:
                        adjacency_node.pop(i)
                        i-=1
                i+=1
            #print("ajd: "+str(adjacency_node))
            for i in adjacency_node:
                if not i in self.expanded:
                    if i[0] == goal[0] and i[1] == goal[1]:
                        expanded_parent.append(len(self.expanded) - 1)
                        self.expanded.append(i)
                        parent_pos = len(self.expanded) - 1
                        while parent_pos != -1:
                            return_value.append(self.expanded[parent_pos])
                            parent_pos = expanded_parent[parent_pos]
                        return_value = return_value[::-1]
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
            #self.BFS_ship(self.pacman,self.food[0])
        elif int(choice) == 2:
            self.UCS_ship(self.pacman,self.food[0])
        elif int(choice) == 3:
            self.A_star_ship(self.pacman,self.food[0])
        elif int(choice) == 4 :
            self.greedy_BFS_ship(self.pacman,self.food[0])

    def BFS_ship(self,ship,food):
        #assum that ship = [x,y]
        food_found = False
        list_child = list()# [father,child] with father = [x,y], child = [x,y]
        founded_path = list()
        frontier = list()
        explore = list()
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
            start = time.time()
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
                #clock.tick(5)
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
            end = time.time()
            print("Time to finished: ", end-start)
            print("The length of the discovered paths: ", len(founded_path))
            print("Point: ", 20 - len(founded_path))
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
            n = len(frontier)
            for i in range(n):
                for j in range(0, n-i-1):
                    if frontier[j][1] > frontier[j+1][1] :
                        frontier[j], frontier[j+1] = frontier[j+1], frontier[j]
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
            start = time.time()
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
            end = time.time()
            print("Time to finished: ", end-start)
            print("The length of the discovered paths: ", len(founded_path))
            print("Point: ", 20 - len(founded_path))
        else:
            print("Can not find food")
            print("Point: 0")
            self.draw_map()
            pygame.display.update()
    def greedy_BFS_ship(self,ship,food):
               #assum that ship = [x,y]
        food_found = False
        list_child = list()# [father,child] with father = [x,y], child = [x,y]
        founded_path = list()
        frontier = list()# frontier = [*[[x,y],1]*,*[[x,y],2]*]
        explore = list()
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
            n = len(frontier)
            for i in range(n):
                for j in range(0, n-i-1):
                    if frontier[j][1] > frontier[j+1][1] :
                         frontier[j], frontier[j+1] = frontier[j+1], frontier[j]
            pop_node = frontier.pop(0)#[[x,y],cost,h]
            if pop_node[0][0]==food[0] and pop_node[0][1]==food[1]:
                    food_found = True
                    break
            explore.append(pop_node)
            #finding surround templist = [child1, child2,child3,child4] with child = [x,y]
            if (pop_node[0][1]-1>=0 and pop_node[0][1]-1<self.col):#up
                if self.map[pop_node[0][0]][pop_node[0][1]-1]!=1:
                    p1 = pow(food[0]-pop_node[0][0],2)
                    p2 = pow(food[1] - (pop_node[0][1])-1,2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0],pop_node[0][1]-1],h]
                    temp_list.append(cur_node)
            if (pop_node[0][0]+1>=0 and pop_node[0][0]+1<self.row):   #right
                if self.map[pop_node[0][0]+1][pop_node[0][1]]!=1:
                    p1 = pow(food[0]-(pop_node[0][0]+1),2)
                    p2 = pow(food[1] - (pop_node[0][1]),2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0]+1,pop_node[0][1]],h]
                    temp_list.append(cur_node)
            if (pop_node[0][1]+1>=0 and pop_node[0][1]+1<self.col):#down
                if self.map[pop_node[0][0]][pop_node[0][1]+1]!=1:
                    p1 = pow(food[0]-pop_node[0][0],2)
                    p2 = pow(food[1] - (pop_node[0][1])+1,2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0],pop_node[0][1]+1],h]
                    temp_list.append(cur_node)
            if (pop_node[0][0]-1>=0 and pop_node[0][0]-1<self.row):#left
                if self.map[pop_node[0][0]-1][pop_node[0][1]]!=1:
                    p1 = pow(food[0]-(pop_node[0][0]-1),2)
                    p2 = pow(food[1] - (pop_node[0][1]),2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0]-1,pop_node[0][1]],h]
                    temp_list.append(cur_node)
            for i in temp_list:#temp_list = [[node,cost],[node],cost]
                flag_frontier = False
                flag_explore = False
                check = i
                for j in frontier:
                    if i[0][0]==j[0][0] and j[0][1]==i[0][1]:
                        if check[1] < j[1]:
                            count = 0
                            for find in frontier:
                                if check[0][0] == find[0][0] and check[0][1]== find[0][1]:
                                    frontier.pop(count)
                                    frontier.append(check)
                                    for x in list_child:
                                        if j[0]==x[0]:
                                            list_child.pop(x)
                                            list_child.append(pop_node[0],check[0])
                                            break
                                count+=1
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
            start = time.time()
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
            end = time.time()
            print("Time to finished: ", end-start)
            print("The length of the discovered paths: ", len(founded_path))
            print("Point: ", 20 - len(founded_path))
        else:
            print("Can not find food")
            print("Point: 0")
            self.draw_map()
            pygame.display.update()
    def A_star_ship(self,ship,food):
         #assum that ship = [x,y]
        food_found = False
        list_child = list()# [father,child] with father = [x,y], child = [x,y]
        founded_path = list()
        frontier = list()# frontier = [*[[x,y],1]*,*[[x,y],2]*]
        explore = list()
        h_ship = pow(pow(food[0]-ship[0],2)+pow(food[1]-ship[1],2),1.0/2)
        init_node = [ship,0,h_ship] #init_node = [ship= [x,y],cost= int,h=float]
        frontier.append(init_node)
        if (ship[0]==food[0] and ship[1]==food[1]):
            return
        while food_found==False:
            if not frontier:
                print("Food not found")
                return
            temp_list = list()
            #sort UCS
            n = len(frontier)
            for i in range(n):
                for j in range(0, n-i-1):
                    if (frontier[j][1]+frontier[j][2]) > (frontier[j+1][1]+frontier[j+1][2]) :
                         frontier[j], frontier[j+1] = frontier[j+1], frontier[j]
            pop_node = frontier.pop(0)#[[x,y],cost,h]
            if pop_node[0][0]==food[0] and pop_node[0][1]==food[1]:
                    food_found = True
                    break
            explore.append(pop_node)
            #finding surround templist = [child1, child2,child3,child4] with child = [x,y]
            if (pop_node[0][1]-1>=0 and pop_node[0][1]-1<self.col):#up
                if self.map[pop_node[0][0]][pop_node[0][1]-1]!=1:
                    p1 = pow(food[0]-pop_node[0][0],2)
                    p2 = pow(food[1] - (pop_node[0][1])-1,2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0],pop_node[0][1]-1],pop_node[1]+1,h]
                    temp_list.append(cur_node)
            if (pop_node[0][0]+1>=0 and pop_node[0][0]+1<self.row):   #right
                if self.map[pop_node[0][0]+1][pop_node[0][1]]!=1:
                    p1 = pow(food[0]-(pop_node[0][0]+1),2)
                    p2 = pow(food[1] - (pop_node[0][1]),2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0]+1,pop_node[0][1]],pop_node[1]+1,h]
                    temp_list.append(cur_node)
            if (pop_node[0][1]+1>=0 and pop_node[0][1]+1<self.col):#down
                if self.map[pop_node[0][0]][pop_node[0][1]+1]!=1:
                    p1 = pow(food[0]-pop_node[0][0],2)
                    p2 = pow(food[1] - (pop_node[0][1])+1,2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0],pop_node[0][1]+1],pop_node[1]+1,h]
                    temp_list.append(cur_node)
            if (pop_node[0][0]-1>=0 and pop_node[0][0]-1<self.row):#left
                if self.map[pop_node[0][0]-1][pop_node[0][1]]!=1:
                    p1 = pow(food[0]-(pop_node[0][0]-1),2)
                    p2 = pow(food[1] - (pop_node[0][1]),2)
                    h= pow(p1+p2,1.0/2)
                    cur_node = [[pop_node[0][0]-1,pop_node[0][1]],pop_node[1]+1,h]
                    temp_list.append(cur_node)
            for i in temp_list:#temp_list = [[node,cost],[node],cost]
                flag_frontier = False
                flag_explore = False
                check = i
                for j in frontier:
                    if i[0][0]==j[0][0] and j[0][1]==i[0][1]:
                        if check[1] < j[1]:
                            count = 0
                            for find in frontier:
                                if check[0][0] == find[0][0] and check[0][1]== find[0][1]:
                                    frontier.pop(count)
                                    frontier.append(check)
                                    for x in list_child:
                                        if j[0]==x[0]:
                                            list_child.pop(x)
                                            list_child.append(pop_node[0],check[0])
                                            break
                                count+=1
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
            start = time.time()
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
            end = time.time()
            print("Time to finished: ", end-start)
            print("The length of the discovered paths: ", len(founded_path))
            print("Point: ", 20 - len(founded_path))
        else:
            print("Can not find food")
            print("Point: 0")
            self.draw_map()
            pygame.display.update()
