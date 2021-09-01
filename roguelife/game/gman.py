import os
import pygame as pg

class GraphicsManager:
    def __init__(self, scale):
        pwd = os.path.dirname(os.path.realpath(__file__))
        self.scale = scale

        self.src_scale = 16
        tile_sheet = pg.image.load(os.path.join(pwd, 'res', 'rogueliketiles.png'))
        creature_sheet = pg.image.load(os.path.join(pwd, 'res', 'roguelikecreatures.png'))
        
        self.sprites = {
            'tree' : self.get_tile(tile_sheet, 0, 0),
            'wall' : self.get_tile(tile_sheet, 1, 1),
            'person' : self.get_tile(creature_sheet, 0, 0),
            'skeleton' : self.get_tile(creature_sheet, 0, 6),
            'arrow' : self.get_tile(tile_sheet, 4, 2),
            'rock' : self.get_tile(tile_sheet, 4, 5),
            'base': self.get_tile(tile_sheet, 4, 8),
            'grave': self.get_tile(tile_sheet, 4, 7),
            'grass': self.get_tile(tile_sheet, 1, 0)

        }

    def get_tile(self, sheet, x, y):
        tile = pg.Surface((self.src_scale, self.src_scale), pg.SRCALPHA)
        tile.blit(sheet, (0, 0), pg.Rect(self.src_scale * x, self.src_scale * y, self.src_scale, self.src_scale))
        return pg.transform.scale(tile, (self.scale, self.scale))
