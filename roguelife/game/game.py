# This file should contain rendering and input handling
import sys
import pygame as pg
import numpy as np
import random
import gym
from .gman import GraphicsManager
from PIL import Image, ImageOps
from .generator import WorldGenerator


class Game(gym.Env):
    A_NOP, A_UP, A_DOWN, A_LEFT, A_RIGHT, A_ATK = range(6)

    def __init__(self, evo_system=None):
        self.framerate = 0
        self.width, self.height = (15, 15)
        self.scale = 32
        self.encoder_scale = 1 / 4

        self.fitness = 0
        self.max_steps = 1000
        self.step_count = 0
        self.action_space = gym.spaces.Discrete(6)
        self.observation_space = gym.spaces.Box(low=0, high=255,
                                                shape=(1, 120, 120),
                                                dtype=np.uint8)

        pg.init()
        self.screen = pg.display.set_mode((self.width * self.scale, self.height * self.scale))
        self.gman = GraphicsManager(self.scale)

        self.clock = pg.time.Clock()

        self.worldgen = WorldGenerator(self, evo_system) 
        self.world = self.worldgen.get_world()


        



    
    def step(self, action):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.event.pump()

        reward, done = self.world.step(action)

        if self.step_count >= self.max_steps:
            done = True
        self.step_count += 1


        if done:
            self.fitness = len(self.world.enemies) - self.world.map_base[self.world.base_x][self.world.base_y]
            self.worldgen.register_fitness(self.fitness)

        self.render()

        pil_image = Image.frombytes("RGBA", (self.scale * self.width, self.scale * self.height),
                                    pg.image.tostring(self.screen, "RGBA", False))

        # if reward > 0: 
        #     print('reward={}!'.format(reward))

        return self.encode_state(pil_image), reward, done, {}

    def render(self, mode='human'):
        # Background
        pg.draw.rect(self.screen, (24, 24, 24), (0, 0, self.width * self.scale, self.height * self.scale))

        for i in range(self.width):
            for j in range(self.height):
                grassColor = pg.Color((31, 87, 66)).lerp((24, 57, 40), self.world.map_grass[i][j])
                pg.draw.rect(self.screen, grassColor, (i * self.scale, j * self.scale, self.scale, self.scale))
                if self.world.map_tree[i][j]:
                    self.screen.blit(self.gman.sprites['tree'], (i * self.scale, j * self.scale), (0, 0, self.scale, self.scale))
                if self.world.map_rock[i][j]:
                    self.screen.blit(self.gman.sprites['rock'], (i * self.scale, j * self.scale), (0, 0, self.scale, self.scale))
                if self.world.map_base[i][j]:
                    self.screen.blit(self.gman.sprites['base'], (i * self.scale, j * self.scale), (0, 0, self.scale, self.scale))
        
        self.screen.blit(self.gman.sprites['person'], (self.world.player.x * self.scale, self.world.player.y * self.scale), (0, 0, self.scale, self.scale))
        for enemy_controller in self.world.enemies:
            if enemy_controller.buried_steps:
                enemy = enemy_controller.character
                self.screen.blit(self.gman.sprites['grave'], (enemy.x * self.scale, enemy.y * self.scale), (0, 0, self.scale, self.scale))
            else:
                enemy = enemy_controller.character
                self.screen.blit(self.gman.sprites['skeleton'], (enemy.x * self.scale, enemy.y * self.scale), (0, 0, self.scale, self.scale))

        for arrow in self.world.arrows:
            self.screen.blit(self.gman.sprites['arrow'], (arrow.x * self.scale, arrow.y * self.scale),
                             (0, 0, self.scale, self.scale))

        pg.display.flip()

        self.clock.tick(int(self.framerate))

    def reset(self):
        self.world = self.worldgen.get_world()
        self.render()

        self.step_count = 0
        self.fitness = 0

        pil_image = Image.frombytes("RGBA", (self.scale * self.width, self.scale * self.height),
                                    pg.image.tostring(self.screen, "RGBA", False))
        return self.encode_state(pil_image)

    def screenshot(self, name):
        self.render()
        pil_image = Image.frombytes("RGBA", (self.scale * self.width, self.scale * self.height),
                                    pg.image.tostring(self.screen, "RGBA", False))
        pil_image.save('{}.png'.format(name))

    def encode_state(self, img_state):
        img_state = ImageOps.grayscale(img_state)
        img_state = ImageOps.scale(img_state, self.encoder_scale)
        img_state = np.asarray(img_state)
        img_state = np.expand_dims(img_state, axis=0)
        return img_state





