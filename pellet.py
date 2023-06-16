import pygame as pg
from abc import ABC,abstractmethod

class Pellet(ABC,pg.sprite.Sprite):

    def __init__(self,groups):
        super().__init__(groups)

    @abstractmethod
    def eat(self):
        pass

class Smol_pellet(Pellet):

    def __init__(self,image,pos,group,object_type):
        super().__init__(group)


        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)

        self.object_type = object_type


    def eat(self):
        self.kill()


class Big_pellet(Pellet):
    def __init__(self,image,pos,group,object_type):
        super().__init__(group)

        self.image = pg.image.load(image).convert_alpha()
        
        self.rect = self.image.get_rect(topleft=pos)

        self.object_type = object_type

    def powerUp(self):
        pass

    def eat(self):
        self.powerUp()
        self.kill()


