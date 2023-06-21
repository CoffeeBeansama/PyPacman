import pygame as pg
from entity import Entity
from settings import *

class Node(Entity):
    def __init__(self,image,pos,group,top,bottom,left,right):
        super().__init__(group)

        self.image = pg.image.load(image).convert_alpha()
        self.top = top

        self.bottom = bottom
        self.left = left
        self.right = right
        self.rect = self.image.get_rect(topleft=pos)
        self.availableDirections = []
        self.hitbox = self.rect.inflate(0,0)


















