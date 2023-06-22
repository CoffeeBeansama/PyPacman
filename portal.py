import pygame as pg
from entity import Entity

class Portal(Entity):
    def __init__(self,image,pos,group,transport_pos):
        super().__init__(group)

        self.image = pg.image.load(image).convert_alpha()
        self.transport_pos = transport_pos
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0,0)

