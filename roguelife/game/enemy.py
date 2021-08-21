from queue import PriorityQueue
import numpy as np
import math

class EnemyController:
    def __init__(self, character, world, enemies_crush_trees, flee_distance):
        self.world = world
        self.character = character

        self.boredom = 70

        self.flee_distance = flee_distance

        self.buried_steps = 20
        if enemies_crush_trees:
            solids = self.world.map_rock
        else:
            solids = np.logical_or(self.world.map_tree, self.world.map_rock)
        
        self.gg = GridGraph((self.world.width, self.world.height), solids)

    def step(self):

        if self.buried_steps:
            self.buried_steps -= 1
        else:

            self.boredom -= 1

            path = self.gg.get_shortest_path((self.character.x, self.character.y), (self.world.base_x, self.world.base_y))
            action = self.world.game.A_NOP

            if math.hypot(self.character.x - self.world.player.x, self.character.y - self.world.player.y) <= self.flee_distance and self.boredom > 0:

                if (abs(self.character.x - self.world.player.x) < abs(self.character.y - self.world.player.y)) and self.character.x + 1 < self.world.width and self.character.x > 1:
                    if self.character.x < self.world.player.x:
                        action = self.world.game.A_LEFT
                    else:
                        action = self.world.game.A_RIGHT
                elif (self.character.y + 1) < self.world.height and self.character.y > 1:
                    if self.character.y < self.world.player.y:
                        action = self.world.game.A_UP
                    else:
                        action = self.world.game.A_DOWN
            
            elif path:
                src, dst = ((self.character.x, self.character.y), path[-1])
            
                if dst[1] - src[1] == 1:
                    action = self.world.game.A_DOWN
                if dst[1] - src[1] == -1:
                    action = self.world.game.A_UP
                if dst[0] - src[0] == 1:
                    action = self.world.game.A_RIGHT
                if dst[0] - src[0] == -1:
                    action = self.world.game.A_LEFT
                
            
            obstacle_found = self.character.move(action)

            if obstacle_found:
                if self.world.map_tree[obstacle_found[0]][obstacle_found[1]]:
                     self.world.map_tree[obstacle_found[0]][obstacle_found[1]] -= 1
                if self.world.map_base[obstacle_found[0]][obstacle_found[1]]:
                     self.world.map_base[obstacle_found[0]][obstacle_found[1]] -= 1








class GridGraph:
    def __init__(self, dimensions, solids):
        self.width, self.height = dimensions
        self.gdict = {}

        # Build graph
        for cell_x in range(self.width):
            for cell_y in range(self.height):
                if solids[cell_x][cell_y] == 0:
                    neighbors = []
                    if cell_x + 1 in range(self.width) and solids[cell_x + 1][cell_y] == 0:
                        neighbors.append((cell_x + 1, cell_y))
                    if cell_x - 1 in range(self.width) and solids[cell_x - 1][cell_y] == 0:
                        neighbors.append((cell_x - 1, cell_y))
                    if cell_y + 1 in range(self.height) and solids[cell_x][cell_y + 1] == 0:
                        neighbors.append((cell_x, cell_y + 1))
                    if cell_y - 1 in range(self.height) and solids[cell_x][cell_y - 1] == 0:
                        neighbors.append((cell_x, cell_y - 1))

                    self.gdict[(cell_x, cell_y)] = neighbors

    # Dijkstra, returns reverse path [dst is first element]
    def get_shortest_path(self, src, dst):
        if src not in self.gdict.keys() or \
           dst not in self.gdict.keys() or \
           src == dst:
            return None

        pbuf = PriorityQueue()
        pbuf.put((0, src))

        unex = list(filter(lambda x: x != src, self.gdict.keys()))
        parent = {}

        while not pbuf.empty():
            dist, pos = pbuf.get()
            if pos == dst:
                path = [pos] # reverse
                cnode = parent[pos]

                while cnode in parent.keys():
                    path.append(cnode)
                    cnode = parent[cnode]

                return path

            for npos in self.gdict[pos]:
                if npos in unex:
                    pbuf.put((dist + 1, npos))
                    unex.remove(npos)
                    parent[npos] = pos

        return None