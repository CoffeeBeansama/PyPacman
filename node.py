import pygame as pg
from entity import Entity

class Node(Entity):
    def __init__(self,image,pos,group):
        super().__init__(group)

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0,0)

