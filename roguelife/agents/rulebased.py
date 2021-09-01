from queue import PriorityQueue
import numpy as np
import random


class RuleBasedAgent0: #The Original
    def __init__(self, env):
        self.env = env
        
        solids = np.logical_or(np.clip(self.env.world.map_tree, 0, 1), self.env.world.map_rock)
        solids[self.env.world.base_x][self.env.world.base_y] = 1
        self.gg = GridGraph((self.env.world.width, self.env.world.height), solids)

    def act(self, state):

        player = self.env.world.player
        threat_levels = []
        
        for enemy_controller in self.env.world.enemies:
            enemy = enemy_controller.character
            threat = abs(enemy.x - self.env.world.base_x) + abs(enemy.y - self.env.world.base_y)
            distance = abs(enemy.x - self.env.world.player.x) + abs(enemy.y - self.env.world.player.y)
            if distance <= 1:
                threat = 0
            threat_levels.append((enemy, threat))
        threat_levels.sort(key=lambda x: x[1])
        
        target = threat_levels[0][0]
        path = self.gg.get_shortest_path((self.env.world.player.x, self.env.world.player.y), (target.x, target.y))
        

        action = random.choice(range(6))

        if path:
            if all(list(map(lambda x: x[0] == player.x, path))): # Vertical
                if player.y - target.y < 0 and player.facing == player.DIR_S:
                    return self.env.A_ATK
                if player.y - target.y > 0 and player.facing == player.DIR_N:
                    return self.env.A_ATK
            if all(list(map(lambda x: x[1] == player.y, path))): # Horizontal
                if player.x - target.x < 0 and player.facing == player.DIR_E:
                    return self.env.A_ATK
                if player.x - target.x > 0 and player.facing == player.DIR_W:
                    return self.env.A_ATK
            
            src, dst = ((self.env.world.player.x, self.env.world.player.y), path[-1])
        
            if dst[0] - src[0] == 1:
                action = self.env.world.game.A_RIGHT
            if dst[0] - src[0] == -1:
                action = self.env.world.game.A_LEFT
            if dst[1] - src[1] == 1:
                action = self.env.world.game.A_DOWN
            if dst[1] - src[1] == -1:
                action = self.env.world.game.A_UP

        return action



class RuleBasedAgent1: #The Defender
    def __init__(self, env):
        self.env = env
        
        solids = np.logical_or(np.clip(self.env.world.map_tree, 0, 1), self.env.world.map_rock)
        solids[self.env.world.base_x][self.env.world.base_y] = 1
        self.gg = GridGraph((self.env.world.width, self.env.world.height), solids)

    def act(self, state):

        player = self.env.world.player
        threat_levels = []
        
        for enemy_controller in self.env.world.enemies:
            threat = abs(enemy_controller.character.x - self.env.world.base_x) + abs(enemy_controller.character.y - self.env.world.base_y)
            distance = abs(enemy_controller.character.x - self.env.world.player.x) + abs(enemy_controller.character.y - self.env.world.player.y)
            if distance <= 1:
                threat = 0
            threat_levels.append((enemy_controller, threat))
        threat_levels.sort(key=lambda x: x[1])
        

        target = threat_levels[0][0]
        path = self.gg.get_shortest_path((self.env.world.player.x, self.env.world.player.y), (target.character.x, target.character.y))


        if threat_levels[0][1] > 7 or ((path is not None) and (len(path) > 10)):

            path = self.gg.get_shortest_path((self.env.world.player.x, self.env.world.player.y), (self.env.world.base_x + random.choice([-1, 1]) , self.env.world.base_y + random.choice([-1, 1])))

            action = random.choice(range(6))

            if path:
        
                src, dst = ((self.env.world.player.x, self.env.world.player.y), path[-1])

                if dst[0] - src[0] == 1:
                    action = self.env.world.game.A_RIGHT
                if dst[0] - src[0] == -1:
                    action = self.env.world.game.A_LEFT
                if dst[1] - src[1] == 1:
                    action = self.env.world.game.A_DOWN
                if dst[1] - src[1] == -1:
                    action = self.env.world.game.A_UP
        else:
            target = threat_levels[0][0]
            path = self.gg.get_shortest_path((self.env.world.player.x, self.env.world.player.y), (target.character.x, target.character.y))
            

            action = random.choice(range(6))

            if path:
                if not target.buried_steps:
                    if all(list(map(lambda x: x[0] == player.x, path))): # Vertical
                        if player.y - target.character.y < 0 and player.facing == player.DIR_S:
                            return self.env.A_ATK
                        if player.y - target.character.y > 0 and player.facing == player.DIR_N:
                            return self.env.A_ATK
                    if all(list(map(lambda x: x[1] == player.y, path))): # Horizontal
                        if player.x - target.character.x < 0 and player.facing == player.DIR_E:
                            return self.env.A_ATK
                        if player.x - target.character.x > 0 and player.facing == player.DIR_W:
                            return self.env.A_ATK
                    
                src, dst = ((self.env.world.player.x, self.env.world.player.y), path[-1])
            
                if dst[0] - src[0] == 1:
                    action = self.env.world.game.A_RIGHT
                if dst[0] - src[0] == -1:
                    action = self.env.world.game.A_LEFT
                if dst[1] - src[1] == 1:
                    action = self.env.world.game.A_DOWN
                if dst[1] - src[1] == -1:
                    action = self.env.world.game.A_UP
        return action


class RuleBasedAgent2: #The Hunter Gravedigger
    def __init__(self, env):
        self.env = env
        
        solids = np.logical_or(np.clip(self.env.world.map_tree, 0, 1), self.env.world.map_rock)
        solids[self.env.world.base_x][self.env.world.base_y] = 1
        self.gg = GridGraph((self.env.world.width, self.env.world.height), solids)

    def act(self, state):

        player = self.env.world.player
        threat_levels = []
        
        for enemy_controller in self.env.world.enemies:
            # enemy = enemy_controller.character
            threat = abs(enemy_controller.character.x - self.env.world.base_x) + abs(enemy_controller.character.y - self.env.world.base_y)
            distance = abs(enemy_controller.character.x - self.env.world.player.x) + abs(enemy_controller.character.y - self.env.world.player.y)
            if distance <= 1:
                threat = 0
            threat_levels.append((enemy_controller, threat))
        threat_levels.sort(key=lambda x: x[1])
        
        target = threat_levels[0][0]
        path = self.gg.get_shortest_path((self.env.world.player.x, self.env.world.player.y), (target.character.x, target.character.y))
    

        action = random.choice(range(6))


        if path:
            if not target.buried_steps:
                if all(list(map(lambda x: x[0] == player.x, path))): # Vertical
                    if player.y - target.character.y < 0 and player.facing == player.DIR_S:
                        return self.env.A_ATK
                    if player.y - target.character.y > 0 and player.facing == player.DIR_N:
                        return self.env.A_ATK
                if all(list(map(lambda x: x[1] == player.y, path))): # Horizontal
                    if player.x - target.character.x < 0 and player.facing == player.DIR_E:
                        return self.env.A_ATK
                    if player.x - target.character.x > 0 and player.facing == player.DIR_W:
                        return self.env.A_ATK
            
            src, dst = ((self.env.world.player.x, self.env.world.player.y), path[-1])
        
            if dst[0] - src[0] == 1:
                action = self.env.world.game.A_RIGHT
            if dst[0] - src[0] == -1:
                action = self.env.world.game.A_LEFT
            if dst[1] - src[1] == 1:
                action = self.env.world.game.A_DOWN
            if dst[1] - src[1] == -1:
                action = self.env.world.game.A_UP


        return action




class RuleBasedAgent3: #The Mad Man
    def __init__(self, env):
        self.env = env
        
        solids = self.env.world.map_rock.copy()
        solids[self.env.world.base_x][self.env.world.base_y] = 1
        self.gg = GridGraph((self.env.world.width, self.env.world.height), solids)

    def act(self, state):

        player = self.env.world.player
        threat_levels = []
        
        for enemy_controller in self.env.world.enemies:
            # enemy = enemy_controller.character
            threat = abs(enemy_controller.character.x - self.env.world.player.x) + abs(enemy_controller.character.y - self.env.world.player.y)
            threat_levels.append((enemy_controller, threat))
        threat_levels.sort(key=lambda x: x[1])
        
        target = threat_levels[0][0]
        path = self.gg.get_shortest_path((self.env.world.player.x, self.env.world.player.y), (target.character.x, target.character.y))
        

        action = self.env.world.game.A_NOP

        if path:

            if self.env.world.map_tree[path[-1][0]][path[-1][1]]:

                if player.y - path[-1][1] < 0 and player.facing == player.DIR_S:
                    return self.env.A_ATK
                if player.y - path[-1][1] > 0 and player.facing == player.DIR_N:
                    return self.env.A_ATK
                if player.x - path[-1][0]< 0 and player.facing == player.DIR_E:
                    return self.env.A_ATK
                if player.x - path[-1][0] > 0 and player.facing == player.DIR_W:
                    return self.env.A_ATK


            if not target.buried_steps:
                if all(list(map(lambda x: x[0] == player.x, path))): # Vertical
                    if player.y - target.character.y < 0 and player.facing == player.DIR_S:
                        return self.env.A_ATK
                    if player.y - target.character.y > 0 and player.facing == player.DIR_N:
                        return self.env.A_ATK
                if all(list(map(lambda x: x[1] == player.y, path))): # Horizontal
                    if player.x - target.character.x < 0 and player.facing == player.DIR_E:
                        return self.env.A_ATK
                    if player.x - target.character.x > 0 and player.facing == player.DIR_W:
                        return self.env.A_ATK
            
            src, dst = ((self.env.world.player.x, self.env.world.player.y), path[-1])
        
            if dst[0] - src[0] == 1:
                action = self.env.world.game.A_RIGHT
            if dst[0] - src[0] == -1:
                action = self.env.world.game.A_LEFT
            if dst[1] - src[1] == 1:
                action = self.env.world.game.A_DOWN
            if dst[1] - src[1] == -1:
                action = self.env.world.game.A_UP
        return action



class RandomAgent: #Random Actions
    def __init__(self, env):
        self.env = env

    def act(self, state):
            
        return random.choice(range(6))






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










