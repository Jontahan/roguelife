# Generator: Takes in a set of parameters, and returns a world object
import sys

import scipy.ndimage

from .world import World, Character
from .enemy import EnemyController, GridGraph

from scipy.ndimage.measurements import label

import random
import numpy as np
import json

class WorldGenerator:
    def __init__(self, game, evo_system):
        self.game = game
        self.evo_system = evo_system
        self.level_params = evo_system.get_initial_population()
        self.params = self.level_params[0].copy()
        self.fitness_scores = []
        self.log = []
        self.generation = 0
    
    def register_fitness(self, fitness):
        self.fitness_scores.append(fitness)
        
        if len(self.fitness_scores) >= len(self.level_params):
            self.generation += 1
            print("Generation: ", self.generation)
            self.log.append({'population' : self.level_params.copy(), 'fitness' : self.fitness_scores.copy()})
            self.level_params = self.evo_system.get_new_generation(list(zip(self.level_params, self.fitness_scores)))
            self.fitness_scores = []

    def save_log(self, fname):
        spec_cpy = self.evo_system.spec.copy()
        for key in spec_cpy:
            del spec_cpy[key]['dtype']
        with open('{}_log.txt'.format(fname), 'w') as file:
            file.write(json.dumps({'spec' : spec_cpy, 'population_history' : self.log}))

    def get_position_neighbours(self, world, matrix, i, j, depth):

        neighbours = []
        bordering_edges = False

        if depth <= 0:
            print("Depth variable needs to be greater than 0")
            exit()

        for n_i in range(i - depth, i + depth + 1):
            for n_j in range(j - depth, j + depth + 1):


                if n_i < 0 or n_i >= world.height or n_j < 0 or n_j >= world.height:
                    bordering_edges = True
                    continue
                if n_i == i and n_j == j:
                    continue
                if matrix[n_i][n_j]:
                    neighbours.append([n_i, n_j])

        return neighbours, bordering_edges


    def generate_rocks(self, world):

        for i in range(world.width):
            for j in range(world.height):
                if random.uniform(0, 1) < self.params['initial_rock_density']:
                    world.map_rock[i][j] = 1

        for run in range(self.params['rock_refinement_runs']):
            to_add = []
            to_remove = []
            for i in range(world.width):
                for j in range(world.height):
                    neighbors, bordering = self.get_position_neighbours(world, world.map_rock, i, j, self.params['rock_neighbour_depth'])
                    if (len(neighbors) >= self.params['rock_neighbour_number']):
                        to_add.append([i, j])
                    else:
                        to_remove.append([i,j])
            for cord in to_add:
                world.map_rock[cord[0]][cord[1]] = 1
            for cord in to_remove:
                world.map_rock[cord[0]][cord[1]] = 0

        return world

    def generate_trees(self, world):

        for i in range(world.width):
            for j in range(world.height):

                if random.uniform(0, 1) < self.params['initial_tree_density'] and world.map_rock[i][j] != 1:
                    world.map_tree[i][j] = 3

        for run in range(self.params['tree_refinement_runs']):
            to_add = []
            to_remove = []
            for i in range(world.width):
                for j in range(world.height):
                    neighbors, bordering = self.get_position_neighbours(world, world.map_tree, i, j, self.params['tree_neighbour_depth'])
                    if (len(neighbors) >= self.params['tree_neighbour_number']) and world.map_rock[i][j] != 1:
                        to_add.append([i, j])
                    else:
                        to_remove.append([i,j])
            for cord in to_add:
                world.map_tree[cord[0]][cord[1]] = 3
            for cord in to_remove:
                world.map_tree[cord[0]][cord[1]] = 0

        return world


    def generate_world_base_and_player(self, world):
        possibilities = []

        counter = 0

        random.seed(self.params['random_seed'])

        while len(possibilities) == 0:
            world.map_rock = np.zeros((world.width, world.height))
            
            self.generate_rocks(world)
            

            inv_map = 1 - world.map_rock

            labeled, ncomponents = label(inv_map)

            if ncomponents > 1:
                possibilities = []
            else:
                world.map_tree = np.zeros((world.width, world.height))
                self.generate_trees(world)
                for i in range(world.width):
                    for j in range(world.height):
                        rock_neighbors, bordering = self.get_position_neighbours(world, world.map_rock, i, j, 1)
                        tree_neighbors, bordering = self.get_position_neighbours(world, world.map_tree, i, j, 1)

                        if (len(rock_neighbors) == 0 and len(tree_neighbors) == 0) and (not bordering) and not world.map_rock[i,j]:
                                possibilities.append([i, j])


            counter += 1
            if self.params['initial_rock_density'] > 0.3 or counter > 30:
                self.params['initial_rock_density'] -= 0.05
                self.params['initial_tree_density'] -= 0.05

            if counter > 10000:
                print("World generation parameters don't allow a base with a self.params['base_clear_depth'] of ", self.params['base_clear_depth'])
                exit()

        chosen_one = random.choice(possibilities)

        world.map_base[chosen_one[0]][chosen_one[1]] = 10
        
        world.base_x, world.base_y = chosen_one 
        
        player_possibilities = []

        for n_i in range(chosen_one[1] - self.params['base_clear_depth'], chosen_one[1] + self.params['base_clear_depth'] + 1):
            for n_j in range(chosen_one[0] - self.params['base_clear_depth'], chosen_one[0] + self.params['base_clear_depth'] + 1):
                if n_i != chosen_one[1] or n_j != chosen_one[0]:
                    player_possibilities.append([n_i, n_j])

        chosen_one = random.choice(player_possibilities)

        world.player.y = chosen_one[0]
        world.player.x = chosen_one[1]

        return

    def get_world(self):
        self.params = self.level_params[len(self.fitness_scores)].copy()

        world = World(self.game)

        self.generate_world_base_and_player(world)



        grassTiles = np.array(np.invert( np.logical_or(np.logical_or(world.map_tree, world.map_rock ), np.random.randint(2, size=(world.height, world.width)) )) , dtype=float)

        grassTiles = scipy.ndimage.gaussian_filter(grassTiles, sigma=1.0)
        world.map_grass = grassTiles
        
        world.enemies = []
        for _ in range(5):
            pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            while not world.is_pos_free(pos):
                pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            world.enemies.append(EnemyController(Character(pos, world), world, self.params['enemies_crush_trees'], self.params['flee_distance']))

        return world


    def create_map_by_parameters(self, parameters, world):

        self.params = parameters


        possibilities = []

        counter = 0

        while len(possibilities) == 0:
            world.map_rock = np.zeros((world.width, world.height))
            
            self.generate_rocks(world)
            

            inv_map = 1 - world.map_rock

            labeled, ncomponents = label(inv_map)

            if ncomponents > 1:
                possibilities = []
            else:
                world.map_tree = np.zeros((world.width, world.height))
                self.generate_trees(world)
                for i in range(world.width):
                    for j in range(world.height):
                        rock_neighbors, bordering = self.get_position_neighbours(world, world.map_rock, i, j, self.params['base_clear_depth'])
                        tree_neighbors, bordering = self.get_position_neighbours(world, world.map_tree, i, j, self.params['base_clear_depth'])

                        if (len(rock_neighbors) == 0 and len(tree_neighbors) == 0) and (not bordering) and not world.map_rock[i,j]:
                                possibilities.append([i, j])


            counter += 1
            if self.params['initial_rock_density'] > 0.3 or counter > 30:
                self.params['initial_rock_density'] -= 0.05
                self.params['initial_tree_density'] -= 0.05

            if counter > 10000:
                print("World generation parameters don't allow a base with a self.params['base_clear_depth'] of ", self.params['base_clear_depth'])
                exit()

        chosen_one = random.choice(possibilities)

        world.map_base[chosen_one[0]][chosen_one[1]] = 10
        
        world.base_x, world.base_y = chosen_one 
        
        player_possibilities = []

        for n_i in range(chosen_one[1] - self.params['base_clear_depth'], chosen_one[1] + self.params['base_clear_depth'] + 1):
            for n_j in range(chosen_one[0] - self.params['base_clear_depth'], chosen_one[0] + self.params['base_clear_depth'] + 1):
                if n_i != chosen_one[1] or n_j != chosen_one[0]:
                    player_possibilities.append([n_i, n_j])

        chosen_one = random.choice(player_possibilities)

        world.player.y = chosen_one[0]
        world.player.x = chosen_one[1]

        return








































