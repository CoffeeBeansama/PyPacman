import pygame as pg
from pygame import mixer
from settings import *
from abc import ABC,abstractmethod

class Pellet(ABC,pg.sprite.Sprite):

    def __init__(self,groups):
        super().__init__(groups)
        self.collision_count = 0

class Smol_pellet(Pellet):
    def __init__(self,image,pos,group,object_type):
        super().__init__(group)

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type



    def Eaten(self,groups):
        self.remove(groups)

class PowerPellet(Pellet):
    def __init__(self,image,pos,group,object_type):
        super().__init__(group)

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.object_type = object_type


    def Eaten(self,player,groups):
        player.PowerUp = True
        self.remove(groups)




